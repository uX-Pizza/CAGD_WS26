
file = "./assets/Curve_1.obj"

def read_obj(path):       
    try:
        vertices = []
        faces = []
        with open(path) as file:
            for line in file:
                if line[0] == "v":
                    vertex = list(map(float, line[2:].strip().split()))
                    vertices.append(vertex)
                elif line[0] == "f":
                    face = list(map(int, line[2:].strip().split()))
                    faces.append(face)
        curve = {
                 "vertecies": vertices, 
                 "faces": faces
                }

        return curve

    except FileNotFoundError:
         print(f"{file} not found")
    except:
         print("An Error occurred")

print(read_obj(file))