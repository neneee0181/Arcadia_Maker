from pico2d import *
import src.config.game_framework as game_framework

import src.config.game_world as game_world
import src.mode.select_mode as select_mode
import src.config.config as config
from src.object.mouse import Mouse


def ui_init():
    global bottom_line_ui
    bottom_line_ui = load_image("./src/asset/mode/maker/bottom_line.png")

    # tiles에 이미지 로드
    global tiles
    tiles = [None] * 179
    for i in range(179):
        try:
            image = load_image(f"./src/asset/kenney_pixel-platformer/Tiles/tile_{i:04}.png")
            tile_info = {
                "id": i,
                "image": image,  # 이미지 객체
                "type": "kenney_pixel-platformer",
                "margin": 5,
                "num_tiles_x": 20,
                "x": -100,
                "y": -100,
            }
            tiles[i] = tile_info
        except OSError:
            print(f"Cannot load image: ./src/asset/kenney_pixel-platformer/Tiles/tile_{i:04}.png")
            tiles[i] = None
    pass


def ui_draw():
    bottom_line_ui.draw(config.screen_width / 2, 200, config.screen_width, bottom_line_ui.h)

    for i in range(tile_h_num, 179):
        if tiles[i]:
            num_tiles_x = tiles[i]["num_tiles_x"]
            margin = tiles[i]["margin"]
            tile_size = (config.screen_width - (num_tiles_x - 1) * margin) // num_tiles_x
            # 타일 위치 계산
            x = (i % num_tiles_x) * (tile_size + margin) + tile_size // 2
            y = 200 - (((i - tile_h_num) // num_tiles_x) * (tile_size + margin)) - (tile_size // 2) - margin
            tiles[i]["image"].draw(x, y, tile_size, tile_size)
    pass


def handle_events():
    events = get_events()
    global tile_h_num

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            tile_h_num = max(tile_h_num - 20, 0)  # 0 이하로 내려가지 않도록 제한
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            tile_h_num = min(tile_h_num + 20, 179)  # 179 이상으로 올라가지 않도록 제한
        else:
            mouse.handle_event(event)


def init():
    global tile_h_num
    tile_h_num = 0

    ui_init()

    global mouse
    mouse = Mouse()
    game_world.add_object(mouse, 1)

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    ui_draw()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
