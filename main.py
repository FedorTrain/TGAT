import math
from numba import njit
import pygame as pg
from config import FPS, TITLE
import sys
from screeninfo import get_monitors

W = get_monitors()[0].width
H = get_monitors()[0].height

pg.init()
flags = pg.FULLSCREEN
window = pg.display.set_mode((W, H), flags, vsync=1)
pg.display.set_caption(TITLE)
clock = pg.time.Clock()
background_menu = pg.image.load("img/background_menu.jpg")
background_menu = pg.transform.scale(background_menu, (W, H))

x, y = 0, 0
time = 0


def update_menu():
    global window, x, y, time
    time += 1
    x = math.sin(time/100) * 100
    y = math.cos(time/100) * 100
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_ESCAPE:
                sys.exit()


def render_menu():
    global x, y
    window.blit(background_menu, (0, 0))
    pg.draw.circle(window, (225, 225, 0), (300 + x, 300 + y), 30)


def menu():

    while True:
        clock.tick(FPS)
        update_menu()
        render_menu()
        pg.display.update()


menu()
