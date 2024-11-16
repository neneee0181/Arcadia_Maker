from pico2d import *


class Tile:
    tile_size = 20

    def __init__(self, id, x, y, image, tile_type, margin, num_tiles_x):
        self.id = id
        self.x = x
        self.y = y
        self.image = image
        self.type = tile_type
        self.margin = margin
        self.num_tiles_x = num_tiles_x

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.tile_size, self.tile_size)
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        return self.x, self.y, self.x, self.y
