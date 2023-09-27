import numpy as np

from OpenGL.GL import *


class TransformNode:
    def __init__(self, element=None, node_id: str | int = 'element_node', offset: np.ndarray | list[float] = None,
                 rot: np.ndarray | list[float] = None, scale: np.ndarray | list[float] = None):
        self.node_id = node_id
        self.element = element
        self.children = {}
        self.parent = None

        self.offset = np.array([0.0, 0.0, 0.0]) if offset is None else np.array(offset)
        self.rot = np.array([0.0, 0.0, 0.0]) if rot is None else np.array(rot)
        self.scale = np.array([1.0, 1.0, 1.0]) if scale is None else np.array(scale)

    def add_child(self, child_node=None):
        child_node = TransformNode() if child_node is None else child_node
        child_node.parent = self
        self.children[child_node.node_id] = child_node

    # draws this element and all sub-nodes down the tree
    def draw(self) -> None:
        glPushMatrix()

        # move scene to center of shape and then rotate
        glTranslate(*self.offset)
        glRotatef(self.rot[0], 0, 1, 0)  # yaw
        glRotatef(self.rot[1], 1, 0, 0)  # pitch
        glRotatef(self.rot[2], 0, 0, 1)  # roll

        # we are scaling every node individually and not using hierarchical scaling
        # otherwise it is very complicated to align elements that have different scales
        glPushMatrix()
        glScalef(*self.scale)

        if self.element is not None:
            self.element.draw()

        glPopMatrix()

        for child_element in self.children.values():
            child_element.draw()

        glPopMatrix()

    def __repr__(self):
        return f"ElementNode(element_id='{self.node_id}', element={self.element.element_id}, children={self.children})"
