from modules.models import PianoModel
from modules.geometries import Cuboid
from modules.element_node import ElementNode


class WhiteKey(Cuboid):
    def __init__(self, element_id: str = 'white_key', piano_model=PianoModel(), shape: str = 'cuboid',
                 color: str = 'white', scale_x: float = 1, scale_y: float = 1, scale_z: float = 1, **kwargs: list):

        self.piano_model = piano_model
        key_width = self.piano_model.white_key_model.width * scale_x
        key_height = self.piano_model.white_key_model.height * scale_y
        key_length = self.piano_model.white_key_model.length * scale_z

        super().__init__(element_id=element_id, shape=shape, color=color, scale_x=key_width, scale_y=key_height,
                         scale_z=key_length, **kwargs)


class BlackKey(Cuboid):
    def __init__(self, element_id: str = 'black_key', piano_model=PianoModel(), shape: str = 'cuboid',
                 color: str = 'black', scale_x: float = 1, scale_y: float = 1, scale_z: float = 1,
                 offset_x: float = 0.0, offset_y: float = 0.0, offset_z: float = 0.0, **kwargs):

        self.piano_model = piano_model
        key_width = self.piano_model.black_key_model.width * scale_x
        key_height = self.piano_model.black_key_model.height * scale_y
        key_length = self.piano_model.black_key_model.length * scale_z

        key_offset_x = offset_x
        key_offset_y = self.piano_model.black_key_model.y_offset + offset_y
        key_offset_z = self.piano_model.black_key_model.z_offset + offset_z

        super().__init__(element_id=element_id, shape=shape, color=color, scale_x=key_width, scale_y=key_height,
                         scale_z=key_length, offset_x=key_offset_x, offset_y=key_offset_y, offset_z=key_offset_z,
                         **kwargs)


class MainPanel(Cuboid):
    def __init__(self, element_id: str = 'main_panel', piano_model=PianoModel(), shape: str = 'cuboid',
                 color: str = 'red', scale_x: float = 1, scale_y: float = 1, scale_z: float = 1, offset_x: float = 0,
                 offset_y: float = 0, offset_z: float = 0, **kwargs):

        self.piano_model = piano_model
        panel_width = self.piano_model.main_panel_model.width * scale_x
        panel_height = self.piano_model.main_panel_model.height * scale_y
        panel_depth = self.piano_model.main_panel_model.depth * scale_z

        panel_offset_x = offset_x
        panel_offset_y = self.piano_model.main_panel_model.y_offset + offset_y
        panel_offset_z = offset_z

        super().__init__(element_id=element_id, shape=shape, color=color, scale_x=panel_width, scale_y=panel_height,
                         scale_z=panel_depth, offset_x=panel_offset_x, offset_y=panel_offset_y, offset_z=panel_offset_z,
                         **kwargs)


class Piano:
    def __init__(self, element_id: str = 'piano', piano_model=PianoModel(), scale_x: float = 1, scale_y: float = 1,
                 scale_z: float = 1, offset_x: float = 0, offset_y: float = 0, offset_z: float = 0):

        self.element_id = element_id
        self.piano_model = piano_model

        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z

        self.main_panel = MainPanel(piano_model=self.piano_model)
        self.keys = self.generate_keys()

    def generate_keys(self) -> list:
        key_distance = self.piano_model.white_key_model.key_distance
        all_keys_offset_x = self.piano_model.keys_offset_x

        keys = []
        white_count = 0

        # create white keys
        for i in range(self.piano_model.keys_amount):
            if i % 12 in [0, 2, 4, 5, 7, 9, 11]:
                offset_x = white_count * key_distance + all_keys_offset_x
                keys.append(WhiteKey(piano_model=self.piano_model, offset_x=offset_x))
                white_count += 1
            else:
                offset_x = (white_count - 0.5) * key_distance + all_keys_offset_x
                keys.append(BlackKey(piano_model=self.piano_model, offset_x=offset_x))

        return keys

    def pre_process(self): ...

    def draw(self):
        self.main_panel.draw()
        for key in self.keys:
            key.draw()
