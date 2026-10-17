from CartesianElements import Element
from Mesh import Mesh



def read_obj(path):       
    try:
        vertices = []
        connections = []
        with open(path) as file:
            for line in file:
                if line[0] == "v":
                    vertex = list(map(float, line[2:].strip().split())) + [0]
                    vertices.append(Element(vertex))
                elif line[0] == "f":
                    face = list(map(int, line[2:].strip().split()))
                    for i in range(1, len(face)):
                        connections.append((face[i - 1], face[i]))

        return Mesh(vertices, connections)

    except FileNotFoundError:
         print(f"{file} not found")
    except:
         print("An Error occurred")



if __name__ == "__main__":
    filename = "./assets/Curve_1.obj"
    print(read_obj(filename))