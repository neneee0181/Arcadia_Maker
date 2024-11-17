from pico2d import *

import src.mode.maker_mode as maker_mode
from src.object.tile import Tile
import src.config.game_world as game_world


class Mouse:
    image_down = None
    image_up = None
    click_status_l = False
    click_status_r = False
    tile = None

    def __init__(self, x=-100, y=-100, velocity=1):
        if Mouse.image_down == None:
            Mouse.image_down = load_image('./src/asset/button/hand_closed.png')
            Mouse.image_up = load_image('./src/asset/button/hand_open.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        if self.click_status_l:
            self.image_down.draw(self.x, self.y)
        else:
            self.image_up.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.x, self.y = event.x, get_canvas_height() - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            self.click_status_l = True
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
            self.click_status_l = False
            self.tile = None
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            self.click_status_r = True
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_RIGHT:
            self.click_status_r = False

    pass

    def update(self):
        pass

    def get_bb(self):
        # fill here
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
        pass

    def handle_collision(self, group, other):
        if self.click_status_l and group == "mouse:tile":
            if self.tile is None:
                self.tile = Tile(
                    id=other.id,
                    x=other.x,  # 초기 X 좌표
                    y=other.y,  # 초기 Y 좌표
                    image=other.image,
                    tile_type=other.tile_type,
                    num_tiles_x=other.num_tiles_x,
                    margin=other.margin,
                    tile_size=other.tile_size,
                    select_num=other.select_num,
                    tt_line=other.tt_line,
                )
                self.tile.selected = True
                game_world.add_object(self.tile, 1)
                game_world.add_collision_pair('mouse:tile_select', None, self.tile)
                maker_mode.maker_tiles.append(self.tile)
        if self.click_status_l and group == "mouse:tile_select" and self.tile is None:
            other.selected = True
            self.tile = other
        pass
