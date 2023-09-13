from modules.geometries import Polyhedron, Cuboid


class ElementNode:
    def __init__(self, element: Polyhedron = None, node_id: str = 'element'):
        self.node_id = node_id
        self.element = element if element is not None else Cuboid()
        self.children: list[ElementNode] = []
        self.parent = None

    def add_child(self, child_node=None):
        child_node = ElementNode() if child_node is None else child_node
        child_node.parent = self
        self.children.append(child_node)

    def pre_process(self): ...

    # draws this element and all sub-nodes down the tree
    def draw(self):
        self.element.draw()
        for child_element in self.children:
            child_element.draw()

    def __repr__(self):
        return f"ElementNode(element_id='{self.node_id}', element={self.element.element_id}, children={self.children})"
