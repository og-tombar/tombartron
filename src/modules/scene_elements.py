from OpenGL.GL import *

from modules.models import PianoModel
from modules.piano import Piano


class SceneElements:
    def __init__(self):
        self.elements = {'piano': Piano(piano_model=PianoModel(keys_amount=49))}

    def render(self):
        for element in self.elements.values():
            glPushMatrix()
            element.pre_process()
            element.draw()
            glPopMatrix()
