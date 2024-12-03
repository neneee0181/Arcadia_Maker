# 이것은 각 상태들을 객체로 구현한 것임.


from pico2d import get_time, load_image, load_font, \
    draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_DOWN

import src.mode.complate_mode as complate_mode
import src.config.game_world as game_world
import src.config.game_framework as game_framework
from src.config.state_machine import start_event, right_down, left_up, left_down, right_up, space_down, StateMachine, \
    jump_down, jump_up, jump_time_out, jump_denied, down_release, down_press
import src.config.config as config
import src.mode.fail_mode as fail_mode
import src.object.objectO as objectO
import src.config.status as status_

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

    if player.y <= -75:
        game_framework.change_mode(fail_mode)
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
        collision_hide_box(player, player.dir * RUN_SPEED_PPS * game_framework.frame_time)

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
        if player.jump_count < player.jump_count_limit:  # 2단 점프까지만 허용
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
        # 프레임 업데이트
        player.frame = (player.frame + 1 * ACTION_PER_TIME * game_framework.frame_time) % 1

        # 점프 높이 업데이트
        player.y += player.jump_h_force * game_framework.frame_time

        # 좌우 이동 처리
        if SDLK_RIGHT in player.current_keys:  # 오른쪽 키가 눌린 경우
            player.x += RUN_SPEED_PPS * game_framework.frame_time
            player.dir = 1
        elif SDLK_LEFT in player.current_keys:  # 왼쪽 키가 눌린 경우
            player.x -= RUN_SPEED_PPS * game_framework.frame_time
            player.dir = -1

        # 점프 시간이 초과되면 상태 전환
        if get_time() - player.jump_time > player.jump_limit_time:
            player.jump_status = True
            player.state_machine.add_event(('JUMP_TIME_OUT', 0))
            player.jump_h_force = JUMP_FORCE  # 점프 높이 초기화

        # 화면 경계 충돌 처리
        collision_hide_box(player, player.dir * RUN_SPEED_PPS * game_framework.frame_time)

    @staticmethod
    def draw(player):
        if player.dir < 0:
            player.images['alienPink_jump'][int(player.frame)].composite_draw(0, 'h', player.x, player.y, 66, 92)
        else:
            player.images['alienPink_jump'][int(player.frame)].composite_draw(0, '', player.x, player.y, 66, 92)


class Down:
    @staticmethod
    def enter(player, e):
        player.frame = 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.jump_status = True
        pass

    @staticmethod
    def draw(player):
        if player.dir < 0:
            player.images['alienPink_down'][0].composite_draw(0, 'h', player.x, player.y, 66, 92)
        else:
            player.images['alienPink_down'][0].composite_draw(0, '', player.x, player.y, 66, 92)


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
            Player.images['alienPink_down'] = [
                load_image(f"./src/asset/mode/play/player_character/pink/alienPink_down1.png")]

    def __init__(self):
        self.x, self.y = 40, 200
        self.ball_count = 10
        self.frame = 0
        self.dir = 1
        self._gravity = 0.9
        self.jump_time = 0
        self.jump_limit_time = 0.5  # 점프 가능 시간 (늘리면 점프 오래함)
        self.type = "player"
        self.jump_h_force = JUMP_FORCE
        self.current_keys = set()  # 눌린 키를 추적하는 집합
        self.jump_count = 0  # 점프 횟수를 추적
        self.jump_count_limit = 1
        self.jump_status = False  # 점프 상태 false = up, true = down
        self.font = load_font('./src/asset/prac/ENCR10B.TTF', 16)
        self.image = self.load_images()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, jump_down: Jump, jump_up: Jump},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, jump_down: Jump, jump_up: Jump},
                Jump: {jump_time_out: self.decide_next_state},
            }
        )
        self.is_fast_falling = False  # 빠른 낙하 상태 플래그 추가

    # 중력
    def gravity(self):
        if self.is_fast_falling:
            self.y -= self._gravity * 3  # 중력을 3배로 증가시킴
        else:
            self.y -= self._gravity

    def update(self):
        self.gravity()
        self.state_machine.update()
        self._gravity = 0.9

    def handle_event(self, event):
        # 키 입력 상태 업데이트
        if event.type == SDL_KEYDOWN:
            self.current_keys.add(event.key)  # 눌린 키를 추가
            if event.key == SDLK_DOWN:  # 아래 방향키 누름
                self.is_fast_falling = True  # 빠른 낙하 활성화

        elif event.type == SDL_KEYUP:
            self.current_keys.discard(event.key)  # 뗀 키를 제거
            if event.key == SDLK_DOWN:  # 아래 방향키 뗌
                self.is_fast_falling = False  # 빠른 낙하 비활성화

        self.state_machine.add_event(('INPUT', event))

    def decide_next_state(self, e):
        if SDLK_RIGHT in self.current_keys:  # 오른쪽 키가 눌려 있는 경우
            self.dir = 1
            return Run
        elif SDLK_LEFT in self.current_keys:  # 왼쪽 키가 눌려 있는 경우
            self.dir = -1
            return Run
        elif SDLK_DOWN not in self.current_keys:  # 아래 방향키가 떼어진 경우
            return Idle
        else:
            return Idle

    def draw(self):
        self.state_machine.draw()
        if status_.is_bb:
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
                self.is_fast_falling = False
            if other.type == "finish":  # 게임 종료 (성공)
                game_framework.change_mode(complate_mode)
                pass
        if group == "player:monster":
            if self.jump_status:  # 점프 -> 착지 -> 충돌
                self.jump_count = 0
                self.state_machine.start(Jump)
                game_world.remove_object(other)
                self.is_fast_falling = False
            else:  # 게임 종료 (실패)
                game_framework.change_mode(fail_mode)
        if group == "player:Object":  # 오브 젝트 충돌 처리
            for object_type in objectO.object_types:
                if other.type == object_type['name'] and '_jumpO_player' in object_type:  # 점프패드
                    object_type['_jumpO_player'](self, other)
                    self.is_fast_falling = False
                    return
                if other.type == object_type['name'] and '_waterO_player' in object_type:
                    object_type['_waterO_player'](self, other)
                    self.is_fast_falling = False
                    return
                if other.type == object_type['name'] and '_itemO_jump_time_up_player' in object_type:
                    object_type['_itemO_jump_time_up_player'](self, other)
                    self.is_fast_falling = False
                    return
                if other.type == object_type['name'] and '_sticky_blockO_player' in object_type:
                    object_type['_sticky_blockO_player'](self, other)
                    self.is_fast_falling = False
                    return
        pass
