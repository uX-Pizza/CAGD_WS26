class Mesh:
    def __init__(self, vertices=None, connections=None, degree=None, curve=None, parameter=None, cstype=None):
        if connections is None:
            connections = []
        if vertices is None:
            vertices = []
        if degree is None:
            degree = 0
        if curve is None:
            curve = []
        if parameter is None:
            parameter = []
        if cstype is None:
            cstype = "default"


        self.vertices = vertices
        self.connections = connections
        self.degree = degree # Degree of curve
        self.curve = curve
        self.parameter = parameter
        self.cstype = cstype


    def __str__(self):
        v = []
        for i in self.vertices:
            v.append(i.value)
        return f"{v}\n{self.connections}\n{len(v)} vertices\n{len(self.connections)} connections\n Degree {self.degree}\n Curv {self.curve}\n Parm {self.parameter}"


    def delete_vertex(self, vertex):
        self.vertices.pop(vertex)
        for c in self.connections.copy():
            if vertex + 1 in c:
                self.connections.remove(c)
            else:
                if c[0] > vertex + 1 and c[1] > vertex + 1:
                    self.connections[self.connections.index(c)] = (c[0] - 1, c[1] - 1)
                elif c[0] > vertex + 1:
                    self.connections[self.connections.index(c)] = (c[0] - 1, c[1])
                elif c[1] > vertex + 1:
                    self.connections[self.connections.index(c)] = (c[0], c[1] - 1)