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
selected_mesh = None
selected_vertex = None
l_mouse_pressed = False
r_mouse_pressed = False
last_mouse_pos = None
x_offset = 400
y_offset = 400

mesh_list = [read_obj("./assets/Curve_1.obj"), Mesh([Element([3, 0, 1])])]

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



run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_PLUS:
                SCALE_FACTOR = min(MAX_SCALE_FACTOR, SCALE_FACTOR * SCALE_STEP)
            if event.key == K_MINUS:
                SCALE_FACTOR = max(MIN_SCALE_FACTOR, SCALE_FACTOR / SCALE_STEP)

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            if not l_mouse_pressed:
                for i in range(0, len(drawn_positions)):
                    mouse_pos = pygame.mouse.get_pos()
                    distances = [euclidean_distance(mouse_pos, x) for x in drawn_positions[i]]
                    min_distance = min(distances)
                    min_index = distances.index(min_distance)
                    if min_distance <= POINT_RADIUS * 2:
                        print(f"selected mesh {i}, vertex {min_index}")
                        selected_mesh = i
                        selected_vertex = min_index
                l_mouse_pressed = True
            else:
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


    screen.fill(BACKGROUND_COLOR)

    drawn_positions = []
    for m in range(0, len(mesh_list)):
        for c in mesh_list[m].connections:
            pos1 = (mesh_list[m].vertices[c[0] - 1].value[0] * SCALE_FACTOR + x_offset, (mesh_list[m].vertices[c[0] - 1].value[1] * -1) * SCALE_FACTOR + y_offset)
            pos2 = (mesh_list[m].vertices[c[1] - 1].value[0] * SCALE_FACTOR + x_offset, (mesh_list[m].vertices[c[1] - 1].value[1] * -1) * SCALE_FACTOR + y_offset)
            pygame.draw.line(screen, POINT_COLOR, pos1, pos2, 3)


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