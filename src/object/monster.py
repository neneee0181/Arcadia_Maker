import random

from pico2d import get_time, load_image, load_font, \
    draw_rectangle
import math
import src.config.game_framework as game_framework
from src.config.behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import src.mode.play_mode as play_mode
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

monster_img_path = "./src/asset/mode/play/monster"

monster_types = [{
    'name': "fly_monster_bee",
    'size': 3,
    'rigid_': 5,
    '_beeO_object': None,
    '_beeO_player': None,
    'load_images': [
        f"{monster_img_path}/fly_monster_bee/tile_0180.png",
        f"{monster_img_path}/fly_monster_bee/tile_0181.png",
        f"{monster_img_path}/fly_monster_bee/tile_0182.png"
    ],
    'ai_status': True,
    'inversion': 'h'
}, {
    'name': "water_monster_fishi",
    'size': 2,
    'rigid_': 5,
    '_fishiO_object': None,
    '_fishiO_player': None,
    'load_images': [
        f"{monster_img_path}/water_monster_fishi/tile_0014.png",
        f"{monster_img_path}/water_monster_fishi/tile_0013.png",
    ],
    'ai_status': True,
    'inversion': 'v'
}, {
    'name': "block_monster_block",
    'size': 1,
    'rigid_': 5,
    '_blockO_object': None,
    '_blockO_player': None,
    'ai_status': True,
    'inversion': 'h',
    'load_images': [
        f"{monster_img_path}/block_monster_block/tile_0013.png",
        f"{monster_img_path}/block_monster_block/tile_0013.png",
        f"{monster_img_path}/block_monster_block/tile_0012.png",
    ],
}]


class Monster:
    images = None

    def load_images(self, image):
        self.images = {}
        for monster_type in monster_types:
            if self.type == monster_type['name']:
                # load_images 키가 없으면 기본값 처리
                if 'load_images' in monster_type and monster_type['load_images']:
                    self.images[monster_type['name']] = [
                        load_image(image_path) for image_path in monster_type['load_images']
                    ]
                else:
                    # load_images가 없으면 단일 이미지로 로드
                    self.images[monster_type['name']] = [load_image(image)]
                self.frames_per_action = monster_type['size']  # 이미지 개수
                self.inversion = monster_type['inversion']
                # 모든 이미지의 크기를 확인하고 가장 큰 크기를 기준으로 설정
                max_width = 0
                max_height = 0
                for img in self.images[monster_type['name']]:
                    max_width = max(max_width, img.w)
                    max_height = max(max_height, img.h)

                self.frames_per_action = monster_type['size']  # 이미지 개수
                self.rigid_x1 = max_width + monster_type['rigid_']
                self.rigid_x2 = max_width + monster_type['rigid_']
                self.rigid_y1 = max_height + monster_type['rigid_']
                self.rigid_y2 = max_height + monster_type['rigid_']

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
        self.inversion = 'h'
        self.load_images(image)
        self.tile_size = tile_size
        self.select_num = select_num
        self.tt_line = tt_line
        # ai_status 확인 후 BehaviorTree 초기화
        monster_type = next((m for m in monster_types if m['name'] == self.type), None)
        if monster_type and monster_type.get('ai_status', False):  # ai_status가 True인지 확인
            self.build_behavior_tree()  # AI 초기화
        else:
            self.bt = None  # AI가 없을 경우 bt를 None으로 설정
        self.initial_y = self.y  # 초기 위치 저장 (물고기 이동)
        self.target_y = self.initial_y + random.randint(200, 400)  # 랜덤 이동 높이 설정

    def update(self):
        self.frame = (self.frame + self.frames_per_action
                      * ACTION_PER_TIME * game_framework.frame_time) % self.frames_per_action
        # bt가 초기화된 경우에만 실행
        if self.bt:
            self.bt.run()
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        if self.dir < 0:
            self.images[self.type][int(self.frame)].composite_draw(0, self.inversion, self.x, self.y, self.tile_size,
                                                                   self.tile_size)
        else:
            self.images[self.type][int(self.frame)].composite_draw(0, '', self.x, self.y, self.tile_size,
                                                                   self.tile_size)
        if config.is_bb:
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

    def move_h(self, h=400):
        # 방향에 따라 이동
        if self.dir == -1:  # 아래로 이동
            if self.y > self.initial_y:
                self.y -= RUN_SPEED_PPS * game_framework.frame_time * 1.2
            else:  # 제자리로 돌아왔으면 방향 전환
                self.dir = 1
                self.target_y = self.initial_y + random.randint(200, 400)  # 새로운 랜덤 높이 설정
        elif self.dir == 1:  # 위로 이동
            if self.y < self.target_y:
                self.y += RUN_SPEED_PPS * game_framework.frame_time * 1.3
            else:  # 목표 지점에 도달했으면 방향 전환
                self.dir = -1

        return BehaviorTree.RUNNING

    def change_img(self):
        self.frame = 2
        pass

    def build_behavior_tree(self):
        if self.type == monster_types[0]['name']:  # bee 일때
            c1 = Condition('player 근처에 있는가?', self.is_player_nearby, 5)
            a4 = Action('player에게 접근', self.move_to_boy)
            root = chase_boy = Sequence('player 추적', c1, a4)
            self.bt = BehaviorTree(root)
        elif self.type == monster_types[1]['name']:  # fishi 일때
            a1 = Action('물고기가 위에서 아래로 이동', self.move_h)
            root = move_f = Sequence('물고기 상하 이동', a1)
            self.bt = BehaviorTree(root)
        elif self.type == monster_types[2]['name']:  # block 일때
            c1 = Condition('player 근처에 있는가?', self.is_player_nearby, 9)
            a1 = Action('박스 이미지 변경', self.change_img)
            root = move_f = Sequence('근처에 있으면 박스 얼굴 변경', c1, a1)
            self.bt = BehaviorTree(root)
