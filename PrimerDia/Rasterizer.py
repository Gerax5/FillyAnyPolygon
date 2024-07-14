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
poligono2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
poligono3 = [(377, 249), (411, 197), (436, 249)]
poligono4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)]
poligono5 = [(682, 175),(708, 120),(735, 148),(739, 170)]

def poligono(listaPoligono, fillColor = None, fill = True):
    for i in range(len(listaPoligono)):
        rend.glLine(listaPoligono[i], listaPoligono[(i + 1) % len(listaPoligono)])
    poligonoTemp = []
    for i in listaPoligono:
        poligonoTemp.append(i)
    cx, cy = rend.centerPolygon(poligonoTemp)
    if fill:
        rend.boundaryfill(cx, cy, fillColor=fillColor)

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
    poligono(poligono2)
    poligono(poligono3)
    poligono(poligono5, fill=False)
    poligono(poligono4)

    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()

#screen.fill((0,0,0))
#pygame.display.flip()
#clock.tick(60)