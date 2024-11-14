from pico2d import load_image, get_time, clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
import src.config.game_framework as game_framework, src.config.play_mode as play_mode


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif  event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
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
    image.draw(400, 300)
    update_canvas()