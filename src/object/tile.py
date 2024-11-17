from pico2d import *

import src.config.game_world as game_world


class Tile:
    tile_size = 20  # 기본 타일 사이즈
    select_num = 40  # 화면에 보이는 전체 개수
    tt_line = 0  # 타일 전체 줄수 -> ex 9개
    selected = False

    def __init__(self, id, x, y, image, tile_type, margin, num_tiles_x, tile_size=20, select_num=40, tt_line=0):
        self.id = id
        self.x = x
        self.y = y
        self.image = image
        self.tile_type = tile_type
        self.margin = margin
        self.num_tiles_x = num_tiles_x
        self.tile_size = tile_size
        self.select_num = select_num
        self.tt_line = tt_line

    def update(self):
        pass

    def draw(self):
        if self.select_num > self.id >= self.select_num - 40:
            self.image.draw(self.x, self.y, self.tile_size, self.tile_size)
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if other.click_status_l is False and group == "mouse:tile_select":
            self.selected = False
        if self.selected and other.click_status_l and group == "mouse:tile_select":
            if self.id == other.tile.id:
                self.x, self.y = other.x, other.y
        elif other.click_status_r and group == "mouse:tile_select":
            game_world.remove_object(self)
            game_world.remove_collision_object(self)
        pass

    def get_bb(self):
        if self.select_num > self.id >= self.select_num - 40:
            return self.x - self.tile_size // 2, self.y - self.tile_size // 2, self.x + self.tile_size // 2, self.y + self.tile_size // 2
        else:
            return 0, 0, 0, 0
