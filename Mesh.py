class Mesh:
    def __init__(self, vertices=None, connections=None):
        if connections is None:
            connections = []
        if vertices is None:
            vertices = []

        self.vertices = vertices
        self.connections = connections


    def __str__(self):
        v = []
        for i in self.vertices:
            v.append(i.value)
        return f"{v}\n{self.connections}\n{len(v)} vertices\n{len(self.connections)} connections"