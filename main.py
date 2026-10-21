import pygame
from pygame.locals import *
from sys import exit
import math

from ObjectReader import read_obj
from CartesianElements import Element
from Mesh import Mesh



pygame.init()
screen = pygame.display.set_mode((800, 800))
drawn_positions = []
drawn_connections = []
selected_mesh = None
selected_vertex = None
selected_connection = None
l_mouse_pressed = False
r_mouse_pressed = False
last_mouse_pos = None
x_offset = 400
y_offset = 400

mesh_list = [read_obj("./assets/Curve_1.obj"), Mesh([Element([3, 0, 1]), Element([1, 3, 1])], [(0, 1)])]

SCALE_FACTOR = 10
SCALE_STEP = 1.75
MAX_SCALE_FACTOR = 30.0
MIN_SCALE_FACTOR = 1.0

POINT_RADIUS = 5
BACKGROUND_COLOR = (255, 255, 255)
POINT_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)
CONNECTION_CLICKSPOT_RADIUS = 10



def euclidean_distance(a: tuple, b: tuple):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)


# create new mesh at position (screen coordinates)
def create_mesh(p):
    p = [(p[0] - x_offset) / SCALE_FACTOR, (((p[1]) - y_offset) / SCALE_FACTOR) * -1, 1]
    mesh_list.append(Mesh([Element(p)]))


def create_vertex(mesh, p):
    p = [(p[0] - x_offset) / SCALE_FACTOR, (((p[1]) - y_offset) / SCALE_FACTOR) * -1, 1]
    mesh_list[mesh].vertices.append(Element(p))



run = True
while run:
    """
    -------------------------EVENTS-------------------------
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_PLUS:
                SCALE_FACTOR = min(MAX_SCALE_FACTOR, SCALE_FACTOR * SCALE_STEP)
            if event.key == K_MINUS:
                SCALE_FACTOR = max(MIN_SCALE_FACTOR, SCALE_FACTOR / SCALE_STEP)
            if event.key == K_m:
                create_mesh(pygame.mouse.get_pos())
            if event.key == K_n:
                if selected_mesh is not None:
                    create_vertex(selected_mesh, pygame.mouse.get_pos())

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            if not l_mouse_pressed:
                mouse_pos = pygame.mouse.get_pos()
                v_min_distance, c_min_distance = 0, 0
                v_min_index, c_min_index = 0, 0
                v_mesh, c_mesh = None, None
                for i in range(0, len(drawn_positions)):
                    distances = [euclidean_distance(mouse_pos, x) for x in drawn_positions[i]]
                    v_min_distance = min(distances)
                    v_min_index = distances.index(v_min_distance)
                    if v_min_distance <= POINT_RADIUS * 2:
                        v_mesh = i
                        break

                for i in range(0, len(drawn_connections)):
                    distances = [euclidean_distance(mouse_pos, x) for x in drawn_connections[i]]
                    if len(distances) > 0:
                        c_min_distance = min(distances)
                        c_min_index = distances.index(c_min_distance)
                        if c_min_distance <= CONNECTION_CLICKSPOT_RADIUS * 2:
                            c_mesh = i
                            break

                if v_min_distance <= POINT_RADIUS * 2 and v_mesh is not None:
                    print(f"selected mesh {v_mesh}, vertex {v_min_index}")
                    selected_mesh = v_mesh
                    selected_vertex = v_min_index
                    selected_connection = None
                elif c_min_distance <= CONNECTION_CLICKSPOT_RADIUS * 2 and c_mesh is not None:
                    print(f"selected mesh {c_mesh}, connection {c_min_index}")
                    selected_mesh = c_mesh
                    selected_connection = c_min_index
                    selected_vertex = None
                else:
                    selected_mesh = None
                    selected_vertex = None
                    selected_connection = None

                l_mouse_pressed = True
            elif selected_mesh is not None and selected_vertex is not None:
                x_diff = pygame.mouse.get_pos()[0] - last_mouse_pos[0]
                y_diff = pygame.mouse.get_pos()[1] - last_mouse_pos[1]
                screen_pos = drawn_positions[selected_mesh][selected_vertex]
                screen_pos[0] += x_diff
                screen_pos[1] += y_diff
                mesh_list[selected_mesh].vertices[selected_vertex].value = [(drawn_positions[selected_mesh][selected_vertex][0] - x_offset) / SCALE_FACTOR, (((drawn_positions[selected_mesh][selected_vertex][1]) - y_offset) / SCALE_FACTOR) * -1, 1]
            last_mouse_pos = pygame.mouse.get_pos()
        elif l_mouse_pressed:
            l_mouse_pressed = False

        if not mouse_buttons[2]:
            if r_mouse_pressed:
                r_mouse_pressed = False
        else:
            if not r_mouse_pressed:
                r_mouse_pressed = True
            else:
                x_diff = pygame.mouse.get_pos()[0] - last_mouse_pos[0]
                y_diff = pygame.mouse.get_pos()[1] - last_mouse_pos[1]
                x_offset += x_diff
                y_offset += y_diff
            last_mouse_pos = pygame.mouse.get_pos()


    """
    -------------------------DRAWING-------------------------
    """
    screen.fill(BACKGROUND_COLOR)

    drawn_positions = []
    drawn_connections = []
    for m in range(0, len(mesh_list)):
        mesh_connections = []
        for i in range(0, len(mesh_list[m].connections)):
            pos1 = (mesh_list[m].vertices[mesh_list[m].connections[i][0] - 1].value[0] * SCALE_FACTOR + x_offset, (mesh_list[m].vertices[mesh_list[m].connections[i][0] - 1].value[1] * -1) * SCALE_FACTOR + y_offset)
            pos2 = (mesh_list[m].vertices[mesh_list[m].connections[i][1] - 1].value[0] * SCALE_FACTOR + x_offset, (mesh_list[m].vertices[mesh_list[m].connections[i][1] - 1].value[1] * -1) * SCALE_FACTOR + y_offset)
            if m == selected_mesh and i == selected_connection:
                pygame.draw.line(screen, SELECTED_COLOR, pos1, pos2, 3)
            else:
                pygame.draw.line(screen, POINT_COLOR, pos1, pos2, 3)
            mesh_connections.append([(pos1[0] + pos2[0])/2, (pos1[1] + pos2[1])/2])
        drawn_connections.append(mesh_connections)



        mesh_positions = []
        for i in range(0, len(mesh_list[m].vertices)):
            pos = (mesh_list[m].vertices[i].value[0] * SCALE_FACTOR + x_offset, (mesh_list[m].vertices[i].value[1] * -1) * SCALE_FACTOR + y_offset)
            if m == selected_mesh and i == selected_vertex:
                pygame.draw.circle(screen, SELECTED_COLOR, pos, POINT_RADIUS)
            else:
                pygame.draw.circle(screen, POINT_COLOR, pos, POINT_RADIUS)
            mesh_positions.append(list(pos))
        drawn_positions.append(mesh_positions)

    pygame.display.update()

pygame.quit()
exit()