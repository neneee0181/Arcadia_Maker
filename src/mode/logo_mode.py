from pico2d import load_image, get_time, clear_canvas, update_canvas, get_events

import src.config.game_framework as game_framework, src.mode.title_mode as title_mode
import src.config.config as config


def handle_events():
    event = get_events()


def init():
    global image
    global logo_start_time
    image = load_image('./src/asset/tuk_credit.png')
    logo_start_time = get_time()


def finish():
    global image
    del image


def update():
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    image.draw(config.screen_width / 2, config.screen_height / 2, config.screen_width, config.screen_height)
    update_canvas()
