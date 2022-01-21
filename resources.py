import pygame as pg
from screeninfo import get_monitors

W = get_monitors()[0].width
H = get_monitors()[0].height


background_menu = pg.image.load("img/background_menu.jpg")
background_menu = pg.transform.scale(background_menu, (W, H))
background_game = pg.image.load("img/background_game.jpg")
background_game = pg.transform.scale(background_game, (W, H))

background_img = {
    "water": pg.image.load("img/water.jpg"),
    "grass": pg.image.load("img/grass.jpg")
}




