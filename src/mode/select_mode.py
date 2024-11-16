from pico2d import load_image, clear_canvas, update_canvas, get_events, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, \
    SDLK_RETURN, SDLK_UP, SDLK_DOWN
import src.config.game_framework as game_framework
import src.config.config as config
import src.mode.maker_mode as maker_mode
import src.mode.title_mode as title_mode

def handle_events():
    global running, selected_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if selected_num == 2:
                selected_num = 0
            else:
                selected_num = selected_num + 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if selected_num == 0:
                selected_num = 2
            else:
                selected_num = selected_num - 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            if selected_num == 0:
                pass
            elif selected_num == 1:
                game_framework.change_mode(maker_mode)
                pass
            elif selected_num == 2:
                game_framework.quit()


def init():
    global background_image
    background_image = load_image('./src/asset/mode/select/Sample1.png')
    global selected_img1
    selected_img1 = load_image('./src/asset/mode/select/divider-000-green.png')
    global keyboard_img_arrow, keyboard_img_return
    keyboard_img_arrow = load_image('./src/asset/mode/select/keyboard_arrows_vertical.png')
    keyboard_img_return = load_image('./src/asset/mode/select/keyboard_enter.png')
    global font
    global selected_mode
    global selected_num
    font = load_font('./src/asset/font/SourGummy-VariableFont_wdth,wght.ttf', 56)
    selected_mode = [
        {"mode": "Load Game", "value": 130},
        {"mode": "Make Game", "value": 130},
        {"mode": "Quit", "value": 50}
    ]
    selected_num = 0
    pass


def finish():
    global background_image
    del background_image
    global keyboard_img_arrow, keyboard_img_return, font
    del keyboard_img_arrow
    del keyboard_img_return
    del font
    pass


def update():
    pass


def draw():
    clear_canvas()
    background_image.draw(config.screen_width / 2, config.screen_height / 2, config.screen_width, config.screen_height)
    selected_img1.clip_composite_draw(0, 0,
                                      selected_img1.w, selected_img1.h,
                                      0,
                                      '',
                                      config.screen_width / 2 - 400, config.screen_height / 2,
                                      selected_img1.w + 50, selected_img1.h + 0)
    # 좌우 반전
    selected_img1.clip_composite_draw(0, 0,
                                      selected_img1.w, selected_img1.h,
                                      0,
                                      'h',
                                      config.screen_width / 2 + 400, config.screen_height / 2,
                                      selected_img1.w + 50, selected_img1.h + 0)
    keyboard_img_arrow.draw(config.screen_width - 200, 100)
    keyboard_img_return.draw(config.screen_width - 100, 105, keyboard_img_arrow.w - 30, keyboard_img_arrow.h - 30)
    font.draw(config.screen_width / 2 - selected_mode[selected_num]["value"], config.screen_height / 2,
              f'{selected_mode[selected_num]["mode"]}', (0, 255, 0))
    update_canvas()
