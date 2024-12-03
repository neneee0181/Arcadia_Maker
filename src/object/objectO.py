# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, \
    draw_rectangle
import math

from sdl2 import SDLK_RIGHT, SDLK_LEFT

import src.config.game_framework as game_framework
import src.config.status as status_
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


def jumpO_player(self_o, other_o):  # 점프패드 - player
    if self_o.jump_status:
        self_o.jump_count = 0
        self_o.jump_h_force = self_o.jump_h_force * 1.5
        from src.object.player import Jump  # 지연 Import
        self_o.state_machine.start(Jump)

    pass


def waterO_player(self_o, other_o):
    """
    물에 닿았을 때 중력 감쇠 또는 부력을 적용하는 함수
    """
    self_o.y += -0.1  # 부력을 적용해 살짝 떠오르게 함
    self_o.jump_count = 0


def itemO_jump_time_up_player(self_o, other_o):
    from src.object.player import Jump
    if self_o.state_machine.cur_state == Jump:
        self_o.y -= self_o._gravity * 1.2
        self_o.jump_status = True
        self_o.jump_time = 2
        self_o.jump_count_limit = 2
        self_o.jump_time_limit = 0.7
    else:
        self_o.jump_status = False
        self_o.y += self_o._gravity * 1.2
        self_o.jump_count = 0
    pass


def sticky_blockO_player(self_o, other_o):
    # 플레이어와 블록의 충돌 영역 확인
    player_bb = self_o.get_bb()
    block_bb = other_o.get_bb()

    # 아래로 내려가는 중력 막기: 플레이어 바닥이 블록 윗면에 접촉한 경우
    if player_bb[1] <= block_bb[3] and player_bb[3] > block_bb[3]:
        # 블록 위에 자연스럽게 서 있게 조정
        self_o.y = block_bb[3] + (player_bb[3] - player_bb[1]) / 2
        self_o.jump_status = False  # 점프 상태 초기화
        self_o.jump_count = 0  # 점프 횟수 초기화

    # 위로 올라가는 경우 막기: 플레이어 머리가 블록 아래면에 접촉한 경우
    if player_bb[3] >= block_bb[1] and player_bb[1] < block_bb[1]:
        # 플레이어를 블록 아래로 밀어냄
        self_o.y = block_bb[1] - (player_bb[3] - player_bb[1]) / 2

    # 좌우 움직임 막기
    if SDLK_RIGHT in self_o.current_keys:
        self_o.x -= self_o.dir * RUN_SPEED_PPS * game_framework.frame_time
    if SDLK_LEFT in self_o.current_keys:
        self_o.x += self_o.dir * RUN_SPEED_PPS * game_framework.frame_time


def spikeO_player(self_o, other_o):
    print(1111)
    pass


def finishO_player(self_o, other_o):
    print(2222)
    pass


monster_img_path = "./src/asset/kenney_pixel-platformer/Tiles"

object_types = [{
    'name': "jump_object",
    'size': 2,
    'rigid_': 5,
    '_jumpO_object': None,
    '_jumpO_player': jumpO_player,
    'load_images': [
        f"{monster_img_path}/tile_0107.png",
        f"{monster_img_path}/tile_0108.png"
    ]
}, {
    'name': "water",
    'size': 1,
    'rigid_': 15,
    '_waterO_object': None,
    '_waterO_player': waterO_player,
}, {
    'name': "item_jump_time_up",
    'size': 1,
    'rigid_': 15,
    '_itemO_jump_time_up_object': None,
    '_itemO_jump_time_up_player': itemO_jump_time_up_player,
}, {
    'name': "sticky_block",
    'size': 1,
    'rigid_': 28,
    '_sticky_blockO_object': None,
    '_sticky_blockO_player': sticky_blockO_player,
}, {
    'name': "spike",
    'size': 1,
    'rigid_': 28,
    '_spikeO_object': None,
    '_spikeO_player': spikeO_player,
}, {
    'name': "finish",
    'size': 2,
    'rigid_': 28,
    '_finishO_object': None,
    '_finishO_player': finishO_player,
    'load_images': [
        f"{monster_img_path}/tile_0111.png",
        f"{monster_img_path}/tile_0112.png"
    ]
}
]


class ObjectO:
    images = None

    def load_images(self, image):
        self.images = {}
        for object_type in object_types:
            if self.type == object_type['name']:
                # load_images 키가 없으면 기본값 처리
                if 'load_images' in object_type and object_type['load_images']:
                    self.images[object_type['name']] = [
                        load_image(image_path) for image_path in object_type['load_images']
                    ]
                else:
                    # load_images가 없으면 단일 이미지로 로드
                    self.images[object_type['name']] = [load_image(image)]

                self.frames_per_action = object_type['size']  # 이미지 개수
                self.rigid_x1 = self.images[object_type['name']][0].w + object_type['rigid_']
                self.rigid_x2 = self.images[object_type['name']][0].w + object_type['rigid_']
                self.rigid_y1 = self.images[object_type['name']][0].h + object_type['rigid_']
                self.rigid_y2 = self.images[object_type['name']][0].h + object_type['rigid_']

    def __init__(self, id, x, y, tile_type, margin, num_tiles_x, image=None,
                 tile_size=20, select_num=40, tt_line=0, type="Unknown"):
        self.x, self.y = x, y
        self.size_x, self.size_y = 0, 0
        self.rigid_x1 = 0
        self.rigid_x2 = 0
        self.rigid_y1 = 0
        self.rigid_y2 = 0
        self.frames_per_action = 2  # 사진 개수
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

    def update(self):
        self.frame = (self.frame + self.frames_per_action
                      * ACTION_PER_TIME * game_framework.frame_time) % self.frames_per_action
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        if self.dir < 0:
            self.images[self.type][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.tile_size,
                                                                   self.tile_size)
        else:
            self.images[self.type][int(self.frame)].composite_draw(0, '', self.x, self.y, self.tile_size,
                                                                   self.tile_size)
        if status_.is_bb:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return (self.x - self.rigid_x1, self.y - self.rigid_y1,
                self.x + self.rigid_x2, self.y + self.rigid_y2)
        pass

    def handle_collision(self, group, other):
        if group == "player:Object":
            for object_type in object_types:
                if self.type == object_type['name'] and '_jumpO_object' in object_type:
                    # onCollision 함수 호출
                    # object_type['_jumpO_object'](self, other)
                    break
