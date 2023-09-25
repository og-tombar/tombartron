import math
import numpy as np

from typing import List
from OpenGL.GL import *

from graphics.colors import Colors
from graphics.transform_node import TransformNode


class Vertex:
    def __init__(self, color: str = 'white', node: TransformNode = TransformNode(), relative_pos_x: float = 0,
                 relative_pos_y: float = 0, relative_pos_z: float = 0):
        self.color = Colors.rgb.get(color)
        self.node = node

        # relative to node position offset
        self.relative_pos_x = relative_pos_x
        self.relative_pos_y = relative_pos_y
        self.relative_pos_z = relative_pos_z

    def draw(self) -> None:
        glColor3f(*self.color)
        glVertex3f(self.relative_pos_x, self.relative_pos_y, self.relative_pos_z)


class Polyhedron:
    def __init__(self, element_id: str = 'polyhedron', colors: list[str] = None, vertices: List[Vertex] = None,
                 node: TransformNode = TransformNode()):
        self.element_id = element_id
        self.colors = colors
        self.vertices: List[Vertex] = vertices if vertices is not None else []
        self.node = node

    def __str__(self):
        return 'Element ID: ' + self.element_id + '. Node: ' + self.node.node_id

    def draw(self) -> None: ...


class Triangle(Polyhedron):
    def __init__(self, element_id: str = 'triangle', colors: list[str] = None, vertices: List[Vertex] = None,
                 node: TransformNode = TransformNode()):
        colors = ['white'] * 3 if colors is None else colors
        super().__init__(element_id=element_id, colors=colors, vertices=vertices, node=node)
        self.default_vertices()
        self.normal = self.calc_normal()

    def default_vertices(self) -> None:
        top = Vertex(color=self.colors[0], node=self.node, relative_pos_x=0, relative_pos_y=1, relative_pos_z=0)
        left = Vertex(color=self.colors[1], node=self.node, relative_pos_x=-math.sqrt(3) / 2, relative_pos_y=-0.5,
                      relative_pos_z=0)
        right = Vertex(color=self.colors[2], node=self.node, relative_pos_x=math.sqrt(3) / 2, relative_pos_y=-0.5,
                       relative_pos_z=0)

        defaults = [top, left, right]

        # add defaults to vertices until vertices is filled
        while len(self.vertices) < len(defaults):
            self.vertices.append(defaults[len(self.vertices)])

    def calc_normal(self) -> np.array:
        v1, v2, v3 = self.vertices[0], self.vertices[1], self.vertices[2]
        coords1 = np.array((v1.relative_pos_x, v1.relative_pos_x, v1.relative_pos_z))
        coords2 = np.array((v2.relative_pos_x, v2.relative_pos_x, v2.relative_pos_z))
        coords3 = np.array((v3.relative_pos_x, v3.relative_pos_x, v3.relative_pos_z))
        edge1 = coords2 - coords1
        edge2 = coords3 - coords1
        norm = np.cross(edge1, edge2)
        return norm / np.linalg.norm(norm)

    def draw(self) -> None:
        glBegin(GL_TRIANGLES)
        glNormal3fv(self.normal)
        for vertex in self.vertices:
            vertex.draw()
        glEnd()


class Rectangle(Polyhedron):
    def __init__(self, element_id: str = 'rectangle', colors: list[str] = None, vertices: List[Vertex] = None,
                 node: TransformNode = TransformNode()):
        colors = ['white'] * 4 if colors is None else colors
        super().__init__(element_id=element_id, colors=colors, vertices=vertices, node=node)
        self.default_vertices()
        self.triangles = self.to_triangles()

    def default_vertices(self) -> None:
        bottom_left = Vertex(
            color=self.colors[0], node=self.node, relative_pos_x=-0.5, relative_pos_y=-0.5, relative_pos_z=0)
        bottom_right = Vertex(
            color=self.colors[1], node=self.node, relative_pos_x=0.5, relative_pos_y=-0.5, relative_pos_z=0)
        top_right = Vertex(
            color=self.colors[2], node=self.node, relative_pos_x=0.5, relative_pos_y=0.5, relative_pos_z=0)
        top_left = Vertex(
            color=self.colors[3], node=self.node, relative_pos_x=-0.5, relative_pos_y=0.5, relative_pos_z=0)

        defaults = [bottom_left, bottom_right, top_right, top_left]

        # add defaults to vertices until vertices is filled
        while len(self.vertices) < len(defaults):
            self.vertices.append(defaults[len(self.vertices)])

    def to_triangles(self) -> [Triangle]:
        t1 = Triangle(element_id='triangle1', vertices=[self.vertices[0], self.vertices[1], self.vertices[2]],
                      colors=self.colors, node=self.node)
        t2 = Triangle(element_id='triangle2', vertices=[self.vertices[2], self.vertices[3], self.vertices[0]],
                      colors=self.colors, node=self.node)
        return [t1, t2]

    def draw(self) -> None:
        for triangle in self.triangles:
            triangle.draw()


