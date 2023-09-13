import math
import numpy as np

from typing import List
from OpenGL.GL import *

from modules.colors import colors_rgb


class Vertex:
    def __init__(self, color: str = 'white', pos_x: float = 0.0, pos_y: float = 0.0, pos_z: float = 0.0):
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z

    def draw(self, scale_x: float = 1.0, scale_y: float = 1.0, scale_z: float = 1.0, offset_x: float = 0.0,
             offset_y: float = 0.0, offset_z: float = 0.0, center_pos_x: float = 0.0, center_pos_y: float = 0.0,
             center_pos_z: float = 0.0):
        glColor3f(*colors_rgb.get(self.color))
        x_pos = self.pos_x * scale_x + offset_x - center_pos_x
        y_pos = self.pos_y * scale_y + offset_y - center_pos_y
        z_pos = self.pos_z * scale_z + offset_z - center_pos_z
        glVertex3f(*(x_pos, y_pos, z_pos))


class Polyhedron:
    def __init__(self, element_id: str = 'polygon', shape: str = 'polygon', color: str = 'white', offset_x: float = 0.0,
                 offset_y: float = 0.0, offset_z: float = 0.0, scale_x: float = 1.0, scale_y: float = 1.0,
                 scale_z: float = 1.0, yaw: float = 0.0, pitch: float = 0.0, roll: float = 0.0,
                 vertices: List[Vertex] = None):
        self.element_id = element_id
        self.shape = shape
        self.color = color

        # offset
        self.offset_x, self.offset_y, self.offset_z = offset_x, offset_y, offset_z

        # scale
        self.scale_x, self.scale_y, self.scale_z = scale_x, scale_y, scale_z

        # rotation
        self.yaw, self.pitch, self.roll = yaw, pitch, roll

        # vertices
        self.vertices: List[Vertex] = vertices if vertices is not None else []

        # center coords
        self.center_pos_x, self.center_pos_y, self.center_pos_z = 0.0, 0.0, 0.0

    def __str__(self):
        s = 'Element ID: ' + self.element_id + '\n'
        s += 'Shape: ' + self.shape + '\n'
        s += 'x_offset: ' + str(self.offset_x) + '\n'
        s += 'y_offset: ' + str(self.offset_y) + '\n'
        s += 'z_offset: ' + str(self.offset_z) + '\n'
        s += 'x_scale: ' + str(self.scale_x) + '\n'
        s += 'y_scale: ' + str(self.scale_y) + '\n'
        s += 'z_scale: ' + str(self.scale_z) + '\n'
        return s

    # finds center coords of shape
    def calc_center(self) -> (float, float, float):
        max_x = max(vertex.pos_x for vertex in self.vertices)
        max_y = max(vertex.pos_y for vertex in self.vertices)
        max_z = max(vertex.pos_z for vertex in self.vertices)

        min_x = min(vertex.pos_x for vertex in self.vertices)
        min_y = min(vertex.pos_y for vertex in self.vertices)
        min_z = min(vertex.pos_z for vertex in self.vertices)

        avg_x = (max_x + min_x) / 2
        avg_y = (max_y + min_y) / 2
        avg_z = (max_z + min_z) / 2

        return avg_x, avg_y, avg_z

    def rotate(self) -> None:
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.roll, 0, 0, 1)

    def pre_process(self) -> None:
        # Move scene to center of shape and then rotate
        glTranslate(self.center_pos_x, self.center_pos_y, self.center_pos_z)
        self.rotate()

    def draw(self, center_pos_x: float = 0.0, center_pos_y: float = 0.0, center_z: float = 0.0) -> None: ...


