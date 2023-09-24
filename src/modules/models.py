class WhiteKeyModel:
    def __init__(self, key_size: float = 1):
        self.key_size = key_size
        self.length = self.key_size
        self.width = self.key_size * 0.2
        self.height = self.key_size * 0.2
        self.space = self.key_size * 0.01
        self.key_distance = self.width + self.space
        self.offset_y = self.height


class BlackKeyModel:
    def __init__(self, white_key_model=WhiteKeyModel()):
        self.length = white_key_model.length * 0.65
        self.width = white_key_model.width * 0.5
        self.height = white_key_model.height * 0.5
        self.offset_y = (white_key_model.height + self.height) / 2 + white_key_model.offset_y
        self.offset_z = -(white_key_model.length - self.length) / 2


class MainPanelModel:
    def __init__(self, white_key_model=WhiteKeyModel(), white_keys_amount: int = 15):
        self.width = white_key_model.key_distance * (white_keys_amount + 5)
        self.height = white_key_model.height
        self.depth = white_key_model.length * 1.5


class PianoModel:
    def __init__(self, keys_amount: int = 25, key_size: float = 1):
        self.keys_amount = keys_amount
        self.white_key_model = WhiteKeyModel(key_size=key_size)
        self.black_key_model = BlackKeyModel(white_key_model=self.white_key_model)
        self.white_keys_amount, black_keys_amount = self.calc_white_and_black_keys_amounts()

        self.keys_total_length = self.white_key_model.key_distance * self.white_keys_amount
        self.keys_offset_x = -0.5 * self.white_key_model.key_distance * (self.white_keys_amount - 1)
        self.main_panel_model = MainPanelModel(white_key_model=self.white_key_model,
                                               white_keys_amount=self.white_keys_amount)

    def calc_white_and_black_keys_amounts(self) -> (int, int):
        black_idx = [1, 3, 6, 8, 10]
        white_count, black_count = 0, 0
        for i in range(self.keys_amount):
            if i % 12 in black_idx:
                black_count += 1
            else:
                white_count += 1
        return white_count, black_count
