# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, \
    draw_rectangle

from src.object.ball import Ball
import src.config.game_world as game_world
import src.config.game_framework as game_framework
from src.config.state_machine import start_event, right_down, left_up, left_down, right_up, space_down, StateMachine, \
    time_out

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
        player.wait_time = get_time()

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


class Sleep:
    @staticmethod
    def enter(player, e):
        if start_event(e):
            player.face_dir = 1
            player.action = 3
        player.frame = 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # player.frame = (player.frame + 1) % 8
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_composite_draw(int(player.frame) * 100, 300, 100, 100,
                                             3.141592 / 2, '', player.x - 25, player.y - 25, 100, 100)
        else:
            player.image.clip_composite_draw(int(player.frame) * 100, 200, 100, 100,
                                             -3.141592 / 2, '', player.x + 25, player.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(player, e):
        print(1)
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir= -1

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.fire_ball()

    @staticmethod
    def do(player):
        player.frame = (player.frame + 2 * ACTION_PER_TIME * game_framework.frame_time) % 2
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player):
        if player.dir < 0:
            player.images['alienPink_stand'][int(player.frame)].composite_draw(0, 'h', player.x, player.y, 66, 92)
        else:
            player.images['alienPink_stand'][int(player.frame)].composite_draw(0, '', player.x, player.y, 66, 92)


animation_stand = ['alienPink_stand']

class Player:
    images = None

    def load_images(self):
        if Player.images == None:
            Player.images = {}
            Player.images['alienPink_stand'] = [
                load_image(f"./src/asset/mode/play/player_character/pink/alienPink_stand{i}.png") for i in range(1, 3)]

    def __init__(self):
        self.x, self.y = 400, 400
        self.ball_count = 10
        self.frame = 0
        self.dir = 1
        self.font = load_font('./src/asset/prac/ENCR10B.TTF', 16)
        self.image = self.load_images()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                # Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50
        pass

    def handle_collision(self, group, other):
        pass
