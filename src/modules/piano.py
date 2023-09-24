from modules.models import PianoModel
from modules.geometries import Cuboid
from modules.transform_node import TransformNode


class WhiteKey(Cuboid):
    def __init__(self, element_id: str = 'white_key', piano_model=PianoModel(), color: str = 'white',
                 node: TransformNode = TransformNode()):
        self.piano_model = piano_model
        self.node = node
        self.node.offset_y += self.piano_model.white_key_model.offset_y
        self.node.scale_x *= self.piano_model.white_key_model.width
        self.node.scale_y *= self.piano_model.white_key_model.height
        self.node.scale_z *= self.piano_model.white_key_model.length
        super().__init__(element_id=element_id, color=color, node=node)


class BlackKey(Cuboid):
    def __init__(self, element_id: str = 'black_key', piano_model=PianoModel(), color: str = 'black',
                 node: TransformNode = TransformNode()):
        self.piano_model = piano_model
        self.node = node
        self.node.offset_y += self.piano_model.black_key_model.offset_y
        self.node.offset_z += self.piano_model.black_key_model.offset_z
        self.node.scale_x *= self.piano_model.black_key_model.width
        self.node.scale_y *= self.piano_model.black_key_model.height
        self.node.scale_z *= self.piano_model.black_key_model.length
        super().__init__(element_id=element_id, color=color, node=node)


class MainPanel(Cuboid):
    def __init__(self, element_id: str = 'main_panel', piano_model=PianoModel(), color: str = 'red',
                 node: TransformNode = TransformNode()):
        self.piano_model = piano_model
        self.node = node
        self.node.scale_x *= self.piano_model.main_panel_model.width
        self.node.scale_y *= self.piano_model.main_panel_model.height
        self.node.scale_z *= self.piano_model.main_panel_model.depth
        super().__init__(element_id=element_id, color=color, node=node)


# consider making Piano inherit TransformNode instead of having one as an attribute?
class Piano:
    def __init__(self, element_id: str = 'piano', piano_model=PianoModel(), color: str = 'red',
                 node: TransformNode = TransformNode()):
        self.element_id = element_id
        self.piano_model = piano_model
        self.color = color

        main_panel_node = TransformNode(node_id='main_panel_node')
        main_panel_node.element = MainPanel(piano_model=piano_model, color=color, node=main_panel_node)

        self.node = node
        self.node.add_child(child_node=main_panel_node)
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

    def pre_process(self) -> None:
        self.node.pre_process()

    def draw(self) -> None:
        print(self.node)
