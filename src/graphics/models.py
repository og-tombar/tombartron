import numpy as np


class WhiteKeyModel:
    def __init__(self, key_size: float = 1):
        scale_x = 0.2 * key_size
        scale_y = 0.2 * key_size
        scale_z = key_size
        self.scale = np.array([scale_x, scale_y, scale_z])
        self.space = 0.01 * key_size
        self.key_distance = scale_x + self.space

        offset_y = scale_y
        self.offset = np.array([0, offset_y, 0])


class BlackKeyModel:
    def __init__(self, white_key_model=WhiteKeyModel()):
        scale_x = 0.5 * white_key_model.scale[0]
        scale_y = 0.5 * white_key_model.scale[1]
        scale_z = 0.65 * white_key_model.scale[2]
        self.scale = np.array([scale_x, scale_y, scale_z])

        offset_y = 0.5 * (self.scale[1] + white_key_model.scale[1]) + white_key_model.offset[1]
        offset_z = -0.5 * (white_key_model.scale[2] - self.scale[2])
        self.offset = np.array([0, offset_y, offset_z])


class MainPanelModel:
    def __init__(self, white_key_model=WhiteKeyModel(), white_keys_amount: int = 15):
        self.white_key_model = white_key_model
        scale_x = white_key_model.key_distance * white_keys_amount
        scale_y = white_key_model.scale[1]
        scale_z = white_key_model.scale[2] * 1.05
        self.scale = np.array([scale_x, scale_y, scale_z])


class BackPanelModel:
    def __init__(self, main_panel_model=MainPanelModel()):
        self.main_panel_model = main_panel_model

        scale_x = main_panel_model.scale[0]
        scale_y = 1.2 * main_panel_model.scale[1] + main_panel_model.white_key_model.scale[1]
        scale_z = main_panel_model.white_key_model.scale[2]
        self.scale = np.array([scale_x, scale_y, scale_z])

        offset_y = 0.5 * (self.scale[1] - main_panel_model.scale[1])
        offset_z = -0.5 * (main_panel_model.scale[2] + self.scale[2])
        self.offset = np.array([0, offset_y, offset_z])


class RightPanelModel:
    def __init__(self, back_panel_model=BackPanelModel()):
        self.back_panel_model = back_panel_model
        scale_x = 0.5 * back_panel_model.main_panel_model.white_key_model.scale[0]
        scale_y = back_panel_model.scale[1]
        scale_z = back_panel_model.scale[2] + back_panel_model.main_panel_model.scale[2]
        self.scale = np.array([scale_x, scale_y, scale_z])

        offset_x = 0.5 * (back_panel_model.scale[0] + self.scale[0])
        offset_y = 0.5 * (self.scale[1] - back_panel_model.main_panel_model.scale[1])
        offset_z = -0.5 * (self.scale[2] - back_panel_model.main_panel_model.scale[2])
        self.offset = np.array([offset_x, offset_y, offset_z])


class LeftPanelModel:
    def __init__(self, right_panel_model=RightPanelModel()):
        self.right_panel_model = right_panel_model
        scale_x = 5 * right_panel_model.back_panel_model.main_panel_model.white_key_model.scale[0]
        scale_y = right_panel_model.scale[1]
        scale_z = right_panel_model.scale[2]
        self.scale = np.array([scale_x, scale_y, scale_z])

        offset_x = -0.5 * (right_panel_model.back_panel_model.main_panel_model.scale[0] + self.scale[0])
        offset_y = right_panel_model.offset[1]
        offset_z = right_panel_model.offset[2]
        self. offset = np.array([offset_x, offset_y, offset_z])


class KeyboardModel:
    def __init__(self, keys_amount: int = 25, key_size: float = 1):
        self.keys_amount = keys_amount
        self.white_key_model = WhiteKeyModel(key_size=key_size)
        self.black_key_model = BlackKeyModel(white_key_model=self.white_key_model)
        self.white_keys_amount, black_keys_amount = self.calc_white_and_black_keys_amounts()
        self.main_panel_model = MainPanelModel(white_key_model=self.white_key_model,
                                               white_keys_amount=self.white_keys_amount)

        self.back_panel_model = BackPanelModel(main_panel_model=self.main_panel_model)
        self.right_panel_model = RightPanelModel(back_panel_model=self.back_panel_model)
        self.left_panel_model = LeftPanelModel(right_panel_model=self.right_panel_model)

        # TODO: WITH DIFFERENT MAIN_PANEL.SCALE_Y THIS DOES NOT WORK
        self.keys_offset = -0.5 * (self.main_panel_model.scale - self.white_key_model.scale)

    def calc_white_and_black_keys_amounts(self) -> (int, int):
        black_idx = [1, 3, 6, 8, 10]
        white_count, black_count = 0, 0
        for i in range(self.keys_amount):
            if i % 12 in black_idx:
                black_count += 1
            else:
                white_count += 1
        return white_count, black_count
