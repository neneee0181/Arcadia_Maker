from pico2d import *
import src.config.game_framework as game_framework
import src.mode.maker_mode as maker_mode
import src.config.game_world as game_world
import src.config.config as config
import src.mode.select_mode as select_mode

maker_tiles = []


def make_file():
    # Tile 객체를 딕셔너리로 변환
    if file_name == '':
        print("파일 이름이 비어있습니다.")
        return

    data = [tile.to_dict() for tile in maker_tiles]

    # JSON 파일로 저장
    with open(f"map/{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Data exported to maker_tiles.json")
    pass


def handle_events():
    events = get_events()
    global file_name

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key is None:  # key가 None이면 무시
                continue

            if event.key == SDLK_ESCAPE:
                game_world.clear()
                game_framework.change_mode(maker_mode)
            elif event.key == SDLK_RETURN:
                make_file()
                game_world.clear()
                game_framework.change_mode(select_mode)
            elif event.key == SDLK_BACKSPACE or event.key == 8:  # Backspace 처리
                if len(file_name) > 0:
                    file_name = file_name[:-1]
            elif 32 <= event.key <= 126:  # ASCII 출력 가능한 문자만 추가
                file_name += chr(event.key)


def init():
    global file_name
    file_name = ''
    global file_name_font
    file_name_font = load_font('./src/asset/font/SourGummy-VariableFont_wdth,wght.ttf', 56)
    global file_name_result
    file_name_result = load_font('./src/asset/font/SourGummy-VariableFont_wdth,wght.ttf', 56)

    global keyboard_img_return
    keyboard_img_return = load_image('./src/asset/mode/select/keyboard_enter.png')
    pass


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    file_name_font.draw(config.screen_width / 2 - 400, config.screen_height / 2,
                        f'File Name : ', (100, 255, 100))
    file_name_font.draw(config.screen_width / 2 - 100, config.screen_height / 2,
                        f'{file_name}', (0, 0, 0))
    keyboard_img_return.draw(config.screen_width - 100, 105, keyboard_img_return.w - 30, keyboard_img_return.h - 30)
    update_canvas()


def pause():
    pass


def resume():
    pass
