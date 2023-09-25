from modules.models import PianoModel
from modules.piano import Piano
from modules.transform_node import TransformNode

from modules.geometries import Cuboid
from modules.colors import Gradient8


class SceneElements:
    def __init__(self):
        self.elements = {}
        self.test_piano()
        # self.test_cube()

    def render(self):
        for element in self.elements.values():
            element.node.draw()

    def test_piano(self):
        gradient = Gradient8(['red', 'blue'])
        piano_node = TransformNode(node_id='piano_node', offset_x=0)
        piano = Piano(piano_model=PianoModel(keys_amount=49, key_size=piano_node.scale_x), node=piano_node,
                      gradient=gradient)
        self.elements['piano'] = piano

    def test_cube(self):
        gradient = Gradient8(['red', 'green', 'blue', 'white'])
        colors = gradient.get_cube_z_rotated(amount=4)

        cube_node = TransformNode(node_id='cubeNode', offset_x=0)
        cube = Cuboid(colors=colors, node=cube_node)
        cube_node.element = cube
        self.elements['cube'] = cube
