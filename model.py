import numpy as np
import pywavefront as pw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys ,time,os
import pyrr, glfw
import transformation as tr
from OpenGL.GL.shaders import compileProgram, compileShader
from  texture import load_texture

class Model:
    def __init__(self,file_path:str):
        self.path = file_path
        self.scene = None     
        self.vao = None
        self.vbo = None
        self.vertices = None
        self.program = None
        self.texture = None
        self.model = pyrr.matrix44.create_from_translation(np.array([0,0,0]))
        
        
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
                
        """
        The object mode loads the object and return  a list of vertexs by format of 
        vertex3v, texture2d, normal3v
        """
        # print(self.scene)
        for name,  material in self.scene.materials.items():
            self.vertices = np.array(self.scene.materials[name].vertices,dtype=np.float32)
            break


       
        '''
        creating the shaders and attaching with the shaders
        '''
        self.program =  compileProgram(compileShader(self.getShaders("vertex.shader"),GL_VERTEX_SHADER), compileShader(self.getShaders("fragment.shader"),GL_FRAGMENT_SHADER))

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
        glVertexAttribPointer(vertex_location, 3, GL_FLOAT, GL_FALSE, 8*self.vertices.itemsize, ctypes.c_void_p(5*self.vertices.itemsize))
        glEnableVertexAttribArray(vertex_location)


        glUseProgram(self.program)
        projection_location = glGetUniformLocation(self.program, "projection")
        view_location = glGetUniformLocation(self.program, "view")
        model_location = glGetUniformLocation(self.program, 'model')

        glUniformMatrix4fv(projection_location, 1, GL_FALSE, pyrr.matrix44.create_perspective_projection_matrix(45, w_width / w_height, 1, 500,dtype=np.float32))
        glUniformMatrix4fv(view_location, 1, GL_FALSE, pyrr.matrix44.create_look_at(np.array([0.0,10.0,10.0]),np.array([0.0,0.0,0.0]) , np.array([0.0,1.0,0.0])))
        glUniformMatrix4fv(model_location, 1, GL_FALSE, self.model)



    def set_mode(self,model):
        self.model = model

    def draw(self):
        glUseProgram(self.program)
        glBindVertexArray(self.vao)
        model_location = glGetUniformLocation(self.program, 'model')
        glUniformMatrix4fv(model_location, 1, GL_FALSE, self.model)
        glDrawArrays(GL_TRIANGLES, 0,len(self.vertices)//8)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
        


   




