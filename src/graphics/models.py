class WhiteKeyModel:
    def __init__(self, key_size: float = 1):
        self.key_size = key_size
        self.length = self.key_size
        self.width = 0.2 * self.key_size
        self.height = 0.2 * self.key_size
        self.space = 0.01 * self.key_size
        self.key_distance = self.width + self.space
        self.offset_y = self.height


class BlackKeyModel:
    def __init__(self, white_key_model=WhiteKeyModel()):
        self.length = 0.65 * white_key_model.length
        self.width = 0.5 * white_key_model.width
        self.height = 0.5 * white_key_model.height
        self.offset_y = 0.5 * (white_key_model.height + self.height) + white_key_model.offset_y
        self.offset_z = -0.5 * (white_key_model.length - self.length)


class MainPanelModel:
    def __init__(self, white_key_model=WhiteKeyModel(), white_keys_amount: int = 15):
        self.white_key_model = white_key_model
        self.keys_total_width = white_key_model.key_distance * white_keys_amount
        self.width = white_key_model.key_distance * 0 + self.keys_total_width
        self.height = white_key_model.height
        self.depth = 1.05 * white_key_model.length


class BackPanelModel:
    def __init__(self, main_panel_model=MainPanelModel()):
        self.main_panel_model = main_panel_model
        self.width = main_panel_model.width
        self.height = 1.2 * main_panel_model.height + main_panel_model.white_key_model.height
        self.depth = main_panel_model.white_key_model.length

        self.offset_y = 0.5 * (self.height - main_panel_model.height)
        self.offset_z = -0.5 * (main_panel_model.depth + self.depth)


class RightPanelModel:
    def __init__(self, back_panel_model=BackPanelModel()):
        self.back_panel_model = back_panel_model
        self.width = 0.5 * back_panel_model.main_panel_model.white_key_model.width
        self.height = back_panel_model.height
        self.depth = back_panel_model.depth + back_panel_model.main_panel_model.depth
        self.offset_x = 0.5 * (back_panel_model.width + self.width)
        self.offset_y = 0.5 * (self.height - back_panel_model.main_panel_model.height)
        self.offset_z = -0.5 * (self.depth - back_panel_model.main_panel_model.depth)


class LeftPanelModel:
    def __init__(self, right_panel_model=RightPanelModel()):
        self.right_panel_model = right_panel_model
        self.width = 5 * right_panel_model.back_panel_model.main_panel_model.white_key_model.width
        self.height = right_panel_model.height
        self.depth = right_panel_model.depth
        self.offset_x = -0.5 * (right_panel_model.back_panel_model.main_panel_model.width + self.width)
        self.offset_y = right_panel_model.offset_y
        self.offset_z = right_panel_model.offset_z


class PianoModel:
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

        self.keys_total_width = self.white_key_model.key_distance * (self.white_keys_amount - 0.5)
        self.keys_offset_x = 0.5 * self.main_panel_model.width - self.keys_total_width
        self.keys_offset_z = -0.5 * (self.main_panel_model.depth - self.white_key_model.length)

    def calc_white_and_black_keys_amounts(self) -> (int, int):
        black_idx = [1, 3, 6, 8, 10]
        white_count, black_count = 0, 0
        for i in range(self.keys_amount):
            if i % 12 in black_idx:
                black_count += 1
            else:
                white_count += 1
        return white_count, black_count