class Triangle(Polyhedron):
    def __init__(self, element_id: str = 'triangle', shape: str = 'triangle', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.default_vertices()
        self.center_pos_x, self.center_pos_y, self.center_pos_z = self.calc_center()
        self.normal = self.calc_normal()

    def default_vertices(self) -> None:
        top = Vertex(color=self.color, pos_x=0.0, pos_y=1.0, pos_z=0.0)
        left = Vertex(color=self.color, pos_x=-math.sqrt(3) / 2, pos_y=-0.5, pos_z=0.0)
        right = Vertex(color=self.color, pos_x=math.sqrt(3) / 2, pos_y=-0.5, pos_z=0.0)

        defaults = [top, left, right]

        # add defaults to vertices until vertices is filled
        while len(self.vertices) < len(defaults):
            self.vertices.append(defaults[len(self.vertices)])

    def calc_normal(self) -> np.array:
        v1, v2, v3 = self.vertices[0], self.vertices[1], self.vertices[2]
        coords1 = np.array((v1.pos_x, v1.pos_y, v1.pos_z))
        coords2 = np.array((v2.pos_x, v2.pos_y, v2.pos_z))
        coords3 = np.array((v3.pos_x, v3.pos_y, v3.pos_z))
        edge1 = coords2 - coords1
        edge2 = coords3 - coords1
        norm = np.cross(edge1, edge2)
        return norm / np.linalg.norm(norm)

    def draw(self, center_pos_x: float = None, center_pos_y: float = None, center_pos_z: float = None) -> None:
        center_pos_x = self.center_pos_x if center_pos_x is None else center_pos_x
        center_pos_y = self.center_pos_y if center_pos_y is None else center_pos_y
        center_pos_z = self.center_pos_z if center_pos_z is None else center_pos_z

        glBegin(GL_TRIANGLES)
        glNormal3fv(self.normal)
        for vertex in self.vertices:
            vertex.draw(scale_x=self.scale_x, scale_y=self.scale_y, scale_z=self.scale_z, offset_x=self.offset_x,
                        offset_y=self.offset_y, offset_z=self.offset_z, center_pos_x=center_pos_x,
                        center_pos_y=center_pos_y, center_pos_z=center_pos_z)
        glEnd()


class Rectangle(Polyhedron):
    def __init__(self, element_id: str = 'rectangle', shape: str = 'rectangle', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.default_vertices()
        self.center_pos_x, self.center_pos_y, self.center_pos_z = self.calc_center()
        self.triangles = self.to_triangles(**kwargs)

    def default_vertices(self) -> None:
        bottom_left = Vertex(color=self.color, pos_x=-0.5, pos_y=-0.5, pos_z=0.0)
        bottom_right = Vertex(color=self.color, pos_x=0.5, pos_y=-0.5, pos_z=0.0)
        top_right = Vertex(color=self.color, pos_x=0.5, pos_y=0.5, pos_z=0.0)
        top_left = Vertex(color=self.color, pos_x=-0.5, pos_y=0.5, pos_z=0.0)

        defaults = [bottom_left, bottom_right, top_right, top_left]

        # add defaults to vertices until vertices is filled
        while len(self.vertices) < len(defaults):
            self.vertices.append(defaults[len(self.vertices)])

    def to_triangles(self, vertices, **kwargs) -> [Triangle]:
        t1 = Triangle(element_id='triangle1', vertices=[self.vertices[0], self.vertices[1], self.vertices[2]], **kwargs)
        t2 = Triangle(element_id='triangle2', vertices=[self.vertices[2], self.vertices[3], self.vertices[0]], **kwargs)
        return [t1, t2]

    def draw(self, center_pos_x: float = None, center_pos_y: float = None, center_pos_z: float = None) -> None:
        center_pos_x = self.center_pos_x if center_pos_x is None else center_pos_x
        center_pos_y = self.center_pos_y if center_pos_y is None else center_pos_y
        center_pos_z = self.center_pos_z if center_pos_z is None else center_pos_z

        for triangle in self.triangles:
            triangle.draw(center_pos_x=center_pos_x, center_pos_y=center_pos_y, center_pos_z=center_pos_z)


class Cuboid(Polyhedron):
    def __init__(self, element_id: str = 'cuboid', shape: str = 'cuboid', **kwargs):
        super().__init__(element_id=element_id, shape=shape, **kwargs)
        self.vertices = []
        self.default_vertices()
        self.center_x, self.center_y, self.center_z = self.calc_center()
        self.rectangles = self.to_rectangles(**kwargs)

    def default_vertices(self) -> None:

        front_bottom_left = Vertex(color=self.color, pos_x=-0.5, pos_y=-0.5, pos_z=0.5)  # 0
        front_bottom_right = Vertex(color=self.color, pos_x=0.5, pos_y=-0.5, pos_z=0.5)  # 1
        front_top_right = Vertex(color=self.color, pos_x=0.5, pos_y=0.5, pos_z=0.5)  # 2
        front_top_left = Vertex(color=self.color, pos_x=-0.5, pos_y=0.5, pos_z=0.5)  # 3

        back_top_left = Vertex(color=self.color, pos_x=-0.5, pos_y=0.5, pos_z=-0.5)  # 4
        back_top_right = Vertex(color=self.color, pos_x=0.5, pos_y=0.5, pos_z=-0.5)  # 5
        back_bottom_right = Vertex(color=self.color, pos_x=0.5, pos_y=-0.5, pos_z=-0.5)  # 6
        back_bottom_left = Vertex(color=self.color, pos_x=-0.5, pos_y=-0.5, pos_z=-0.5)  # 7

        defaults = [front_bottom_left, front_bottom_right, front_top_right, front_top_left,
                    back_top_left, back_top_right, back_bottom_right, back_bottom_left]

        # add defaults to vertices until vertices is filled
        while len(self.vertices) < len(defaults):
            self.vertices.append(defaults[len(self.vertices)])

    def to_rectangles(self, **kwargs) -> [Rectangle]:
        vtx = [vertex for vertex in self.vertices]

        front = Rectangle(element_id='front_side', vertices=[vtx[0], vtx[3], vtx[2], vtx[1]], **kwargs)
        right = Rectangle(element_id='right_side', vertices=[vtx[1], vtx[2], vtx[5], vtx[6]], **kwargs)
        back = Rectangle(element_id='back_side', vertices=[vtx[4], vtx[7], vtx[6], vtx[5]], **kwargs)
        left = Rectangle(element_id='left_side', vertices=[vtx[0], vtx[7], vtx[4], vtx[3]], **kwargs)
        bottom = Rectangle(element_id='bottom_side', vertices=[vtx[0], vtx[1], vtx[6], vtx[7]], **kwargs)
        top = Rectangle(element_id='top_side', vertices=[vtx[2], vtx[3], vtx[4], vtx[5]], **kwargs)

        return [front, right, back, left, bottom, top]

    def draw(self, center_pos_x: float = None, center_pos_y: float = None, center_pos_z: float = None) -> None:
        center_pos_x = self.center_pos_x if center_pos_x is None else center_pos_x
        center_pos_y = self.center_pos_y if center_pos_y is None else center_pos_y
        center_pos_z = self.center_pos_z if center_pos_z is None else center_pos_z

        for rectangle in self.rectangles:
            rectangle.draw(center_pos_x=center_pos_x, center_pos_y=center_pos_y, center_pos_z=center_pos_z)
