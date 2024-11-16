import random

from pico2d import *
import src.config.game_framework as game_framework

import src.config.game_world as game_world
import src.mode.select_mode as select_mode
import src.config.config as config


def ui_init():
    global bottom_line_ui
    bottom_line_ui = load_image("./src/asset/mode/maker/bottom_line.png")

    tile_width = config.screen_width // 10  # 한 줄에 최대 10개
    tile_height = config.screen_height // 10  # 한 열에 최대 10개
    # tiles에 이미지 로드
    global tiles
    tiles = [None] * 179
    for i in range(179):
        try:
            image = load_image(f"./src/asset/kenney_pixel-platformer/Tiles/tile_{i:04}.png")
            tile_info = {
                "image": image,  # 이미지 객체
                "x": (i % 10) * tile_width + tile_width // 2,  # X 좌표
                "y": config.screen_height - ((i // 10) * tile_height + tile_height // 2),  # Y 좌표
                "tile_cnt_w": 10,
                "tile_cnt_h": 10
            }
            tiles[i] = tile_info
        except OSError:
            print(f"Cannot load image: ./src/asset/kenney_pixel-platformer/Tiles/tile_{i:04}.png")
            tiles[i] = None
    pass


def ui_draw():
    bottom_line_ui.draw(config.screen_width / 2, 100, config.screen_width, bottom_line_ui.h)

    # tiles를 화면에 그리기 (예: 10개씩 줄 맞춰 출력)
    for i in range(179):
        if tiles[i]:  # None이 아닌 경우에만 그리기
            tiles[i]["image"].draw(tiles[i]["x"], tiles[i]["y"], config.screen_width // tiles[i]["tile_cnt_w"],
                                   config.screen_height // tiles[i]["tile_cnt_h"])
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_mode)


def init():
    ui_init()
    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    ui_draw()
    update_canvas()


def pause():
    pass


def resume():
    pass
