from modules.models import WhiteKeyModel
from modules.shapes import Cuboid
from modules.cluster import Cluster


class WhiteKey(Cuboid):
    def __init__(self, element_id='white_key', shape='cuboid', **kwargs):
        width = WhiteKeyModel.WIDTH
        height = WhiteKeyModel.HEIGHT
        length = WhiteKeyModel.LENGTH
        super().__init__(element_id=element_id, shape=shape, **kwargs, scale={'x': width, 'y': height, 'z': length})


class Piano(Cluster):
    def __init__(self):
        super().__init__()
        for i in range(20):
            key = WhiteKey(offset={'x': -1 + i * 0.21})
            self.elements[f'key{i}'] = key



