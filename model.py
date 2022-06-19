import numpy as np
import pywavefront as pw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys ,time,os
import pyrr, glfw
from OpenGL.GL.shaders import compileProgram, compileShader
from  texture import load_texture

class Model:
    def __init__(self,file_path:str,texture_path:list):
        self.texture_path = texture_path
        self.path = file_path
        self.scene = None     
        self.vao = None
        self.vbo = None
        self.vertices = None
        self.program = None
        self.texture = None
        self.model = None
        self.view = None
        self.projection =  None
        
        
    def load_model(self):
        try:
            self.scene = pw.Wavefront(self.path, collect_faces= True)
            pw.wavefront
        except:
            print("model loading failed")

    def getShaders(self,filename):
        p = os.path.join(os.getcwd(), "shaders", filename)
        return open(p, 'r').read()

    def ready(self):
       
        self.load_model()
                
        """
        The object mode loads the object and return  a list of vertexs by format of 
        vertex3v, texture2d, normal3v
        """
        # print(self.scene)
        for name,  material in self.scene.materials.items():
            self.vertices = np.array(self.scene.materials[name].vertices,dtype=np.float32)
            break

        # glActiveTexture(0)
        '''
        creating the shaders and attaching with the shaders
        '''
        self.program =  compileProgram(compileShader(self.getShaders("vertex.shader"),GL_VERTEX_SHADER), compileShader(self.getShaders("fragment.shader"),GL_FRAGMENT_SHADER))

        '''
        Generating the buffers
        '''
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.texture = glGenTextures(2)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER,self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

         
        texture_location = glGetAttribLocation(self.program, "texture")
        glVertexAttribPointer(texture_location, 2, GL_FLOAT, GL_FALSE,  8*self.vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(texture_location)

       

        vertex_location = glGetAttribLocation(self.program, "position")
        glVertexAttribPointer(vertex_location, 3, GL_FLOAT, GL_FALSE, 8*self.vertices.itemsize, ctypes.c_void_p(5*self.vertices.itemsize))
        glEnableVertexAttribArray(vertex_location)


        glUseProgram(self.program)


        load_texture(self.texture_path[0], GL_TEXTURE0, self.texture[0])
        load_texture(self.texture_path[1], GL_TEXTURE1, self.texture[1])

        earthTexLocation = glGetUniformLocation(self.program, 'earthTex')
        print(earthTexLocation)
        glUniform1i(earthTexLocation, 0)

        cloudTexLocation = glGetUniformLocation(self.program, 'cloudTex')
        glUniform1i(cloudTexLocation, 1)
        print(cloudTexLocation)


        
        

        glBindVertexArray(0)
    def set_transformation(self,model, view, projection):
        self.model = model
        self.view = view
        self.projection = projection
        

    def draw(self):
        model_location = glGetUniformLocation(self.program, 'model')
        view_location = glGetUniformLocation(self.program, "view")
        projection_location = glGetUniformLocation(self.program, "projection")

        glUniformMatrix4fv(projection_location, 1, GL_FALSE,self.projection)
        glUniformMatrix4fv(model_location, 1, GL_FALSE, self.model)
        glUniformMatrix4fv(view_location, 1, GL_FALSE, self.view)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture[0])

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture[1])

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0,len(self.vertices)//8)
        glBindVertexArray(0)
        


   



