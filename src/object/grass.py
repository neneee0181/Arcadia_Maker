from pico2d import *


class Grass:
    def __init__(self):
        self.image = load_image('./src/asset/prac/grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)

    def get_bb(self):
        # fill here
        return 0, 0, 1600 - 1, 50
        pass