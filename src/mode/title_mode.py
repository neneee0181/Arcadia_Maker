from pico2d import load_image, clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, \
    SDLK_RETURN, SDLK_b
import src.config.game_framework as game_framework
import src.config.config as config
import src.mode.select_mode as select_mode
from src.object.mouse import Mouse
import src.config.game_world as game_world

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif  event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_mode(select_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if 1550 <= event.x <= 1890 and 788 <= event.y <= 1048:
                game_framework.change_mode(select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            config.is_bb = not config.is_bb


def init():
    global image
    image = load_image('./src/asset/mode/title/SampleB2.png')

    mouse = Mouse()
    game_world.add_object(mouse, 1)


def finish():
    global image
    del image
    game_world.clear()


def update():
    game_world.update()
    pass


def draw():
    clear_canvas()
    image.draw(config.screen_width / 2, config.screen_height / 2, config.screen_width, config.screen_height)
    game_world.render()
    update_canvas()