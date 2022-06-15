import numpy as np
import pywavefront as pw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import sys ,time,os
import transformation as tr
class Model:
    def __init__(self,path):
        self.path = path
        self.scene = None     
        self.scene_scale = None
        self.scene_translate = None
        self.vao = None
        self.vbo = None
        self.vertices = None
        self.program = None
        self.ibo = None

    def load_model(self):
        try:
            self.scene = pw.Wavefront(self.path, collect_faces= True)
        except:
            print("model loading failed")

    def getShaders(self,filename):
        p = os.path.join(os.getcwd(), "shaders", filename)
        return open(p, 'r').read()

    def ready(self,w_width,w_height):
       
        self.load_model()
        # scene_box = (self.scene.vertices[0], self.scene.vertices[0])

        # for vertex in self.scene.vertices:
        #     min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
        #     max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
        #     scene_box = (min_v, max_v)

        # scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
        # max_scene_size = max(scene_size)
        # scaled_size    = 5
        # self.scene_scale    = [scaled_size/max_scene_size for i in range(3)]
        # self.scene_translate    = [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)]

        
        '''
        compile the shaders 
        '''
        vertex_shader = compileShader(self.getShaders("Moon.vertex.shader"),GL_VERTEX_SHADER)
        fragment_shader = compileShader(self.getShaders("Moon.fragment.shader"),GL_FRAGMENT_SHADER)


        """
        The object mode loads the object and return  a list of vertexs by format of 
        vertex3v, texture2d, normal3v
        """
        material = self.scene.materials["Moon"]
        self.vertices = np.array(self.scene.materials["Moon"].vertices,dtype=np.float32)
       
       
        '''
        creating the shaders and attaching with the shaders
        '''
        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program,fragment_shader)
        glLinkProgram(self.program)


        '''
        Generating the buffers
        '''
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER,self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)


        # texture_location = glGetAttribLocation(self.program, "texture")
        # glVertexAttribPointer(texture_location, 2, GL_FLOAT, GL_FALSE,  8*self.vertices.itemsize, ctypes.c_void_p(0))
        # glEnableVertexAttribArray(texture_location)

        # normal_location = glGetAttribLocation(self.program, "normal")
        # glVertexAttribPointer(normal_location, 3, GL_FLOAT, GL_FALSE,  8*self.vertices.itemsize, ctypes.c_void_p(2*ctypes.sizeof(ctypes.c_float)))
        # glEnableVertexAttribArray(normal_location)


        vertex_location = glGetAttribLocation(self.program, "position")
        glVertexAttribPointer(vertex_location, 3, GL_FLOAT, GL_FALSE,  8*self.vertices.itemsize, ctypes.c_void_p(5*ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(vertex_location)

        glUseProgram(self.program)
        translation_location = glGetUniformLocation(self.program, "projection")
        glUniformMatrix4fv(translation_location, 1, GL_FALSE, tr.translationMatrix( 0, -10, 0))

        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
            

    def draw(self):
        
        glUseProgram(self.program)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0,len(self.vertices)//8)
        glBindVertexArray(0)
        


        
        
    
   




