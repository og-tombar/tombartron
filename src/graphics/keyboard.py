import numpy as np

from graphics.models import KeyboardModel
from graphics.geometry import Cuboid
from graphics.transform_node import TransformNode
from graphics.colors import Gradient8


class WhiteKey(Cuboid):
    def __init__(self, element_id: str = 'white_key', keyboard_model=KeyboardModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['white'] * 8 if colors is None else colors
        self.keyboard_model = keyboard_model
        self.node = node
        self.node.offset += self.keyboard_model.white_key_model.offset + self.keyboard_model.keys_offset
        self.node.scale *= self.keyboard_model.white_key_model.scale
        super().__init__(element_id=element_id, colors=colors, node=node)


class BlackKey(Cuboid):
    def __init__(self, element_id: str = 'black_key', keyboard_model=KeyboardModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['black'] * 8 if colors is None else colors
        self.keyboard_model = keyboard_model
        self.node = node
        self.node.offset += self.keyboard_model.black_key_model.offset + self.keyboard_model.keys_offset
        self.node.scale *= self.keyboard_model.black_key_model.scale
        super().__init__(element_id=element_id, colors=colors, node=node)


class MainPanel(Cuboid):
    def __init__(self, element_id: str = 'main_panel', keyboard_model=KeyboardModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.keyboard_model = keyboard_model
        self.node = node
        self.node.scale *= self.keyboard_model.main_panel_model.scale
        super().__init__(element_id=element_id, colors=colors, node=node)


class BackPanel(Cuboid):
    def __init__(self, element_id: str = 'left_panel', keyboard_model=KeyboardModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.keyboard_model = keyboard_model
        self.node = node
        self.node.offset += self.keyboard_model.back_panel_model.offset
        self.node.scale *= self.keyboard_model.back_panel_model.scale
        super().__init__(element_id=element_id, colors=colors, node=node)


class RightPanel(Cuboid):
    def __init__(self, element_id: str = 'right_panel', keyboard_model=KeyboardModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.keyboard_model = keyboard_model
        self.node = node
        self.node.offset += self.keyboard_model.right_panel_model.offset
        self.node.scale = self.keyboard_model.right_panel_model.scale
        super().__init__(element_id=element_id, colors=colors, node=node)


class LeftPanel(Cuboid):
    def __init__(self, element_id: str = 'left_panel', keyboard_model=KeyboardModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.keyboard_model = keyboard_model
        self.node = node
        self.node.offset += self.keyboard_model.left_panel_model.offset
        self.node.scale *= self.keyboard_model.left_panel_model.scale
        super().__init__(element_id=element_id, colors=colors, node=node)


# consider making keyboard inherit TransformNode instead of having one as an attribute?
class Keyboard:
    def __init__(self, element_id: str = 'keyboard', keyboard_model=KeyboardModel(), gradient: Gradient8 = Gradient8(),
                 node: TransformNode = TransformNode()):
        self.element_id = element_id
        self.keyboard_model = keyboard_model
        self.gradient = gradient
        self.node = node

        main_panel_node = TransformNode(node_id='main_panel_node')
        main_panel_node.element = MainPanel(keyboard_model=keyboard_model, colors=gradient.colors, node=main_panel_node)
        self.node.add_child(child_node=main_panel_node)

        back_panel_node = TransformNode(node_id='back_panel_node')
        back_panel_node.element = BackPanel(keyboard_model=keyboard_model, colors=gradient.colors, node=back_panel_node)
        self.node.add_child(child_node=back_panel_node)

        right_panel_node = TransformNode(node_id='right_panel_node')
        right_panel_colors = 8 * [self.gradient.colors[1]]
        right_panel_node.element = RightPanel(keyboard_model=keyboard_model, colors=right_panel_colors,
                                              node=right_panel_node)
        self.node.add_child(child_node=right_panel_node)

        left_panel_node = TransformNode(node_id='left_panel_node')
        left_panel_colors = self.gradient.get_cube_z_rotated(amount=2)
        left_panel_node.element = LeftPanel(keyboard_model=keyboard_model, colors=left_panel_colors,
                                            node=left_panel_node)
        self.node.add_child(child_node=left_panel_node)

        self.generate_keys()

    def generate_keys(self) -> None:
        key_distance = self.keyboard_model.white_key_model.key_distance

        white_count = 0
        keys_node = TransformNode(node_id='keys_node')
        self.node.add_child(keys_node)

        # for every key, the node_id is its midi note number
        for i in range(self.keyboard_model.keys_amount):
            if i % 12 in [0, 2, 4, 5, 7, 9, 11]:
                # create white key
                node_offset_x = white_count * key_distance
                node_offset = np.array([node_offset_x, 0.0, 0.0])
                node = TransformNode(node_id=i, offset=node_offset)
                node.element = WhiteKey(keyboard_model=self.keyboard_model, node=node)
                keys_node.add_child(child_node=node)
                white_count += 1
            else:
                # create black key
                node_offset_x = (white_count - 0.5) * key_distance
                node_offset = np.array([node_offset_x, 0.0, 0.0])
                node = TransformNode(node_id=i, offset=node_offset)
                node.element = BlackKey(keyboard_model=self.keyboard_model, node=node)
                keys_node.add_child(child_node=node)

    def draw(self) -> None: ...
