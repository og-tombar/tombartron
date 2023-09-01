import math
from typing import List

from OpenGL.GL import *

from modules.color import colors
from modules.other_utils import *


class Polyhedron:
    def __init__(self, element_id='polygon', shape='polygon', offset=None, scale=None, rotation=None, vertices=None):
        self.element_id = element_id
        self.shape = shape

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
        self.center = self.calc_center()

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

    # finds center coords of shape
    def calc_center(self) -> (float, float, float):
        max_x = max([vertex['x_pos'] for vertex in self.vertices])
        max_y = max([vertex['y_pos'] for vertex in self.vertices])
        max_z = max([vertex['z_pos'] for vertex in self.vertices])

        min_x = min([vertex['x_pos'] for vertex in self.vertices])
        min_y = min([vertex['y_pos'] for vertex in self.vertices])
        min_z = min([vertex['z_pos'] for vertex in self.vertices])

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
            x_pos = vertex.get('x_pos', 0.0) + self.x_offset - self.center[0]
            y_pos = vertex.get('y_pos', 0.0) + self.y_offset - self.center[1]
            z_pos = vertex.get('z_pos', 0.0) + self.z_offset - self.center[2]
            glVertex3f(*(x_pos, y_pos, z_pos))
        glEnd()


class Rectangle(Polyhedron):
    def __init__(self, element_id='rectangle', shape='rectangle', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
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


class Cuboid(Polyhedron):
    def __init__(self, element_id='cuboid', shape='cuboid', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.vertices = []
        self.default_vertices()
        self.triangles = self.to_triangles(**kwargs)

    def default_vertices(self) -> None:
        # front face
        default1 = {"color": "white", "x_pos": -1.0, "y_pos": -1.0, "z_pos": 1.0}  # bottom left
        default2 = {"color": "red", "x_pos": 1.0, "y_pos": -1.0, "z_pos": 1.0}  # bottom right
        default3 = {"color": "green", "x_pos": 1.0, "y_pos": 1.0, "z_pos": 1.0}  # top right
        default4 = {"color": "blue", "x_pos": -1.0, "y_pos": 1.0, "z_pos": 1.0}  # top left

        # back face
        default5 = {"color": "white", "x_pos": -1.0, "y_pos": -1.0, "z_pos": -1.0}  # bottom left
        default6 = {"color": "red", "x_pos": 1.0, "y_pos": -1.0, "z_pos": -1.0}  # bottom right
        default7 = {"color": "green", "x_pos": 1.0, "y_pos": 1.0, "z_pos": -1.0}  # top right
        default8 = {"color": "blue", "x_pos": -1.0, "y_pos": 1.0, "z_pos": -1.0}  # top left

        defaults = [default1, default2, default3, default4, default5, default6, default7, default8]
        for i, vertex in enumerate(self.vertices):
            update_dict_recursive(src_dict=vertex, dest_dict=defaults[i])

        self.vertices = defaults

    def to_triangles(self, vertices, **kwargs) -> [Triangle]:
        t1 = Triangle(element_id='t1', vertices=[self.vertices[0], self.vertices[1], self.vertices[2]], **kwargs)
        t2 = Triangle(element_id='t2', vertices=[self.vertices[2], self.vertices[3], self.vertices[0]], **kwargs)
        t3 = Triangle(element_id='t3', vertices=[self.vertices[1], self.vertices[2], self.vertices[5]], **kwargs)
        t4 = Triangle(element_id='t4', vertices=[self.vertices[5], self.vertices[6], self.vertices[1]], **kwargs)
        t5 = Triangle(element_id='t5', vertices=[self.vertices[4], self.vertices[5], self.vertices[6]], **kwargs)
        t6 = Triangle(element_id='t6', vertices=[self.vertices[6], self.vertices[7], self.vertices[4]], **kwargs)
        t7 = Triangle(element_id='t7', vertices=[self.vertices[0], self.vertices[3], self.vertices[4]], **kwargs)
        t8 = Triangle(element_id='t8', vertices=[self.vertices[4], self.vertices[7], self.vertices[0]], **kwargs)
        t9 = Triangle(element_id='t9', vertices=[self.vertices[0], self.vertices[1], self.vertices[4]], **kwargs)
        t10 = Triangle(element_id='t10', vertices=[self.vertices[4], self.vertices[5], self.vertices[0]], **kwargs)
        t11 = Triangle(element_id='t11', vertices=[self.vertices[2], self.vertices[3], self.vertices[6]], **kwargs)
        t12 = Triangle(element_id='t12', vertices=[self.vertices[6], self.vertices[7], self.vertices[2]], **kwargs)
        return [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]

    def draw(self) -> None:
        for triangle in self.triangles:
            triangle.draw()


class PolyhedronFactory:
    @staticmethod
    def construct(element_data: dict) -> Polyhedron:
        match element_data['shape']:
            case 'triangle':
                return Triangle(**element_data)
            case 'rectangle':
                return Rectangle(**element_data)
            case 'cuboid':
                return Cuboid(**element_data)
