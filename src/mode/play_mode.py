import random

from pico2d import *
import src.config.game_framework as game_framework
import src.config.config as config
from src.object.tile import Tile

import src.object.player as player
import src.config.game_world as game_world

load_tiles = []

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    game_world.clear()
    global bottom_line_ui
    bottom_line_ui = load_image("./src/asset/mode/maker/bottom_line.png")

    global tiles
    tiles = []
    for make_tile in load_tiles:
        try:
            tile = Tile(
                id=make_tile['id'],
                x=make_tile['x'],
                y=make_tile['y'] - 200,
                tile_type=make_tile['tile_type'],
                num_tiles_x=make_tile['num_tiles_x'],
                margin=make_tile['margin'],
                image=load_image(f"./src/asset/{make_tile['tile_type']}/Tiles/tile_{make_tile['id']:04}.png"),
                tile_size=make_tile['tile_size'],
                select_num=make_tile['select_num'],
                tt_line=make_tile['tt_line']
            )
            tiles.append(tile)  # Tile 객체를 리스트에 추가
        except OSError:
            print(f"Cannot load image: ./src/asset/{make_tile['tile_type']}/Tiles/tile_{make_tile['id']:04}.png")
            tiles.append(None)  # 로드 실패 시 None 추가

    game_world.add_objects(tiles, 2)

    global player
    player = player.Player()
    game_world.add_object(player, 1)

    pass

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    bottom_line_ui.draw(config.screen_width / 2, 1, config.screen_width, bottom_line_ui.h)
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass