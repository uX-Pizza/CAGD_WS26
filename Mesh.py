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