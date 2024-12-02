# 이것은 각 상태들을 객체로 구현한 것임.


from pico2d import get_time, load_image, load_font, \
    draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT

import src.mode.complate_mode as complate_mode
import src.config.game_world as game_world
import src.config.game_framework as game_framework
from src.config.state_machine import start_event, right_down, left_up, left_down, right_up, space_down, StateMachine, \
    jump_down, jump_up, jump_time_out, jump_denied
import src.config.config as config
import src.mode.fail_mode as fail_mode

# 점프 크기 상수 추가
SCREEN_HEIGHT = config.screen_height
PIXEL_PER_METER = SCREEN_HEIGHT / 30  # 30m 기준
JUMP_FORCE = 20 * PIXEL_PER_METER  # 점프 높이 (15m)

# player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def collision_hide_box(player, xy):
    if player.x <= 0:
        player.x -= xy
    elif player.x >= config.screen_width:
        player.x -= xy
    pass


class Idle:
    @staticmethod
    def enter(player, e):
        player.frame = 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 2 * ACTION_PER_TIME * game_framework.frame_time) % 2

    @staticmethod
    def draw(player):
        if player.dir < 0:
            player.images['alienPink_stand'][int(player.frame)].composite_draw(0, 'h', player.x, player.y, 66, 92)
        else:
            player.images['alienPink_stand'][int(player.frame)].composite_draw(0, '', player.x, player.y, 66, 92)


class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir = -1

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.fire_ball()

    @staticmethod
    def do(player):
        player.frame = (player.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        collision_hide_box(player, player.dir * RUN_SPEED_PPS * game_framework.frame_time)
        pass

    @staticmethod
    def draw(player):
        if player.dir < 0:
            player.images['alienPink_walk'][int(player.frame)].composite_draw(0, 'h', player.x, player.y, 66, 92)
        else:
            player.images['alienPink_walk'][int(player.frame)].composite_draw(0, '', player.x, player.y, 66, 92)


class Jump:
    @staticmethod
    def enter(player, e):
        if player.jump_count < 1:  # 2단 점프까지만 허용
            player.jump_status = False
            if right_down(e) or left_up(e):  # 오른쪽으로 RUN
                player.dir = 1
            elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
                player.dir = -1
            player.jump_time = get_time()
            player.jump_count += 1  # 점프 횟수 증가
        else:
            player.state_machine.add_event(('JUMP_DENIED', 0))

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1 * ACTION_PER_TIME * game_framework.frame_time) % 1

        player.y += JUMP_FORCE * game_framework.frame_time

        if SDLK_RIGHT in player.current_keys or SDLK_LEFT in player.current_keys:  # 오른쪽 키가 눌려 있는 경우
            player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - player.jump_time > 0.5:
            player.jump_status = True
            player.state_machine.add_event(('JUMP_TIME_OUT', 0))
        collision_hide_box(player, player.dir * RUN_SPEED_PPS * game_framework.frame_time)
        pass

    @staticmethod
    def draw(player):
        if player.dir < 0:
            player.images['alienPink_jump'][int(player.frame)].composite_draw(0, 'h', player.x, player.y, 66, 92)
        else:
            player.images['alienPink_jump'][int(player.frame)].composite_draw(0, '', player.x, player.y, 66, 92)


class Player:
    images = None

    def load_images(self):
        if Player.images == None:
            Player.images = {}
            Player.images['alienPink_stand'] = [
                load_image(f"./src/asset/mode/play/player_character/pink/alienPink_stand{i}.png") for i in range(1, 3)]
            Player.images['alienPink_walk'] = [
                load_image(f"./src/asset/mode/play/player_character/pink/alienPink_walk{i}.png") for i in range(1, 4)]
            Player.images['alienPink_jump'] = [
                load_image(f"./src/asset/mode/play/player_character/pink/alienPink_jump{i}.png") for i in range(1, 4)]

    def __init__(self):
        self.x, self.y = 40, 200
        self.ball_count = 10
        self.frame = 0
        self.dir = 1
        self._gravity = 0.9
        self.jump_time = 0
        self.current_keys = set()  # 눌린 키를 추적하는 집합
        self.jump_count = 0  # 점프 횟수를 추적
        self.jump_status = False  # 점프 상태 false = up, true = down
        self.font = load_font('./src/asset/prac/ENCR10B.TTF', 16)
        self.image = self.load_images()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, jump_down: Jump, jump_up: Jump},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, jump_down: Jump, jump_up: Jump},
                Jump: {jump_time_out: self.decide_next_state}
            }
        )

    # 중력
    def gravity(self):
        self.y -= self._gravity

    def update(self):
        self.gravity()
        self.state_machine.update()

    def handle_event(self, event):
        # 키 입력 상태 업데이트
        if event.type == SDL_KEYDOWN:
            self.current_keys.add(event.key)  # 눌린 키를 추가
        elif event.type == SDL_KEYUP:
            self.current_keys.discard(event.key)  # 뗀 키를 제거

        self.state_machine.add_event(('INPUT', event))
        pass

    def decide_next_state(self, e):
        # 눌린 키 상태에 따라 다음 상태 결정
        if SDLK_RIGHT in self.current_keys:  # 오른쪽 키가 눌려 있는 경우
            self.dir = 1
            return Run
        elif SDLK_LEFT in self.current_keys:  # 왼쪽 키가 눌려 있는 경우
            self.dir = -1
            return Run
        else:
            return Idle

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 34, self.y - 45, self.x + 31, self.y + 47
        pass

    def handle_collision(self, group, other):
        if group == 'player:tile':
            if other.type == "ground":  # 땅
                self.y += self._gravity + 0.05
                self.jump_count = 0  # 충돌 시 점프 횟수 초기화
                self.jump_status = False
            if other.type == "finish":  # 게임 종료 (성공)
                game_framework.change_mode(complate_mode)
                pass
        if group == "player:monster":
            if self.jump_status:  # 점프 -> 착지 -> 충돌
                self.jump_count = 0
                self.state_machine.start(Jump)
                game_world.remove_object(other)
            else:  # 게임 종료 (실패)
                game_framework.change_mode(fail_mode)

        pass
