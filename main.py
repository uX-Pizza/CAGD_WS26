from asyncio import timeout

import pygame
from pygame.locals import *
from pygame import freetype
from sys import exit
import math

from ObjectReader import read_obj



pygame.init()
screen = pygame.display.set_mode((800, 800))
drawn_positions = []
selected_mesh = None
selected_vertex = None

mesh_list = [read_obj("./assets/Curve_1.obj")]

SCALE_FACTOR = 10
SCALE_STEP = 1.75
MAX_SCALE_FACTOR = 30.0
MIN_SCALE_FACTOR = 1.0
X_OFFSET = 400
Y_OFFSET = 400

POINT_RADIUS = 5
BACKGROUND_COLOR = (255, 255, 255)
POINT_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)



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
            for i in range(0, len(drawn_positions)):
                mouse_pos = pygame.mouse.get_pos()
                distances = [euclidean_distance(mouse_pos, x) for x in drawn_positions[i]]
                min_distance = min(distances)
                min_index = distances.index(min_distance)
                if min_distance <= POINT_RADIUS * 2:
                    print(f"selected mesh {i}, vertex {min_index}")
                    selected_mesh = i
                    selected_vertex = min_index

    screen.fill(BACKGROUND_COLOR)

    drawn_positions = []
    for m in range(0, len(mesh_list)):
        for c in mesh_list[m].connections:
            pos1 = (mesh_list[m].vertices[c[0] - 1].value[0] * SCALE_FACTOR + X_OFFSET, (mesh_list[m].vertices[c[0] - 1].value[1] * -1) * SCALE_FACTOR + Y_OFFSET)
            pos2 = (mesh_list[m].vertices[c[1] - 1].value[0] * SCALE_FACTOR + X_OFFSET, (mesh_list[m].vertices[c[1] - 1].value[1] * -1) * SCALE_FACTOR + Y_OFFSET)
            pygame.draw.line(screen, POINT_COLOR, pos1, pos2, 3)


        mesh_positions = []
        for i in range(0, len(mesh_list[m].vertices)):
            pos = (mesh_list[m].vertices[i].value[0] * SCALE_FACTOR + X_OFFSET, (mesh_list[m].vertices[i].value[1] * -1) * SCALE_FACTOR + Y_OFFSET)
            # inverse transform: mesh.vertices[i].value[0], pos[0] / SCALE_FACTOR - X_OFFSET
            if m == selected_mesh and i == selected_vertex:
                pygame.draw.circle(screen, SELECTED_COLOR, pos, POINT_RADIUS)
            else:
                pygame.draw.circle(screen, POINT_COLOR, pos, POINT_RADIUS)
            mesh_positions.append(pos)

        drawn_positions.append(mesh_positions)

    pygame.display.update()

pygame.quit()
exit()