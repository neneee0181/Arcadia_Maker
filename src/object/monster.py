# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, \
    draw_rectangle

import src.config.game_framework as game_framework
import src.config.config as config

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

class Monster:
    images = None

    def load_images(self):
        pass

    def __init__(self):
        self.x, self.y = 40, 200
        self.frame = 0
        self.dir = 1
        self.font = load_font('./src/asset/prac/ENCR10B.TTF', 16)
        self.image = self.load_images()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 34, self.y - 45, self.x + 31, self.y + 47
        pass

    def handle_collision(self, group, other):
        pass
