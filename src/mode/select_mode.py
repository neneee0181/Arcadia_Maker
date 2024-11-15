from pico2d import load_image, clear_canvas, update_canvas, get_events, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, \
    SDLK_RETURN, SDLK_UP, SDLK_DOWN
import src.config.game_framework as game_framework, src.mode.play_mode as play_mode
import src.config.config as config

def handle_events():
    global running, selected_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            selected_num = selected_num + 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            selected_num = selected_num - 1


def init():
    global background_image
    background_image = load_image('./src/asset/kenney_platformer-pack-redux/Sample1.png')
    global font
    global selected_mode
    global selected_num
    font = load_font('./src/asset/prac/ENCR10B.TTF', 16)
    selected_mode = ["Load Game", "Make Game", "Quit"]
    selected_num = 0
    pass


def finish():
    global background_image
    del background_image
    pass

def update():
    pass


def draw():
    clear_canvas()
    background_image.draw(config.screen_width / 2, config.screen_height / 2, config.screen_width, config.screen_height)
    font.draw(50, 50, f'{10:02d}', (0, 255, 0))
    update_canvas()
