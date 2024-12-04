from pico2d import *

import src.config.game_world as game_world
import src.config.config as config
import src.mode.maker_mode as maker_mode


class Tile:
    tile_size = 20  # 기본 타일 사이즈
    select_num = 40  # 화면에 보이는 전체 개수
    tt_line = 0  # 타일 전체 줄수 -> ex 9개
    selected = False

    def __init__(self, id, x, y, tile_type, margin, num_tiles_x, image=None, tile_size=20, select_num=40, tt_line=0,
                 type=""):
        self.id = id
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.margin = margin
        self.num_tiles_x = num_tiles_x
        self.image = image
        self.tile_size = tile_size
        self.select_num = select_num
        self.tt_line = tt_line
        self.type = type

    def update(self):
        pass

    def draw(self):
        if self.select_num > self.id >= self.select_num - 40:
            self.image.draw(self.x, self.y, self.tile_size, self.tile_size)
        if config.is_bb:
            draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):

        if group == "mouse:tile_select" and other.click_status_l is False:
            self.selected = False
        if self.selected and group == "mouse:tile_select" and other.click_status_l:
            if self.id == other.tile.id:
                self.x, self.y = other.x, other.y
        elif group == "mouse:tile_select" and other.click_status_r:
            game_world.remove_object(self)
            game_world.remove_collision_object(self)
            """maker_mode의 maker_tiles에서 자신의 id와 동일한 타일을 찾아 삭제"""
            for tile in maker_mode.maker_tiles:
                if tile.id == self.id:
                    maker_mode.maker_tiles.remove(tile)
                    print(f"Tile with id {self.id} removed from maker_tiles.")
                    break
            else:
                print(f"Tile with id {self.id} not found in maker_tiles.")
        if group == "player:tile":
            pass
        pass

    def get_bb(self):
        if self.select_num > self.id >= self.select_num - 40:
            return self.x - self.tile_size // 2, self.y - self.tile_size // 2, self.x + self.tile_size // 2, self.y + self.tile_size // 2
        else:
            return 0, 0, 0, 0

    def to_dict(self):
        """객체를 딕셔너리 형태로 변환"""
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "tile_type": self.tile_type,
            "margin": self.margin,
            "num_tiles_x": self.num_tiles_x,
            "tile_size": self.tile_size,
            "select_num": self.select_num,
            "tt_line": self.tt_line,
            "type": self.type
        }
