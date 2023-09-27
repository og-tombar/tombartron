from graphics.models import KeyboardModel
from graphics.keyboard import Keyboard
from graphics.transform_node import TransformNode
from graphics.geometry import Cuboid
from graphics.colors import Gradient8


class SceneElements:
    def __init__(self):
        self.elements = {}
        self.test_keyboard()
        # self.test_cube()

    def render(self):
        for element in self.elements.values():
            element.node.draw()

    def test_keyboard(self):
        gradient = Gradient8(['red', 'blue'])
        keyboard_node = TransformNode(node_id='keyboard_node')
        keyboard = Keyboard(keyboard_model=KeyboardModel(keys_amount=49, key_size=keyboard_node.scale[0]),
                            node=keyboard_node, gradient=gradient)
        self.elements['keyboard'] = keyboard

    def test_cube(self):
        gradient = Gradient8(['red', 'green', 'blue', 'white'])
        colors = gradient.get_cube_z_rotated()

        cube_node = TransformNode(node_id='cubeNode', offset=[0, -5, 0])
        cube = Cuboid(colors=colors, node=cube_node)
        cube_node.element = cube
        self.elements['cube'] = cube
