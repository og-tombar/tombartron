from OpenGL.GL import *

from modules.piano import WhiteKey, Piano


class SceneElements:
    def __init__(self):
        self.elements = {}
        self.create_piano()

    def render(self):
        for element in self.elements.values():
            glPushMatrix()
            element.pre_process()
            element.draw()
            glPopMatrix()

    def create_piano(self):
        self.elements['piano'] = Piano()
        for i in range(7):
            self.elements[f'key{i}'] = WhiteKey(offset={'x': -1 + i * 0.21})
