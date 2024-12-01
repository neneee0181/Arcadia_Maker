# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, \
    draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT

import src.config.game_framework as game_framework
from src.config.state_machine import start_event, right_down, left_up, left_down, right_up, space_down, StateMachine, \
    jump_down, jump_up, jump_time_out

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
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir = -1

        player.jump_time = get_time()

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1 * ACTION_PER_TIME * game_framework.frame_time) % 1

        if player.dir == -1:
            player.y -= player.dir * RUN_SPEED_PPS * game_framework.frame_time * 2
        else:
            player.y += player.dir * RUN_SPEED_PPS * game_framework.frame_time * 2
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - player.jump_time > 0.5:
            player.state_machine.add_event(('JUMP_TIME_OUT', 0))

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
        self.x, self.y = 400, 400
        self.ball_count = 10
        self.frame = 0
        self.dir = 1
        self._gravity = 0.3
        self.jump_time = 0
        self.current_keys = set()  # 눌린 키를 추적하는 집합
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
            self.y += self._gravity + 0.1
        pass
