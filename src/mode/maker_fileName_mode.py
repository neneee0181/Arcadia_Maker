from pico2d import *
import src.config.game_framework as game_framework
import src.mode.maker_mode as maker_mode
import src.config.game_world as game_world

maker_tiles = []

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_world.clear()
            game_framework.change_mode(maker_mode)


def init():
    pass


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    update_canvas()


def pause():
    pass


def resume():
    pass
