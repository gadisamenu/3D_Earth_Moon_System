import ctypes
import glfw
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from model import Model
import os,time,pyrr
import numpy as np
import pywavefront as wf
import transformation as tr


class Render:
    def __init__(self):
        self.models =None
       
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

        
        self.models = {"Earth":Model("resource/Earth/Simple Earth/earth.obj"),
        "Moon":Model("resource/moon/Moon 2K.obj")
        }
    
        for model in self.models:
            self.models[model].ready(display[0],display[1])


        glEnable(GL_DEPTH_TEST)

        return window

    def __draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        scale = pyrr.matrix44.create_from_scale(np.array([1.5,1.5,1.5],dtype=np.float32))
        translation = pyrr.matrix44.create_from_translation(np.array([0,0,0],dtype=np.float32))
        model = pyrr.matrix44.multiply(scale, translation)
        self.models["Earth"].set_mode(model)
  
        
        self.models["Earth"].draw()  

        scale = pyrr.matrix44.create_from_scale(np.array([0.5,0.5,0.5],dtype=np.float32))
        translation = pyrr.matrix44.create_from_translation(np.array([5,0,0],dtype=np.float32))
        rotation = pyrr.matrix44.create_from_y_rotation(0.5* glfw.get_time())
        model = pyrr.matrix44.multiply(scale, translation)

        
        self.models["Moon"].set_mode(model)
        self.models["Moon"].draw() 

    

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