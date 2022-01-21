from numba import njit
import math
from config import *
import sys
import json
from classes import *
from resources import *

pg.init()
flags = pg.FULLSCREEN
window = pg.display.set_mode((W, H), flags, vsync=1)
pg.display.set_caption(TITLE)
clock = pg.time.Clock()


x, y = 0, 0
time = 0
map_x = 0
map_y = 0
map_x_d = 0
map_y_d = 0

entities = []
backgrounds = []
statics = []
transports = []
buttons = []


def update_game():
    global map_x, map_y, map_y_d, map_x_d
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_ESCAPE:
                menu(True)
            if i.key in [pg.K_d, pg.K_RIGHT]:
                map_x_d = MAP_SPEED
            if i.key in [pg.K_a, pg.K_LEFT]:
                map_x_d = -MAP_SPEED
            if i.key in [pg.K_w, pg.K_UP]:
                map_y_d = -MAP_SPEED
            if i.key in [pg.K_s, pg.K_DOWN]:
                map_y_d = MAP_SPEED
        if i.type == pg.KEYUP:
            if i.key in [pg.K_d, pg.K_RIGHT]:
                map_x_d = 0
            if i.key in [pg.K_a, pg.K_LEFT]:
                map_x_d = 0
            if i.key in [pg.K_w, pg.K_UP]:
                map_y_d = 0
            if i.key in [pg.K_s, pg.K_DOWN]:
                map_y_d = 0
        if i.type == pg.MOUSEBUTTONDOWN:
            for btn in buttons:
                if i.pos[0] > btn.xy[0] and i.pos[1] > btn.xy[1]:
                    if i.pos[0] < btn.xy[0] + btn.width and i.pos[1] < btn.xy[1] + btn.height:
                        if btn.arg == 'non':
                            btn.f()
                        else:
                            btn.f(btn.arg)
    map_y += map_y_d
    map_x += map_x_d


def render_game():
    window.blit(background_game, (0, 0))
    for bg in backgrounds:
        window.blit(background_img[bg.biome], (bg.xy[0] + map_x, bg.xy[1] + map_y))
    for btn in buttons:
        window.blit(btn.img, btn.xy)


gaming = False


def game_exit():
    global gaming
    gaming = False
    buttons.clear()
    img = pg.image.load("img/newgame.jpg")
    tempbtn = Button(400, 200, 424, 76, img, "default")
    tempbtn.f = load_game
    buttons.append(tempbtn)
    img = pg.image.load("img/exit.jpg")
    tempbtn = Button(400, 500, 323, 147, img, "non")
    tempbtn.f = sys.exit
    buttons.append(tempbtn)


def game():
    global gaming
    buttons.clear()
    gaming = True
    while gaming:
        clock.tick(FPS)
        update_game()
        render_game()
        pg.display.update()


def load_game(name):
    global entities, backgrounds, statics, transports
    with open("save/" + name + ".json", "r") as read_file:
        loaded = json.load(read_file)
    entities.clear()
    for i in loaded['entities']:
        entities.append(Entity(i['xy'][0], i['xy'][1], i["sprite"], i['speed'], i['backpack'],
                               i['backpack_size'], i['job'], i['need'], i['tip']))
    backgrounds.clear()
    for i in loaded['backgrounds']:
        backgrounds.append(Background(i['xy'][0], i['xy'][1], i["biome"]))
    statics.clear()
    for i in loaded['statics']:
        statics.append(Static(i['xy'][0], i['xy'][1], i["sprite"]))
    transports.clear()
    for i in loaded['transports']:
        transports.append(Transport(i['xy'][0], i['xy'][1], i["sprite"], i['tip']))
    if m_e:
        map_editor()
    else:
        game()


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
    print('game save')


def update_menu():
    global window, x, y, time
    time += 0.25
    x = math.sin(time/(95*1)) * 500
    y = math.cos(time/(100*1)) * 600
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_ESCAPE and not gaming:
                sys.exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            for btn in buttons:
                if i.pos[0] > btn.xy[0] and i.pos[1] > btn.xy[1]:
                    if i.pos[0] < btn.xy[0] + btn.width and i.pos[1] < btn.xy[1] + btn.height:
                        if btn.arg == 'non':
                            btn.f()
                        else:
                            btn.f(btn.arg)


