from OpenGL.GL import *


class TransformNode:
    def __init__(self, element=None, node_id: str | int = 'element_node', anchor_pos_x: float = None,
                 anchor_pos_y: float = None, anchor_pos_z: float = None, offset_x: float = 0, offset_y: float = 0,
                 offset_z: float = 0, yaw: float = 0, pitch: float = 0, roll: float = 0, scale_x: float = 1,
                 scale_y: float = 1, scale_z: float = 1):
        self.node_id = node_id
        self.element = element
        self.children = {}
        self.parent = None

        # hierarchical offset, is summed with offsets up to root
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z

        # hierarchical scale, is multiplied with scales up to root
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z

        # rotation
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

        self.anchor_pos_x = anchor_pos_x if anchor_pos_x is not None else self.offset_x
        self.anchor_pos_y = anchor_pos_y if anchor_pos_y is not None else self.offset_y
        self.anchor_pos_z = anchor_pos_z if anchor_pos_z is not None else self.offset_z

    def add_child(self, child_node=None):
        child_node = TransformNode() if child_node is None else child_node
        child_node.parent = self
        child_node.anchor_pos_x = self.anchor_pos_x
        child_node.anchor_pos_y = self.anchor_pos_y
        child_node.anchor_pos_z = self.anchor_pos_z
        self.children[child_node.node_id] = child_node

    def pre_process(self):
        # Move scene to center of shape and then rotate
        glTranslate(self.offset_x, self.offset_y, self.offset_z)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.roll, 0, 0, 1)

    def update_relative_pos_for_all_vertices(self):
        vertices = self.get_all_tree_vertices()
        for vertex in vertices:
            vertex.calc_relative_pos()

    def get_root_scale(self) -> (float, float, float):
        itr = self
        while itr.parent is not None:
            itr = itr.parent
        return itr.scale_x, itr.scale_y, itr.scale_z

    def get_all_tree_elements(self) -> list:
        elements = []

        # get vertices of current node
        if self.element is not None:
            elements.append(self.element)

        # children recursive
        for child in self.children.values():
            elements.extend(child.get_all_tree_elements())

        return elements

    def get_all_tree_vertices(self) -> list:
        vertices = []

        # get vertices of current node
        if self.element is not None:
            vertices.extend(self.element.vertices)

        # children recursive
        for child in self.children.values():
            vertices.extend(child.get_all_tree_vertices())

        return vertices

    def get_offsets_sums_up_to_root(self) -> (float, float, float):
        offset_x, offset_y, offset_z = 0, 0, 0
        itr = self
        while itr is not None:
            offset_x += itr.offset_x
            offset_y += itr.offset_y
            offset_z += itr.offset_z
            itr = itr.parent
        return offset_x, offset_y, offset_z

    def get_scales_product_up_to_root(self) -> (float, float, float):
        scale_x, scale_y, scale_z = 1, 1, 1
        itr = self
        while itr is not None:
            scale_x *= itr.scale_x
            scale_y *= itr.scale_y
            scale_z *= itr.scale_z
            itr = itr.parent
        return scale_x, scale_y, scale_z

    # draws this element and all sub-nodes down the tree
    def draw(self) -> None:
        glPushMatrix()
        self.pre_process()

        # we are scaling every node individually and not using hierarchical scaling
        glPushMatrix()
        glScalef(self.scale_x, self.scale_y, self.scale_z)

        if self.element is not None:
            self.element.draw()

        glPopMatrix()

        for child_element in self.children.values():
            child_element.draw()

        glPopMatrix()

    def __repr__(self):
        return f"ElementNode(element_id='{self.node_id}', element={self.element.element_id}, children={self.children})"
