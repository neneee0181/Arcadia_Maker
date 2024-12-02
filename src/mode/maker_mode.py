from pico2d import *
import src.config.game_framework as game_framework

import src.config.game_world as game_world
import src.mode.select_mode as select_mode
import src.config.config as config
import src.mode.maker_fileName_mode as maker_fileName_mode
from src.object.mouse import Mouse
from src.object.tile import Tile
from PIL import Image

import os

maker_tiles = []


def load_tiles_with_metadata(folder_path):
    tiles_ = []
    i = 0  # 직접 관리할 인덱스 변수
    for file_name in os.listdir(folder_path):
        try:
            # 폴더인지 확인 (폴더는 무시)
            full_path = os.path.join(folder_path, file_name)
            if not os.path.isfile(full_path):  # 폴더는 무시
                print(f"Skipping folder: {file_name}")
                continue  # 폴더는 스킵

            # 파일 열기
            image = Image.open(full_path)

            # 메타데이터에서 태그 읽기
            metadata = image.info
            tile_type = metadata.get("type", "unknown")  # 'type' 메타데이터가 없으면 기본값 'unknown'

            # 이미지를 Pico2d용으로 로드
            pico2d_image = load_image(full_path)

            # Tile 객체 생성
            tile = Tile(
                id=i,
                x=-100,  # 초기 좌표
                y=-100,  # 초기 좌표
                tile_type="kenney_pixel-platformer",
                margin=5,
                num_tiles_x=20,
                image=pico2d_image,
                type=tile_type,
            )
            tile.tt_line = 9
            tile.tile_size = (config.screen_width - (tile.num_tiles_x - 1) * tile.margin) // tile.num_tiles_x
            tile.x = (i % tile.num_tiles_x) * (tile.tile_size + tile.margin) + tile.tile_size // 2
            tile.y = 200 - ((i // tile.num_tiles_x) * (tile.tile_size + tile.margin)) - (
                    tile.tile_size // 2) - tile.margin
            tiles_.append(tile)
            # print(f"Loaded tile ID {tile.id} with type '{tile_type}'")
            i += 1  # 타일을 성공적으로 추가했을 때만 i 증가
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    return tiles_


def ui_init():
    global bottom_line_ui
    bottom_line_ui = load_image("./src/asset/mode/maker/bottom_line.png")

    global tiles
    tiles = load_tiles_with_metadata("./src/asset/kenney_pixel-platformer/Tiles")  # 경로 수정
    game_world.add_objects(tiles, 1)

    for tile in tiles:
        game_world.add_collision_pair('mouse:tile', None, tile)

    pass


def ui_draw():
    bottom_line_ui.draw(config.screen_width / 2, 200, config.screen_width, bottom_line_ui.h)
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_world.clear_collision_pairs()
            game_framework.change_mode(select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            for tile in tiles:
                if tile.num_tiles_x * tile.tt_line < tile.select_num:
                    return
                tile.select_num += tile.num_tiles_x
                tile.y += tile.tile_size + tile.margin
                pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            for tile in tiles:
                if tile.num_tiles_x * 2 > tile.select_num:
                    return
                tile.select_num -= tile.num_tiles_x
                tile.y -= tile.tile_size + tile.margin
                pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:  # map
            maker_fileName_mode.maker_tiles = maker_tiles
            game_world.clear()
            game_world.clear_collision_pairs()
            game_framework.change_mode(maker_fileName_mode)
            pass
        else:
            mouse.handle_event(event)


def init():
    maker_tiles.clear()
    ui_init()
    global mouse
    mouse = Mouse()
    game_world.add_object(mouse, 2)
    game_world.add_collision_pair('mouse:tile', mouse, None)
    game_world.add_collision_pair('mouse:tile_select', mouse, None)

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
