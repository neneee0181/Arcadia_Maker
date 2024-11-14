from pico2d import load_image, clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDLK_LEFT, SDL_BUTTON_LEFT, \
    SDLK_RETURN
import src.config.game_framework as game_framework, src.play_mode as play_mode
import src.config.config as config


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif  event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_mode(play_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if 1550 <= event.x <= 1890 and 788 <= event.y <= 1048:
                game_framework.change_mode(play_mode)


def init():
    global image
    image = load_image('./src/asset/kenney_pixel-platformer/SampleB2.png')


def finish():
    global image
    del image


def update():
    pass


def draw():
    clear_canvas()
    image.draw(config.screen_width / 2, config.screen_height / 2, config.screen_width, config.screen_height)
    update_canvas()