def render_menu(in_game):
    global x, y
    if not in_game:
        window.blit(background_menu, (0, 0))
    for btn in buttons:
        window.blit(btn.img, btn.xy)
    # pg.draw.circle(window, (225, 225, 0), (510 + x, 650 + y), 1)


def menu(in_game):
    if in_game:
        buttons.clear()
        img = pg.image.load("img/exit.jpg")
        tempbtn = Button(400, 500, 323, 147, img, "non")
        tempbtn.f = game_exit
        buttons.append(tempbtn)
    else:
        buttons.clear()
        img = pg.image.load("img/newgame.jpg")
        tempbtn = Button(400, 200, 424, 76, img, "default")
        tempbtn.f = load_game
        buttons.append(tempbtn)
        img = pg.image.load("img/exit.jpg")
        tempbtn = Button(400, 500, 323, 147, img, "non")
        tempbtn.f = sys.exit
        buttons.append(tempbtn)

    while in_game == gaming:
        clock.tick(FPS)
        update_menu()
        render_menu(in_game)
        pg.display.update()


is_test = True


def test():
    pass


def update_map_editor():
    global map_x, map_y, map_y_d, map_x_d
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_ESCAPE:
                sys.exit()
            if i.key in [pg.K_d, pg.K_RIGHT]:
                map_x_d = MAP_SPEED
            if i.key in [pg.K_a, pg.K_LEFT]:
                map_x_d = -MAP_SPEED
            if i.key in [pg.K_w, pg.K_UP]:
                map_y_d = -MAP_SPEED
            if i.key in [pg.K_s, pg.K_DOWN]:
                map_y_d = MAP_SPEED
        if i.type == pg.KEYUP:
            if i.key in [pg.K_d, pg.K_RIGHT]:
                map_x_d = 0
            if i.key in [pg.K_a, pg.K_LEFT]:
                map_x_d = 0
            if i.key in [pg.K_w, pg.K_UP]:
                map_y_d = 0
            if i.key in [pg.K_s, pg.K_DOWN]:
                map_y_d = 0
        if i.type == pg.MOUSEMOTION:
            cursor_map_editor.xy = (i.pos[0] - i.pos[0] % 32 + map_x % 32, i.pos[1] - i.pos[1] % 32 + map_y % 32)
        if i.type == pg.MOUSEBUTTONDOWN:
            save = False
            for btn in buttons:
                if i.pos[0] > btn.xy[0] and i.pos[1] > btn.xy[1]:
                    if i.pos[0] < btn.xy[0] + btn.width and i.pos[1] < btn.xy[1] + btn.height:
                        save = True
                        if btn.arg == 'non':
                            btn.f()
                        else:
                            btn.f(btn.arg)
            if not save:
                for bg in backgrounds:
                    if bg.xy == (cursor_map_editor.xy[0] - map_x, cursor_map_editor.xy[1] - map_y):
                        backgrounds.remove(bg)
                        print('del')
                backgrounds.append(Background(cursor_map_editor.xy[0] - map_x, cursor_map_editor.xy[1] - map_y,
                                              cursor_map_editor.biome))
    map_y += map_y_d
    map_x += map_x_d


cursor_map_editor = Background(100, 100, 'grass')


def cursor_grass():
    cursor_map_editor.biome = 'grass'


def cursor_water():
    cursor_map_editor.biome = 'water'


def map_editor():
    buttons.clear()
    img = pg.image.load("img/save_button.jpg")
    img = pg.transform.scale(img, (128, 32))
    tempbtn = Button(W-128, H-32, 128, 32, img, "default")
    tempbtn.f = save_game
    buttons.append(tempbtn)
    img = pg.image.load("img/grass.jpg")
    tempbtn = Button(W - 160, H - 32, 32, 32, img, "non")
    tempbtn.f = cursor_grass
    buttons.append(tempbtn)
    img = pg.image.load("img/water.jpg")
    tempbtn = Button(W - 192, H - 32, 32, 32, img, "non")
    tempbtn.f = cursor_water
    buttons.append(tempbtn)
    while True:
        clock.tick(FPS)
        update_map_editor()
        render_game()
        window.blit(background_img[cursor_map_editor.biome], cursor_map_editor.xy)
        pg.draw.rect(window, (255, 255, 255), (cursor_map_editor.xy[0], cursor_map_editor.xy[1], 32, 32), 1)
        pg.display.update()


m_e = True
if m_e:
    load_game('default')
else:
    menu(False)


