class Mesh:
    def __init__(self, vertices=None, connections=None, deg=None, curv=None, parm =None):
        if connections is None:
            connections = []
        if vertices is None:
            vertices = []
        if deg is None:
            deg = 0
        if curv is None:
            curv = []
        if parm is None:
            parm = []

        self.vertices = vertices
        self.connections = connections
        self.deg = deg # Degree of curv
        self.curv = curv
        self.parm = parm

    def __str__(self):
        v = []
        for i in self.vertices:
            v.append(i.value)
        return f"{v}\n{self.connections}\n{len(v)} vertices\n{len(self.connections)} connections\n Degree {self.deg}\n Curv {self.curv}\n Parm {self.parm}"