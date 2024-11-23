import random

from pico2d import *
import src.config.game_framework as game_framework
import src.config.config as config

import src.config.game_world as game_world

maker_tiles = []

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            pass

def init():
    global bottom_line_ui
    bottom_line_ui = load_image("./src/asset/mode/maker/bottom_line.png")

    for i in range(len(maker_tiles)):
        maker_tiles[i].image = load_image(f"./src/asset/{maker_tiles[i].tile_type}/Tiles/tile_{i:04}.png")
        print(f"Index: {i}, Tile: {maker_tiles[i]}, img : {maker_tiles[i].image}")

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    #bottom_line_ui.draw(config.screen_width / 2, 200, config.screen_width, bottom_line_ui.h)
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass