import math
import numpy as np

from typing import List

from OpenGL.GL import *

from modules.colors import colors_rgb
from modules.other_utils import *


class Polyhedron:
    def __init__(self, element_id='polygon', shape='polygon', color='white', offset=None, scale=None, rotation=None,
                 vertices=None):
        self.element_id = element_id
        self.shape = shape
        self.color = color

        self.x_offset = offset.get('x', 0.0) if offset is not None else 0.0
        self.y_offset = offset.get('y', 0.0) if offset is not None else 0.0
        self.z_offset = offset.get('z', 0.0) if offset is not None else 0.0

        self.x_scale = scale.get('x', 1.0) if scale is not None else 1.0
        self.y_scale = scale.get('y', 1.0) if scale is not None else 1.0
        self.z_scale = scale.get('z', 1.0) if scale is not None else 1.0

        self.yaw = rotation.get('yaw', 0.0) if rotation is not None else 0.0
        self.pitch = rotation.get('pitch', 0.0) if rotation is not None else 0.0
        self.roll = rotation.get('roll', 0.0) if rotation is not None else 0.0

        self.vertices: List[dict] = vertices if vertices is not None else []
        self.center = (0, 0, 0)

    def __str__(self):
        s = 'Element ID: ' + self.element_id + '\n'
        s += 'Shape: ' + self.shape + '\n'
        s += 'x_offset: ' + str(self.x_offset) + '\n'
        s += 'y_offset: ' + str(self.y_offset) + '\n'
        s += 'z_offset: ' + str(self.z_offset) + '\n'
        s += 'x_scale: ' + str(self.x_scale) + '\n'
        s += 'y_scale: ' + str(self.y_scale) + '\n'
        s += 'z_scale: ' + str(self.z_scale) + '\n'
        for i, vertex in enumerate(self.vertices):
            s += f'vertex {i}: {vertex}\n'
        return s

    # finds center coords of shape
    def calc_center(self) -> (float, float, float):
        max_x = max([vertex['x_pos'] + self.x_offset for vertex in self.vertices])
        max_y = max([vertex['y_pos'] + self.y_offset for vertex in self.vertices])
        max_z = max([vertex['z_pos'] + self.z_offset for vertex in self.vertices])

        min_x = min([vertex['x_pos'] + self.x_offset for vertex in self.vertices])
        min_y = min([vertex['y_pos'] + self.y_offset for vertex in self.vertices])
        min_z = min([vertex['z_pos'] + self.z_offset for vertex in self.vertices])

        avg_x = (max_x + min_x) / 2
        avg_y = (max_y + min_y) / 2
        avg_z = (max_z + min_z) / 2

        return avg_x, avg_y, avg_z

    def rotate(self, yaw, pitch, roll) -> None:
        glRotatef(yaw, 0, 1, 0)
        glRotatef(pitch, 1, 0, 0)
        glRotatef(roll, 0, 0, 1)

    def pre_process(self) -> None:
        # Move scene to center of shape
        x_center, y_center, z_center = self.center[0], self.center[1], self.center[2]
        glTranslate(x_center, y_center, z_center)

        # Rotate
        self.rotate(self.yaw, self.pitch, self.roll)

    def draw(self) -> None: ...