class Cuboid(Polyhedron):
    def __init__(self, element_id: str = 'cuboid', colors: list[str] = None, vertices: List[Vertex] = None,
                 node: TransformNode = TransformNode()):
        colors = ['white'] * 8 if colors is None else colors
        super().__init__(element_id=element_id, colors=colors, vertices=vertices, node=node)
        self.node = node
        self.default_vertices()
        self.rectangles = self.to_rectangles()

    def default_vertices(self) -> None:
        front_bottom_left = Vertex(
            color=self.colors[0], node=self.node, relative_pos_x=-0.5, relative_pos_y=-0.5, relative_pos_z=0.5)  # 0
        front_bottom_right = Vertex(
            color=self.colors[1], node=self.node, relative_pos_x=0.5, relative_pos_y=-0.5, relative_pos_z=0.5)  # 1
        front_top_right = Vertex(
            color=self.colors[2], node=self.node, relative_pos_x=0.5, relative_pos_y=0.5, relative_pos_z=0.5)  # 2
        front_top_left = Vertex(
            color=self.colors[3], node=self.node, relative_pos_x=-0.5, relative_pos_y=0.5, relative_pos_z=0.5)  # 3

        back_top_left = Vertex(
            color=self.colors[4], node=self.node, relative_pos_x=-0.5, relative_pos_y=0.5, relative_pos_z=-0.5)  # 4
        back_top_right = Vertex(
            color=self.colors[5], node=self.node, relative_pos_x=0.5, relative_pos_y=0.5, relative_pos_z=-0.5)  # 5
        back_bottom_right = Vertex(
            color=self.colors[6], node=self.node, relative_pos_x=0.5, relative_pos_y=-0.5, relative_pos_z=-0.5)  # 6
        back_bottom_left = Vertex(
            color=self.colors[7], node=self.node, relative_pos_x=-0.5, relative_pos_y=-0.5, relative_pos_z=-0.5)  # 7

        defaults = [front_bottom_left, front_bottom_right, front_top_right, front_top_left,
                    back_top_left, back_top_right, back_bottom_right, back_bottom_left]

        # add defaults to vertices until vertices is filled
        while len(self.vertices) < len(defaults):
            self.vertices.append(defaults[len(self.vertices)])

    def to_rectangles(self) -> [Rectangle]:
        vtx = self.vertices

        front = Rectangle(element_id='front_side', colors=self.colors, vertices=[vtx[0], vtx[3], vtx[2], vtx[1]],
                          node=self.node)
        right = Rectangle(element_id='right_side', colors=self.colors, vertices=[vtx[1], vtx[2], vtx[5], vtx[6]],
                          node=self.node)
        back = Rectangle(element_id='back_side', colors=self.colors, vertices=[vtx[4], vtx[7], vtx[6], vtx[5]],
                         node=self.node)
        left = Rectangle(element_id='left_side', colors=self.colors, vertices=[vtx[0], vtx[7], vtx[4], vtx[3]],
                         node=self.node)
        bottom = Rectangle(element_id='bottom_side', colors=self.colors, vertices=[vtx[0], vtx[1], vtx[6], vtx[7]],
                           node=self.node)
        top = Rectangle(element_id='top_side', colors=self.colors, vertices=[vtx[2], vtx[3], vtx[4], vtx[5]],
                        node=self.node)

        return [front, right, back, left, bottom, top]

    def draw(self) -> None:
        for rectangle in self.rectangles:
            rectangle.draw()
