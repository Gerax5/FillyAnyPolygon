import pygame
from pygame.locals import *
from gl import Render

width = 960
height = 540

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rend = Render(screen)

rend.glColor(0.5, 1, 1)
#rend.glClearColor(0.5, 1, 1)

poligono1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]

def poligono(listaPoligono):
    for i in range(len(listaPoligono)):
        rend.glLine(listaPoligono[i], listaPoligono[(i + 1) % len(listaPoligono)])

isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rend.glClear()

    #for i in range(100):
    #    rend.glPoint(480 + i,270 + i)

    # for x in range(0, width, 20):
    #     rend.glLine((0,0), (x, height))
    #     rend.glLine((0, height - 1), (x, 0))
    #     rend.glLine((width - 1, 0), (x, height))
    #     rend.glLine((width - 1, height - 1), (x, 0))
    poligono(poligono1)

    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()

#screen.fill((0,0,0))
#pygame.display.flip()
#clock.tick(60)