from pico2d import *
import src.config.game_framework as game_framework

import src.config.game_world as game_world
import src.mode.select_mode as select_mode
import src.config.config as config
import src.mode.maker_fileName_mode as maker_fileName_mode
from src.object.mouse import Mouse
from src.object.tile import Tile

maker_tiles = []


def ui_init():
    global bottom_line_ui
    bottom_line_ui = load_image("./src/asset/mode/maker/bottom_line.png")

    global tiles
    tiles = []
    for i in range(179):
        try:
            image = load_image(f"./src/asset/kenney_pixel-platformer/Tiles/tile_{i:04}.png")
            tile = Tile(
                id=i,
                x=-100,  # 초기 X 좌표
                y=-100,  # 초기 Y 좌표
                tile_type="kenney_pixel-platformer",
                margin=5,
                num_tiles_x=20,
                image = image,
            )
            tile.tt_line = 9
            tile.tile_size = (config.screen_width - (tile.num_tiles_x - 1) * tile.margin) // tile.num_tiles_x
            tile.x = (i % tile.num_tiles_x) * (tile.tile_size + tile.margin) + tile.tile_size // 2
            tile.y = 200 - ((i // tile.num_tiles_x) * (tile.tile_size + tile.margin)) - (
                    tile.tile_size // 2) - tile.margin
            tiles.append(tile)  # 배열에 추가
        except OSError:
            print(f"Cannot load image: ./src/asset/kenney_pixel-platformer/Tiles/tile_{i:04}.png")
            tiles.append(None)  # 로드 실패 시 None 추가
    game_world.add_objects(tiles, 1)

    for tile in tiles:
        game_world.add_collision_pair('mouse:tile', None, tile)

    # if len(maker_tiles) > 0:
    #     for make_tile in maker_tiles:
    #         tile = Tile(
    #             id=make_tile.id,
    #             x=make_tile.x, y=make_tile.y,
    #             image=make_tile.image,
    #             tile_type=make_tile.tile_type,
    #             num_tiles_x=make_tile.num_tiles_x,
    #             margin=make_tile.margin,
    #             tile_size=make_tile.tile_size,
    #             select_num=make_tile.select_num,
    #             tt_line=make_tile.tt_line,
    #         )
    #         game_world.add_object(tile, 1)
    #         game_world.add_collision_pair('mouse:tile_select', None, tile)
    #         pass

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:  # export
            maker_fileName_mode.maker_tiles = maker_tiles
            game_world.clear()
            game_world.clear_collision_pairs()
            game_framework.change_mode(maker_fileName_mode)
            pass
        else:
            mouse.handle_event(event)


def init():
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
