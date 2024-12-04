import random

from pico2d import *

import src.config.game_framework as game_framework
import src.config.config as config
from src.object.tile import Tile
import src.object.player as player
import src.config.game_world as game_world
import src.mode.select_mode as select_mode
import src.object.monster as monster
import src.object.objectO as objectO

load_tiles = []


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            bgm.stop()
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            bgm.stop()
            game_world.clear_collision_pairs()
            game_world.clear()
            game_framework.push_mode(select_mode)
        else:
            new_player.handle_event(event)


def init():
    global bgm
    music_path = f"./src/asset/sound/play/background_music{random.randint(1, 3)}.mp3"  # 파일 경로 생성
    bgm = load_music(music_path)
    bgm.set_volume(config.sound_size)
    bgm.repeat_play()

    game_world.clear_collision_pairs()
    game_world.clear()
    global bottom_line_ui
    bottom_line_ui = load_image("./src/asset/mode/maker/bottom_line.png")

    global monsters
    monsters = []
    global tiles
    tiles = []
    global objects
    objects = []

    for make_tile in load_tiles:
        try:
            if any(monster_type['name'] == make_tile['type'] for monster_type in monster.monster_types):  # 몬스터 생성
                new_monster = monster.Monster(
                    id=make_tile['id'],
                    x=make_tile['x'],
                    y=make_tile['y'] - 200,
                    tile_type=make_tile['tile_type'],
                    num_tiles_x=make_tile['num_tiles_x'],
                    margin=make_tile['margin'],
                    image=f"./src/asset/{make_tile['tile_type']}/Tiles/tile_{make_tile['id']:04}.png",
                    tile_size=make_tile['tile_size'],
                    select_num=make_tile['select_num'],
                    tt_line=make_tile['tt_line'],
                    type=make_tile['type']
                )
                monsters.append(new_monster)
                continue
            if any(object_type['name'] == make_tile['type'] for object_type in objectO.object_types):  # 점프패드, water
                new_object = objectO.ObjectO(
                    id=make_tile['id'],
                    x=make_tile['x'],
                    y=make_tile['y'] - 200,
                    tile_type=make_tile['tile_type'],
                    num_tiles_x=make_tile['num_tiles_x'],
                    margin=make_tile['margin'],
                    image=f"./src/asset/{make_tile['tile_type']}/Tiles/tile_{make_tile['id']:04}.png",
                    tile_size=make_tile['tile_size'],
                    select_num=make_tile['select_num'],
                    tt_line=make_tile['tt_line'],
                    type=make_tile['type']
                )
                objects.append(new_object)
                continue
            tile = Tile(
                id=make_tile['id'],
                x=make_tile['x'],
                y=make_tile['y'] - 200,
                tile_type=make_tile['tile_type'],
                num_tiles_x=make_tile['num_tiles_x'],
                margin=make_tile['margin'],
                image=load_image(f"./src/asset/{make_tile['tile_type']}/Tiles/tile_{make_tile['id']:04}.png"),
                tile_size=make_tile['tile_size'],
                select_num=make_tile['select_num'],
                tt_line=make_tile['tt_line'],
                type=make_tile['type']
            )
            tiles.append(tile)  # Tile 객체를 리스트에 추가
        except OSError:
            print(f"Cannot load image: ./src/asset/{make_tile['tile_type']}/Tiles/tile_{make_tile['id']:04}.png")
            tiles.append(None)  # 로드 실패 시 None 추가

    game_world.add_objects(objects, 2)
    game_world.add_objects(tiles, 2)
    game_world.add_objects(monsters, 2)

    for tile in tiles:
        game_world.add_collision_pair('player:tile', None, tile)
    for monster_c in monsters:
        game_world.add_collision_pair('player:monster', None, monster_c)
    for object_c in objects:
        game_world.add_collision_pair('player:Object', None, object_c)

    global new_player
    try:
        new_player = player.Player()
        print("Player initialized successfully.")  # 디버깅 로그
    except Exception as e:
        print(f"Error during Player initialization: {e}")  # 예외 내용 출력
        return  # 예외 발생 시 초기화 중단

    try:
        game_world.add_object(new_player, 1)
        print("Player added to game_world.")
    except Exception as e:
        print(f"Error adding Player to game_world: {e}")
    game_world.add_collision_pair('player:tile', new_player, None)
    game_world.add_collision_pair('player:monster', new_player, None)
    game_world.add_collision_pair('player:Object', new_player, None)
    pass


def finish():
    game_world.clear()
    bgm.stop()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    bottom_line_ui.draw(config.screen_width / 2, 1, config.screen_width, bottom_line_ui.h)
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
