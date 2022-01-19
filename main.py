from numba import njit
import math
import pygame as pg
from config import FPS, TITLE
import sys
from screeninfo import get_monitors
import json
from game import *

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

entities = []
backgrounds = []
statics = []
transports = []
buttons = []


def load_game(name):
    global entities, backgrounds, statics, transports
    with open("save/" + name + ".json", "r") as read_file:
        loaded = json.load(read_file)
    entities.clear()
    for i in loaded['entities']:
        entities.append(Entity(i['xy'][0], i['xy'][1], i["sprite"], i['speed'], i['backpack'],
                               i['backpack_size'], i['job'], i['need']))
    backgrounds.clear()
    for i in loaded['backgrounds']:
        backgrounds.append(Background(i['xy'][0], i['xy'][1], i["biome"]))
    statics.clear()
    for i in loaded['statics']:
        statics.append(Static(i['xy'][0], i['xy'][1], i["sprite"]))
    transports.clear()
    for i in loaded['transports']:
        transports.append(Transport(i['xy'][0], i['xy'][1], i["sprite"], i['tip']))


def save_game(name):
    global entities, backgrounds, statics, transports
    data = {
        "entities": [vars(item) for item in entities],
        "backgrounds": [vars(item) for item in backgrounds],
        "statics": [vars(item) for item in statics],
        "transports": [vars(item) for item in transports]
    }
    with open("save/" + name + ".json", "w") as write_file:
        json.dump(data, write_file, indent=2)


def update_menu():
    global window, x, y, time
    time += 1
    x = math.sin(time/100) * 100
    y = math.cos(time/100) * 100
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_ESCAPE:
                sys.exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            for btn in buttons:
                if i.pos[0] > btn.xy[0] and i.pos[1] > btn.xy[1]:
                    if i.pos[0] < btn.xy[0] + btn.width and i.pos[1] < btn.xy[1] + btn.height:
                        if btn.arg == 'non':
                            btn.f()
                        else:
                            btn.f(btn.arg)


def render_menu():
    global x, y
    window.blit(background_menu, (0, 0))
    for btn in buttons:
        window.blit(btn.img, btn.xy)
    #pg.draw.circle(window, (225, 225, 0), (300 + x, 300 + y), 30)


def menu():
    buttons.clear()
    img = pg.image.load("img/newgame.jpg")
    tempbtn = Button(400, 200, 424, 76, img, "default")
    tempbtn.f = load_game
    buttons.append(tempbtn)
    img = pg.image.load("img/exit.jpg")
    tempbtn = Button(400, 500, 323, 147, img, "non")
    tempbtn.f = sys.exit
    buttons.append(tempbtn)

    while True:
        clock.tick(FPS)
        update_menu()
        render_menu()
        pg.display.update()


def test():
    load_game("default")
    save_game("default")
    load_game("default")
    save_game("default")
    load_game("default")
    save_game("default")
    load_game("default")

menu()


