import glfw
from OpenGL.GL import *
import os


def getShaders(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()

def init():
    if not glfw.init():
        raise Exception("glfw can not be initialized!")


    window = glfw.create_window(1280, 720, "Earth", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    glfw.set_window_pos(window, 50, 50)

    glfw.make_context_current(window)


    return window

def draw():
    pass

def main():
    window = init()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        draw()

        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == '__main__':
    main()