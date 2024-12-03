from pico2d import *
import src.config.game_framework as game_framework
import src.mode.select_mode as select_mode
import src.config.game_world as game_world
import src.config.config as config


def handle_events():
    events = get_events()
    global file_name

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key is None:  # key가 None이면 무시
                continue
            if event.key == SDLK_RETURN:
                game_world.clear()
                game_world.clear_collision_pairs()
                game_framework.change_mode(select_mode)
                pass


def init():

    global success_font
    success_font = load_font('./src/asset/font/SourGummy-VariableFont_wdth,wght.ttf', 56)

    global keyboard_img_return
    keyboard_img_return = load_image('./src/asset/mode/select/keyboard_enter.png')
    pass


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    success_font.draw(config.screen_width / 2 - 70, config.screen_height / 2,
                      f'Fail!!', (255, 100, 100))
    keyboard_img_return.draw(config.screen_width - 100, 105, keyboard_img_return.w - 30, keyboard_img_return.h - 30)
    update_canvas()


def pause():
    pass


def resume():
    pass
