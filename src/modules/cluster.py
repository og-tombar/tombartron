class Cluster:
    def __init__(self):
        self.elements = {}

    def pre_process(self): ...

    def draw(self):
        for element in self.elements.values():
            element.draw()
