from CartesianElements import Element
from Mesh import Mesh



def read_obj(path):       
    try:
        vertices = []
        connections = []
        deg = 0
        curv = []
        parm = []
        cstype = ""

        with open(path) as file:
            for line in file:
                parts = line.strip().split()

                if not parts or parts[0].startswith("#"):
                    continue
                
                if parts[0] == "v":
                    vertex = list(map(float, parts[1:])) + [0]
                    vertices.append(Element(vertex))
                elif parts[0] == "f":
                    face = list(map(int, parts[1:]))
                    for i in range(1, len(face)):
                        connections.append((face[i - 1], face[i]))
                    if len(face) > 2:
                        connections.append((face[-1], face[0]))
                elif parts[0] == "cstype":
                    cstype = parts[1]
                elif parts[0] == "deg":
                    deg = parts[1]
                elif parts[0] == "curv":
                    curv = [float(x) if '.' in x else int(x) for x in parts[1:]]
                elif parts[0] == "parm":
                    parm = [float(x) for x in parts[1:]]

        return Mesh(vertices, connections, deg, curv, parm, cstype)

    except FileNotFoundError:
         print(f"{path} not found")
    except:
         print("An Error occurred")



if __name__ == "__main__":
    filename = "./assets/Curve_1.obj"
    print(read_obj(filename))