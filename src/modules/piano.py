from graphics.models import PianoModel
from graphics.geometries import Cuboid
from modules.transform_node import TransformNode
from graphics.colors import Gradient8


class WhiteKey(Cuboid):
    def __init__(self, element_id: str = 'white_key', piano_model=PianoModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['white'] * 8 if colors is None else colors
        self.piano_model = piano_model
        self.node = node
        self.node.offset_y += self.piano_model.white_key_model.offset_y
        self.node.offset_z += self.piano_model.keys_offset_z
        self.node.scale_x *= self.piano_model.white_key_model.width
        self.node.scale_y *= self.piano_model.white_key_model.height
        self.node.scale_z *= self.piano_model.white_key_model.length
        super().__init__(element_id=element_id, colors=colors, node=node)


class BlackKey(Cuboid):
    def __init__(self, element_id: str = 'black_key', piano_model=PianoModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['black'] * 8 if colors is None else colors
        self.piano_model = piano_model
        self.node = node
        self.node.offset_y += self.piano_model.black_key_model.offset_y
        self.node.offset_z += self.piano_model.black_key_model.offset_z + self.piano_model.keys_offset_z
        self.node.scale_x *= self.piano_model.black_key_model.width
        self.node.scale_y *= self.piano_model.black_key_model.height
        self.node.scale_z *= self.piano_model.black_key_model.length
        super().__init__(element_id=element_id, colors=colors, node=node)


class MainPanel(Cuboid):
    def __init__(self, element_id: str = 'main_panel', piano_model=PianoModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.piano_model = piano_model
        self.node = node
        self.node.scale_x *= self.piano_model.main_panel_model.width
        self.node.scale_y *= self.piano_model.main_panel_model.height
        self.node.scale_z *= self.piano_model.main_panel_model.depth
        super().__init__(element_id=element_id, colors=colors, node=node)


class BackPanel(Cuboid):
    def __init__(self, element_id: str = 'left_panel', piano_model=PianoModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.piano_model = piano_model
        self.node = node
        self.node.offset_y += self.piano_model.back_panel_model.offset_y
        self.node.offset_z += self.piano_model.back_panel_model.offset_z
        self.node.scale_x *= self.piano_model.back_panel_model.width
        self.node.scale_y *= self.piano_model.back_panel_model.height
        self.node.scale_z *= self.piano_model.back_panel_model.depth
        super().__init__(element_id=element_id, colors=colors, node=node)


class RightPanel(Cuboid):
    def __init__(self, element_id: str = 'right_panel', piano_model=PianoModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.piano_model = piano_model
        self.node = node
        self.node.offset_x += self.piano_model.right_panel_model.offset_x
        self.node.offset_y += self.piano_model.right_panel_model.offset_y
        self.node.offset_z += self.piano_model.right_panel_model.offset_z
        self.node.scale_x *= self.piano_model.right_panel_model.width
        self.node.scale_y *= self.piano_model.right_panel_model.height
        self.node.scale_z *= self.piano_model.right_panel_model.depth
        super().__init__(element_id=element_id, colors=colors, node=node)


class LeftPanel(Cuboid):
    def __init__(self, element_id: str = 'left_panel', piano_model=PianoModel(), colors: list[str] = None,
                 node: TransformNode = TransformNode()):
        colors = ['red'] * 8 if colors is None else colors
        self.piano_model = piano_model
        self.node = node
        self.node.offset_x += self.piano_model.left_panel_model.offset_x
        self.node.offset_y += self.piano_model.left_panel_model.offset_y
        self.node.offset_z += self.piano_model.left_panel_model.offset_z
        self.node.scale_x *= self.piano_model.left_panel_model.width
        self.node.scale_y *= self.piano_model.left_panel_model.height
        self.node.scale_z *= self.piano_model.left_panel_model.depth
        super().__init__(element_id=element_id, colors=colors, node=node)


# consider making Piano inherit TransformNode instead of having one as an attribute?
class Piano:
    def __init__(self, element_id: str = 'piano', piano_model=PianoModel(), gradient: Gradient8 = Gradient8(),
                 node: TransformNode = TransformNode()):
        self.element_id = element_id
        self.piano_model = piano_model
        self.gradient = gradient
        self.node = node

        main_panel_node = TransformNode(node_id='main_panel_node')
        main_panel_node.element = MainPanel(piano_model=piano_model, colors=gradient.colors, node=main_panel_node)
        self.node.add_child(child_node=main_panel_node)

        back_panel_node = TransformNode(node_id='back_panel_node')
        back_panel_node.element = BackPanel(piano_model=piano_model, colors=gradient.colors, node=back_panel_node)
        self.node.add_child(child_node=back_panel_node)

        right_panel_node = TransformNode(node_id='right_panel_node')
        right_panel_colors = 8 * [self.gradient.colors[1]]
        right_panel_node.element = RightPanel(piano_model=piano_model, colors=right_panel_colors, node=right_panel_node)
        self.node.add_child(child_node=right_panel_node)

        left_panel_node = TransformNode(node_id='left_panel_node')
        left_panel_colors = self.gradient.get_cube_z_rotated(amount=2)
        left_panel_node.element = LeftPanel(piano_model=piano_model, colors=left_panel_colors, node=left_panel_node)
        self.node.add_child(child_node=left_panel_node)

        self.generate_keys()

    def generate_keys(self) -> None:
        key_distance = self.piano_model.white_key_model.key_distance
        all_keys_offset_x = self.piano_model.keys_offset_x

        white_count = 0
        keys_node = TransformNode(node_id='keys_node')
        self.node.add_child(keys_node)

        # for every key, the node_id is its midi note number
        for i in range(self.piano_model.keys_amount):
            if i % 12 in [0, 2, 4, 5, 7, 9, 11]:
                # create white key
                offset_x = white_count * key_distance + all_keys_offset_x
                node = TransformNode(node_id=i, offset_x=offset_x)
                node.element = WhiteKey(piano_model=self.piano_model, node=node)
                keys_node.add_child(child_node=node)
                white_count += 1
            else:
                # create black key
                offset_x = (white_count - 0.5) * key_distance + all_keys_offset_x
                node = TransformNode(node_id=i, offset_x=offset_x)
                node.element = BlackKey(piano_model=self.piano_model, node=node)
                keys_node.add_child(child_node=node)

    def draw(self) -> None: ...
