import math
from typing import List

from OpenGL.GL import *

from modules.color import colors
from modules.other_utils import *


class Polygon:
    def __init__(self, element_id='polygon', shape='polygon', offset=None, scale=None, vertices=None):
        self.element_id = element_id
        self.shape = shape

        # offset and scale are dicts
        self.x_offset = offset.get('x', 0.0) if offset is not None else 0.0
        self.y_offset = offset.get('y', 0.0) if offset is not None else 0.0
        self.z_offset = offset.get('z', 0.0) if offset is not None else 0.0

        self.x_scale = scale.get('x', 1.0) if scale is not None else 1.0
        self.y_scale = scale.get('y', 1.0) if scale is not None else 1.0
        self.z_scale = scale.get('z', 1.0) if scale is not None else 1.0

        self.vertices: List[dict] = vertices if vertices is not None else []

    def __str__(self):
        s = 'Element ID: ' + self.element_id + '\n'
        s += 'Shape: ' + self.shape + '\n'
        s += 'x_offset: ' + str(self.x_offset) + '\n'
        s += 'y_offset: ' + str(self.y_offset) + '\n'
        s += 'z_offset: ' + str(self.z_offset) + '\n'
        s += 'x_scale: ' + str(self.x_scale) + '\n'
        s += 'y_scale: ' + str(self.y_scale) + '\n'
        s += 'z_scale: ' + str(self.z_scale) + '\n'
        s += str(self.vertices)
        return s

    def draw(self): ...


class Triangle(Polygon):
    def __init__(self, element_id='triangle', shape='triangle', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.default_vertices()

    def default_vertices(self) -> None:
        default1 = {"color": "white", "x_pos": 0.0, "y_pos": 1.0, "z_pos": 0.0}
        default2 = {"color": "white", "x_pos": -math.sqrt(3)/2, "y_pos": -0.5, "z_pos": 0.0}
        default3 = {"color": "white", "x_pos": math.sqrt(3)/2, "y_pos": -0.5, "z_pos": 0.0}

        defaults = [default1, default2, default3]
        for i, vertex in enumerate(self.vertices):
            update_dict_recursive(src_dict=vertex, dest_dict=defaults[i])

        self.vertices = defaults

    def draw(self) -> None:
        glBegin(GL_TRIANGLES)
        for vertex in self.vertices:
            glColor3f(*colors.get(vertex.get('color'), 'white'))
            x_pos = vertex.get('x_pos', 0.0) * self.x_scale + self.x_offset
            y_pos = vertex.get('y_pos', 0.0) * self.y_scale + self.y_offset
            z_pos = vertex.get('z_pos', 0.0) * self.z_scale + self.z_offset
            glVertex3f(*(x_pos, y_pos, z_pos))
        glEnd()


class Rectangle(Polygon):
    def __init__(self, element_id='rectangle', shape='rectangle', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.triangles = []
        self.default_vertices()
        self.triangles = self.to_triangles(**kwargs)

    def default_vertices(self) -> None:
        default1 = {"color": "white", "x_pos": 1.0, "y_pos": 1.0, "z_pos": 0.0}
        default2 = {"color": "white", "x_pos": -1.0, "y_pos": 1.0, "z_pos": 0.0}
        default3 = {"color": "white", "x_pos": -1.0, "y_pos": -1.0, "z_pos": 0.0}
        default4 = {"color": "white", "x_pos": 1.0, "y_pos": -1.0, "z_pos": 0.0}

        defaults = [default1, default2, default3, default4]
        for i, vertex in enumerate(self.vertices):
            update_dict_recursive(src_dict=vertex, dest_dict=defaults[i])

        self.vertices = defaults

    def to_triangles(self, vertices, **kwargs) -> [Triangle]:
        t1 = Triangle(element_id='t1', vertices=[self.vertices[0], self.vertices[1], self.vertices[2]], **kwargs)
        t2 = Triangle(element_id='t2', vertices=[self.vertices[2], self.vertices[3], self.vertices[0]], **kwargs)
        return [t1, t2]

    def draw(self) -> None:
        for triangle in self.triangles:
            triangle.draw()


class PolygonFactory:
    @staticmethod
    def construct(element_data: dict) -> Polygon:
        match element_data['shape']:
            case 'triangle':
                return Triangle(**element_data)
            case 'rectangle':
                return Rectangle(**element_data)