class Triangle(Polyhedron):
    def __init__(self, element_id='triangle', shape='triangle', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.default_vertices()
        self.center = self.calc_center()
        self.normal = self.calc_normal()

    def default_vertices(self) -> None:
        top = {"color": self.color, "x_pos": 0.0, "y_pos": 1.0, "z_pos": 0.0}
        left = {"color": self.color, "x_pos": -math.sqrt(3)/2, "y_pos": -0.5, "z_pos": 0.0}
        right = {"color": self.color, "x_pos": math.sqrt(3)/2, "y_pos": -0.5, "z_pos": 0.0}

        defaults = [top, left, right]
        for i, vertex in enumerate(self.vertices):
            update_dict_recursive(src_dict=vertex, dest_dict=defaults[i])

        self.vertices = defaults

    def calc_normal(self) -> np.array:
        v1, v2, v3 = self.vertices[0], self.vertices[1], self.vertices[2]
        coords1 = np.array((v1['x_pos'], v1['y_pos'], v1['z_pos']))
        coords2 = np.array((v2['x_pos'], v2['y_pos'], v2['z_pos']))
        coords3 = np.array((v3['x_pos'], v3['y_pos'], v3['z_pos']))
        e1 = coords2 - coords1
        e2 = coords3 - coords1
        n = np.cross(e1, e2)
        return n / np.linalg.norm(n)

    def draw(self, shape_center=None) -> None:
        shape_center = self.center if shape_center is None else shape_center
        glBegin(GL_TRIANGLES)
        glNormal3fv(self.normal)
        for vertex in self.vertices:
            glColor3f(*colors_rgb.get(vertex.get('color'), 'white'))
            x_pos = vertex.get('x_pos', 0.0) * self.x_scale + self.x_offset - shape_center[0]
            y_pos = vertex.get('y_pos', 0.0) * self.y_scale + self.y_offset - shape_center[1]
            z_pos = vertex.get('z_pos', 0.0) * self.z_scale + self.z_offset - shape_center[2]
            glVertex3f(*(x_pos, y_pos, z_pos))
        glEnd()


class Rectangle(Polyhedron):
    def __init__(self, element_id='rectangle', shape='rectangle', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.default_vertices()
        self.center = self.calc_center()
        self.triangles = self.to_triangles(**kwargs)

    def default_vertices(self) -> None:
        bottom_left = {"color": self.color, "x_pos": -0.5, "y_pos": -0.5, "z_pos": 0.0}
        bottom_right = {"color": self.color, "x_pos": 0.5, "y_pos": -0.5, "z_pos": 0.0}
        top_right = {"color": self.color, "x_pos": 0.5, "y_pos": 0.5, "z_pos": 0.0}
        top_left = {"color": self.color, "x_pos": -0.5, "y_pos": 0.5, "z_pos": 0.0}

        defaults = [bottom_left, bottom_right, top_right, top_left]
        for i, vertex in enumerate(self.vertices):
            update_dict_recursive(src_dict=vertex, dest_dict=defaults[i])

        self.vertices = defaults

    def to_triangles(self, vertices, **kwargs) -> [Triangle]:
        t1 = Triangle(element_id='t1', vertices=[self.vertices[0], self.vertices[1], self.vertices[2]], **kwargs)
        t2 = Triangle(element_id='t2', vertices=[self.vertices[2], self.vertices[3], self.vertices[0]], **kwargs)
        return [t1, t2]

    def draw(self, shape_center=None) -> None:
        shape_center = self.center if shape_center is None else shape_center
        for triangle in self.triangles:
            triangle.draw(shape_center=shape_center)


class Cuboid(Polyhedron):
    def __init__(self, element_id='cuboid', shape='cuboid', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.vertices = []
        self.default_vertices()
        self.center = self.calc_center()
        self.rectangles = self.to_rectangles(**kwargs)

    def default_vertices(self) -> None:
        front_bottom_left = {"color": self.color, "x_pos": -0.5, "y_pos": -0.5, "z_pos": 0.5}  # 0
        front_bottom_right = {"color": self.color, "x_pos": 0.5, "y_pos": -0.5, "z_pos": 0.5}  # 1
        front_top_right = {"color": self.color, "x_pos": 0.5, "y_pos": 0.5, "z_pos": 0.5}  # 2
        front_top_left = {"color": self.color, "x_pos": -0.5, "y_pos": 0.5, "z_pos": 0.5}  # 3

        back_top_left = {"color": self.color, "x_pos": -0.5, "y_pos": 0.5, "z_pos": -0.5}  # 4
        back_top_right = {"color": self.color, "x_pos": 0.5, "y_pos": 0.5, "z_pos": -0.5}  # 5
        back_bottom_right = {"color": self.color, "x_pos": 0.5, "y_pos": -0.5, "z_pos": -0.5}  # 6
        back_bottom_left = {"color": self.color, "x_pos": -0.5, "y_pos": -0.5, "z_pos": -0.5}  # 7

        defaults = [front_bottom_left, front_bottom_right, front_top_right, front_top_left,
                    back_top_left, back_top_right, back_bottom_right, back_bottom_left]
        for i, vertex in enumerate(self.vertices):
            update_dict_recursive(src_dict=vertex, dest_dict=defaults[i])

        self.vertices = defaults

    def to_rectangles(self, **kwargs) -> [Rectangle]:
        vtx = [vertex for vertex in self.vertices]

        front = Rectangle(element_id='front_side', vertices=[vtx[0], vtx[3], vtx[2], vtx[1]], **kwargs)
        right = Rectangle(element_id='right_side', vertices=[vtx[1], vtx[2], vtx[5], vtx[6]], **kwargs)
        back = Rectangle(element_id='back_side', vertices=[vtx[4], vtx[7], vtx[6], vtx[5]], **kwargs)
        left = Rectangle(element_id='left_side', vertices=[vtx[0], vtx[7], vtx[4], vtx[3]], **kwargs)
        bottom = Rectangle(element_id='bottom_side', vertices=[vtx[0], vtx[1], vtx[6], vtx[7]], **kwargs)
        top = Rectangle(element_id='top_side', vertices=[vtx[2], vtx[3], vtx[4], vtx[5]], **kwargs)

        return [front, right, back, left, bottom, top]

    def draw(self, shape_center=None) -> None:
        shape_center = self.center if shape_center is None else shape_center
        for rectangle in self.rectangles:
            rectangle.draw(shape_center=shape_center)


class PolyhedronFactory:
    @staticmethod
    def construct(element_data: dict) -> Polyhedron:
        shapes = {
            'triangle': Triangle,
            'rectangle': Rectangle,
            'cuboid': Cuboid
        }
        return shapes[element_data['shape']](**element_data)
