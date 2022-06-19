from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians


class Camera:
    def __init__(self, lastX, lastY) -> None:
        self.cameraPos = Vector3([0.0, 0.0, 10.0])
        self.cameraUp = Vector3([0.0, 1.0, 0.0])
        self.cameraFront = Vector3([0.0, 0.0, 0.0])
        self.cameraRight = Vector3([1.0, 0.0, 0.0])



        self.lastX = lastX
        self.lastY = lastY
        self.fov = radians(45)
        self.yaw = -90
        self.pitch = 0
        self.sensitivity = 0.3
    def getViewMatrix(self):
        return matrix44.create_look_at(self.cameraPos,self.cameraFront, self.cameraUp)
    def mouseProcess(self, xoffset, yoffset):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 45:
            self.pitch = 45
        if self.pitch < -45:
            self.pitch = -45
        self.moveCamera()
        
        
    def moveCamera(self):
        direction = Vector3([0.0, 0.0, 0.0])

        direction.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        direction.y = sin(radians(self.pitch)) 
        direction.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.cameraFront = vector.normalize(direction)
        self.cameraRight = vector.normalise(vector3.cross(self.cameraFront, Vector3([0.0, 1.0, 0.0])))
        self.cameraUp = vector.normalise(vector3.cross(self.cameraRight, self.cameraFront))

    def keyboardProcess(self, direction, velocity):
        if direction == "FORWARD":
            self.cameraPos += self.cameraFront * velocity
        if direction == "BACKWARD":
            self.cameraPos -=  self.cameraFront * velocity
        if direction == "LEFT":
            self.cameraPos -=  self.cameraRight * velocity
        if direction == "RIGHT":
            self.cameraPos += self.cameraRight * velocity
        


        
