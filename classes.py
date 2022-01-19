
class Entity:
    def __init__(self, x, y, sprite, speed, backpack, backpack_size, job, need):
        self.xy = (x, y)
        self.sprite = sprite
        self.speed = speed
        self.backpack = backpack
        self.backpack_size = backpack_size
        self.job = job
        self.need = need

    def update(self):
        pass

    def render(self):
        pass


class Background:
    def __init__(self, x, y, biome):
        self.xy = x, y
        self.biome = biome


class Static:
    def __init__(self, x, y, img):
        self.xy = x, y
        self.sprite = img


class Transport:
    def __init__(self, x, y, sprite, tip):
        self.xy = x, y
        self.sprite = sprite
        self.tip = tip


class Button:
    def __init__(self, x, y, width, height, img, arg):
        self.xy = x, y
        self.width = width
        self.height = height
        self.img = img
        self.arg = arg

    def f(self):
        pass

