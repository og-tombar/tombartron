from modules.models import PianoModel
from modules.piano import Piano
from modules.transform_node import TransformNode


class SceneElements:
    def __init__(self):
        self.elements = {}

        piano_node = TransformNode(node_id='piano_node')
        piano = Piano(piano_model=PianoModel(keys_amount=49, key_size=piano_node.scale_x), node=piano_node)
        self.elements['piano'] = piano

    def render(self):
        for element in self.elements.values():
            element.node.draw()
