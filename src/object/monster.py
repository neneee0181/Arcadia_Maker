# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, \
    draw_rectangle
import math
import src.config.game_framework as game_framework
from src.config.behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import src.mode.play_mode as play_mode
from src.object.player import Jump
import src.config.game_world as game_world
import src.config.status as status_

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

monster_types = [{
    'name': "fly_monster_bee",
    'size': 3,
    'rigid_': 5
}]

monster_img_path = "./src/asset/mode/play/monster/"


class Monster:
    images = None

    def load_images(self, image):
        self.images = {}
        for monster_type in monster_types:
            if self.type == monster_type['name']:
                # print([
                #     f"{monster_img_path}{monster_type['name']}/tile_{(self.id + i):04}.png"
                #     for i in range(1, monster_type['size'] + 1)
                # ])
                self.images[monster_type['name']] = [
                    load_image(f"{monster_img_path}{monster_type['name']}/tile_{(self.id + i):04}.png") for i in
                    range(0, monster_type['size'])]
                self.frames_per_action = monster_type['size']  # 이미지 개수
                self.rigid_x1 = self.images[monster_type['name']][0].w + monster_type['rigid_']
                self.rigid_x2 = self.images[monster_type['name']][0].w + monster_type['rigid_']
                self.rigid_y1 = self.images[monster_type['name']][0].h + monster_type['rigid_']
                self.rigid_y2 = self.images[monster_type['name']][0].h + monster_type['rigid_']

    def __init__(self, id, x, y, tile_type, margin, num_tiles_x, image=None,
                 tile_size=20, select_num=40, tt_line=0, type="Unknown"):
        self.x, self.y = x, y
        self.size_x, self.size_y = 0, 0
        self.rigid_x1 = 0
        self.rigid_x2 = 0
        self.rigid_y1 = 0
        self.rigid_y2 = 0
        self.frames_per_action = 8  # 사진 개수
        self.monsterName = None
        self.id = id
        self.frame = 0
        self.dir = 1
        self.tile_type = tile_type
        self.margin = margin
        self.num_tiles_x = num_tiles_x
        self.type = type
        self.load_images(image)
        self.tile_size = tile_size
        self.select_num = select_num
        self.tt_line = tt_line
        self.build_behavior_tree()  # ai

    def update(self):
        self.frame = (self.frame + self.frames_per_action
                      * ACTION_PER_TIME * game_framework.frame_time) % self.frames_per_action
        self.bt.run()
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        if self.dir < 0:
            self.images[self.type][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 66, 92)
        else:
            self.images[self.type][int(self.frame)].composite_draw(0, '', self.x, self.y, 66, 92)
        if status_.is_bb:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return (self.x - self.rigid_x1, self.y - self.rigid_y1,
                self.x + self.rigid_x2, self.y + self.rigid_y2)
        pass

    def handle_collision(self, group, other):
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2
        pass

    def is_player_nearby(self, distance):
        if self.distance_less_than(play_mode.new_player.x, play_mode.new_player.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        pass

    def move_to_boy(self, r=0.5):  # monster -> player
        self.move_slightly_to(play_mode.new_player.x, play_mode.new_player.y)
        if (self.distance_less_than(play_mode.new_player.x, play_mode.new_player.y, self.x, self.y, r)):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def build_behavior_tree(self):
        if self.type == monster_types[0]['name']:  # bee 일때
            c1 = Condition('player 근처에 있는가?', self.is_player_nearby, 5)
            a4 = Action('player에게 접근', self.move_to_boy)
            root = chase_boy = Sequence('player 추적', c1, a4)

        self.bt = BehaviorTree(root)
        pass
