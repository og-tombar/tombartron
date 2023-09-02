from OpenGL.GL import *


class Light:
    def __init__(self, position=(0, -100, 0, 0)):
        self.position = position

        glLight(GL_LIGHT0, GL_POSITION, self.position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glEnable(GL_DEPTH_TEST)

    def activate(self):
        glLight(GL_LIGHT0, GL_POSITION, self.position)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def deactivate(self):
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)
