import ctypes
import glfw
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Model import Model
import os,time
import numpy as np
import pywavefront as wf
import transformation as tr

class Render:
    def __init__(self):
        self.model =None
        self.vao = None
        self.vbo = None
        self.vertices = None
        self.program = None
        self.ibo = None


    def __init(self):
        """
        Initializing the window using glfw
        """
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        display = (1280,720)
        window = glfw.create_window(display[0], display[1], "Earh Moon Motion", None, None)

        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        glfw.set_window_pos(window, 50, 50)
        glfw.make_context_current(window)

    
        self.model = Model("resource/moon/Moon 2K.obj")
        
        self.model.ready(display[0],display[1])
        glEnable(GL_DEPTH_TEST)
    
        return window

    def __draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.model.draw()
     

    

    def main(self):
        window = self.__init()
        while not glfw.window_should_close(window):
            glfw.poll_events()
            
            self.__draw()
            glfw.swap_buffers(window)
            # time.sleep(0.5)

        glfw.terminate()


        

if __name__ == '__main__':
    Render().main()