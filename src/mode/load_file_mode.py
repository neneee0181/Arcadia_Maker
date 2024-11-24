from pico2d import *
import src.config.game_framework as game_framework
import src.mode.maker_mode as maker_mode
import src.config.game_world as game_world
import src.config.config as config
import src.mode.play_mode as play_mode

maker_tiles = []

def load_file():
    global file_name  # 현재 입력받은 파일 이름

    if file_name == '':
        print("파일 이름이 비어있습니다.")
        return

    file_path = f'./map/{file_name}.json'  # 파일 경로 구성
    try:
        # JSON 파일 읽기
        with open(file_path, 'r') as file:
            data = json.load(file)

        # JSON 데이터에서 타일 정보 추출 및 Tile 객체 생성
        if len(data) > 0:
            print(f"파일 '{file_name}'을 성공적으로 로드했습니다!")
            play_mode.load_tiles = data
            game_framework.change_mode(play_mode)


    except FileNotFoundError:
        print(f"파일 '{file_name}'을 찾을 수 없습니다. 경로를 확인하세요.")
    except json.JSONDecodeError:
        print(f"파일 '{file_name}'의 JSON 형식이 잘못되었습니다.")
    except KeyError as e:
        print(f"파일에 필요한 키가 없습니다: {e}")
    except Exception as e:
        print(f"파일 로드 중 알 수 없는 오류 발생: {e}")

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
                load_file()
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
