from asyncio import timeout

import pygame
from pygame.locals import *
from pygame import freetype
from sys import exit

from ObjectReader import read_obj



pygame.init()
screen = pygame.display.set_mode((800, 800))

meshes = read_obj("./assets/Curve_1.obj")

SCALE_FACTOR = 10
SCALE_STEP = 4
MAX_SCALE_FACTOR = 30
MIN_SCALE_FACTOR = 1
X_OFFSET = 400 / SCALE_FACTOR
Y_OFFSET = 400 / SCALE_FACTOR



run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_PLUS:
                SCALE_FACTOR = min(MAX_SCALE_FACTOR, SCALE_FACTOR + SCALE_STEP)
            if event.key == K_MINUS:
                SCALE_FACTOR = max(MIN_SCALE_FACTOR, SCALE_FACTOR - SCALE_STEP)
            X_OFFSET = 400 / SCALE_FACTOR
            Y_OFFSET = 400 / SCALE_FACTOR

    screen.fill((255, 255, 255))

    for v in meshes.vertices:
        pos = ((v.value[0] + X_OFFSET) * SCALE_FACTOR, ((v.value[1] * -1) + Y_OFFSET) * SCALE_FACTOR)
        pygame.draw.circle(screen, (0, 0, 0), pos, 5)

    for c in meshes.connections:
        pos1 = ((meshes.vertices[c[0] - 1].value[0] + X_OFFSET) * SCALE_FACTOR, (meshes.vertices[c[0] - 1].value[1] + Y_OFFSET) * SCALE_FACTOR)
        pos2 = ((meshes.vertices[c[1] - 1].value[0] + X_OFFSET) * SCALE_FACTOR, (meshes.vertices[c[1] - 1].value[1] + Y_OFFSET) * SCALE_FACTOR)
        pygame.draw.line(screen, (0, 0, 0), pos1, pos2, 3)


    pygame.display.update()

pygame.quit()
exit()