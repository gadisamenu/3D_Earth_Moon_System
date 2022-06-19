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
from camera import Camera


class Render:
    def __init__(self):
        self.models =None
        self.camera = None
        self.width_height = (1280,720)
       
    def __init(self):
        """
        Initializing the window using glfw
        """
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        self.camera = Camera(self.width_height[0] // 2, self.width_height[1] // 2)
        window = glfw.create_window(self.width_height[0], self.width_height[1], "Earth Moon Motion", None, None)

        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        glfw.set_window_pos(window, 50, 50)
        glfw.set_cursor_pos_callback(window, self.mouse_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        glfw.set_key_callback(window, self.keyboard_callback)
        glfw.make_context_current(window)

        
        self.models = {"Earth":Model("resource/Earth/Simple Earth/earth.obj",["resource/Earth/Simple Earth/images/0_Tierra1.jpg", "resource/Earth/Simple Earth/images/1_Tierra1 (Nubes).jpg"]),
                        "Moon":Model("resource/moon/Moon 2K.obj",["resource/moon/Textures/Diffuse_2K.png", "resource/moon/Textures/Bump_2K.png"])
        }
    
        for model in self.models:
            self.models[model].ready()

        glEnable(GL_DEPTH_TEST)

        return window
    def mouse_callback(self, window, xpos, ypos):
        xoffset = xpos - self.camera.lastX
        yoffset = self.camera.lastY - ypos

        self.camera.lastX = xpos
        self.camera.lastY = ypos

        self.camera.mouseProcess(xoffset, yoffset)
    def scroll_callback(self,window, xoffset, yoffset):
        self.camera.fov -= self.camera.sensitivity * yoffset
        if self.camera.fov < 1.0: self.camera.fov = 1.0
        if self.camera.fov > 45.0: self.camera.fov = 45.0
    def keyboard_callback(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_UP or key == glfw.KEY_W:
            self.camera.keyboardProcess("FORWARD", [0.0,0.0,1.0])
        elif key == glfw.KEY_DOWN or key == glfw.KEY_S:
            self.camera.keyboardProcess("BACKWARD", [0.0,0.0,1.0])
        elif key == glfw.KEY_UP or key == glfw.KEY_A:
            self.camera.keyboardProcess("LEFT", [1.0,0.0,0.0])
        elif key == glfw.KEY_UP or key == glfw.KEY_D:
            self.camera.keyboardProcess("RIGHT", [1.0,0.0,0.0])



    def __draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        scale = pyrr.matrix44.create_from_scale(np.array([2.0,2.0,2.0],dtype=np.float32))
        translation = pyrr.matrix44.create_from_translation(np.array([0,0,0],dtype=np.float32))
        temp = pyrr.matrix44.multiply(scale, translation)
        temp2 = pyrr.matrix44.multiply(temp,pyrr.matrix44.create_from_y_rotation(glfw.get_time() * 0.25))
        model = pyrr.matrix44.multiply(temp2, pyrr.matrix44.create_from_z_rotation(23.5 * np.pi / 180.0))
        projection = pyrr.matrix44.create_perspective_projection_matrix(np.rad2deg(self.camera.fov),  self.width_height[0]/ self.width_height[1], 1, 500,dtype=np.float32)
        view = self.camera.getViewMatrix()

        self.models["Earth"].set_transformation(model, view, projection)
  
        
        self.models["Earth"].draw()  

        scale = pyrr.matrix44.create_from_scale(np.array([0.5,0.5,0.5],dtype=np.float32))
        translation = pyrr.matrix44.create_from_translation(np.array([5,0,0],dtype=np.float32))
        rotation = pyrr.matrix44.create_from_y_rotation(0.5* glfw.get_time())
        temp = pyrr.matrix44.multiply(scale, translation)
        model = pyrr.matrix44.multiply(temp,pyrr.matrix44.create_from_axis_rotation(np.array([-np.tan(5*np.pi/180.0), 1.0, 0.0]), theta=1.0 * glfw.get_time()))


        self.models["Moon"].set_transformation(model, view, projection)
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