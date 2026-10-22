import pygame
from pygame.locals import *
from sys import exit
import math

from ObjectReader import read_obj
from CartesianElements import Element
from Mesh import Mesh



pygame.init()
screen = pygame.display.set_mode((800, 800))
font = pygame.font.Font()
drawn_positions = []
drawn_connections = []
new_connection_start = []
new_connection_active = False
selected_mesh = None
selected_vertex = None
selected_connection = None
l_mouse_pressed = False
r_mouse_pressed = False
last_mouse_pos = None
x_offset = 400
y_offset = 400

mesh_list = [read_obj("./assets/Curve_1.obj"), Mesh([Element([3, 0, 1]), Element([1, 3, 1])], [(1, 2)])]

SCALE_FACTOR = 10
SCALE_STEP = 1.75
MAX_SCALE_FACTOR = 30.0
MIN_SCALE_FACTOR = 1.0
GRID_STEP = 5

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
            if event.key == K_c:
                if selected_mesh is not None and selected_vertex is not None:
                    new_connection_active = not new_connection_active
                    new_connection_start = [selected_mesh, selected_vertex]


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

                if new_connection_active and selected_mesh == new_connection_start[0] and selected_vertex != new_connection_start[1]:
                    conn = (new_connection_start[1] + 1, selected_vertex + 1)
                    rconn = (selected_vertex + 1, new_connection_start[1] + 1)
                    if conn not in mesh_list[selected_mesh].connections and rconn not in mesh_list[selected_mesh].connections:
                        mesh_list[selected_mesh].connections.append((new_connection_start[1] + 1, selected_vertex + 1))
                else:
                    new_connection_start = []
                    new_connection_active = False

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

    axis_color = (200, 200, 200)

    line_lenght = 12
    max_world_zoom = int(400 / SCALE_FACTOR)
    start_world = (max_world_zoom // GRID_STEP) * GRID_STEP
    step_world = 10

    pygame.draw.line(screen, (200, 200, 200), (0, y_offset), (800, y_offset), 1)
    pygame.draw.line(screen, (200, 200, 200), (x_offset, 0), (x_offset, 800), 1)

    for i in range(-start_world, start_world + 1, GRID_STEP):
        screen_x = x_offset + (i * SCALE_FACTOR)
        pygame.draw.line(screen, axis_color, (screen_x, y_offset + line_lenght), (screen_x, y_offset - line_lenght), 1)
        label = str(i)
        text_surface = pygame.font.Font().render(label,True, axis_color)
        screen.blit(text_surface, (screen_x - 10, y_offset + line_lenght + 2))

    for i in range(-start_world, start_world, GRID_STEP):
        if i != 0:
            screen_y = y_offset + (i * SCALE_FACTOR * -1)

            pygame.draw.line(screen, axis_color, (x_offset - line_lenght,  screen_y), (x_offset + line_lenght, screen_y), 1)
            label = str( i* -1)
            text_surface = font.render(label,True, axis_color)
            screen.blit(text_surface, (x_offset + line_lenght + 5, screen_y - 7))

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