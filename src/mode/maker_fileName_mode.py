from pico2d import *
import src.config.game_framework as game_framework
import src.mode.maker_mode as maker_mode
import src.config.game_world as game_world

maker_tiles = []


def make_file():
    # Tile 객체를 딕셔너리로 변환
    data = [tile.to_dict() for tile in maker_tiles]

    # JSON 파일로 저장
    with open(f"export/{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Data exported to maker_tiles.json")
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_world.clear()
            game_framework.change_mode(maker_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            make_file()


def init():
    global file_name
    file_name = 'export_game'
    pass


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    update_canvas()


def pause():
    pass


def resume():
    pass
