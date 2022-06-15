import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
from Model import Model

scene = pywavefront.Wavefront('resource/moon/Moon 2K.obj', collect_faces=True, create_materials= True)
# print(scene.materials.items())
# for m in scene:
#     print(m)
# for name, material in scene.materials.items():
#     print(name)
#     # Contains the vertex format (string) such as "T2F_N3F_V3F"
#     # T2F, C3F, N3F and V3F may appear in this string
#     print(material.vertex_format)
#     # Contains the vertex list of floats in the format described above
#     # print(material.vertices[:20])
#     # Material properties
#     print(material.diffuse)
#     print(material.ambient)
#     print(material.texture)
    # ..

# for mesh in scene.mesh_list:
#         for face in mesh.faces:
#             print(face)
            # for vertex_i in face:
            
# print(scene.mesh_list[0])


scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)

        

scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)
scaled_size    = 5
scene_scale    = [scaled_size/max_scene_size for i in range(3)]
scene_trans    = [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)]
vertices = []

for mesh in scene.mesh_list:
        for face in mesh.faces:
            for vertex_i in face:
                for m in scene.vertices[vertex_i]:
                    # print(m)
                    vertices.append(m)


def Model_():
    glPushMatrix()
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)

    for mesh in scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*scene.vertices[vertex_i])
        glEnd()

    glPopMatrix()
# print(vertices)
# model = Model("resource/moon/Moon 2K.obj")
# display = (1212,2323)
# model.ready(display[0],display[1])

# print(model.materials["Moon"].vertices  == vertices)

def main():
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 1, 500.0)
        glTranslatef(0.0, 0.0, -10)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        glTranslatef(-0.5,0,0)
                    if event.key == pygame.K_RIGHT:
                        glTranslatef(0.5,0,0)
                    if event.key == pygame.K_UP:
                        glTranslatef(0,1,0)
                    if event.key == pygame.K_DOWN:
                        glTranslatef(0,-1,0)

            # glRotatef(1, 5, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            Model_()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            pygame.display.flip()
            pygame.time.wait(10)

main()