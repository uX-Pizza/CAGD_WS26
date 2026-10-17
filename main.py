from asyncio import timeout

import pygame
from pygame.locals import *
from pygame import freetype
from sys import exit

from ObjectReader import read_obj



pygame.init()
screen = pygame.display.set_mode((800, 800))

mesh_list = [read_obj("./assets/Curve_1.obj")]

SCALE_FACTOR = 10
SCALE_STEP = 1.75
MAX_SCALE_FACTOR = 30
MIN_SCALE_FACTOR = 1
X_OFFSET = 400
Y_OFFSET = 400



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


    screen.fill((255, 255, 255))

    for mesh in mesh_list:
        for i in range(0, len(mesh.vertices)):
            pos = (mesh.vertices[i].value[0] * SCALE_FACTOR + X_OFFSET, (mesh.vertices[i].value[1] * -1) * SCALE_FACTOR + Y_OFFSET)
            # inverse transform: mesh.vertices[i].value[0], pos[0] / SCALE_FACTOR - X_OFFSET
            pygame.draw.circle(screen, (0, 0, 0), pos, 5)

        for c in mesh.connections:
            pos1 = (mesh.vertices[c[0] - 1].value[0] * SCALE_FACTOR + X_OFFSET, (mesh.vertices[c[0] - 1].value[1] * -1) * SCALE_FACTOR + Y_OFFSET)
            pos2 = (mesh.vertices[c[1] - 1].value[0] * SCALE_FACTOR + X_OFFSET, (mesh.vertices[c[1] - 1].value[1] * -1) * SCALE_FACTOR + Y_OFFSET)
            pygame.draw.line(screen, (0, 0, 0), pos1, pos2, 3)


    pygame.display.update()

pygame.quit()
exit()