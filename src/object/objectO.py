# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, \
    draw_rectangle
import math
import src.config.game_framework as game_framework
from src.config.behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import src.mode.play_mode as play_mode
from src.object.player import Jump
import src.config.game_world as game_world

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

object_types = [{
    'name': "jump_object",
    'size': 2,
    'rigid_': 5,
    'onCollision': lambda self_o, other_o: print(
        f"Collision: {self_o.type} at ({self_o.x}, {self_o.y}) with {other_o.type} at ({other_o.x}, {other_o.y})"
    )
}]
monster_img_path = "./src/asset/kenney_pixel-platformer/Tiles"


class ObjectO:
    images = None

    def load_images(self, image):
        self.images = {}
        for object_type in object_types:
            if self.type == object_type['name']:
                self.images[object_type['name']] = [
                    load_image(f"{monster_img_path}/tile_{(self.id + i):04}.png") for i in
                    range(0, object_type['size'])]
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
            self.images[self.type][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 66, 92)
        else:
            self.images[self.type][int(self.frame)].composite_draw(0, '', self.x, self.y, 66, 92)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return (self.x - self.rigid_x1, self.y - self.rigid_y1,
                self.x + self.rigid_x2, self.y + self.rigid_y2)
        pass

    def handle_collision(self, group, other):
        if group == "player:Object":
            for object_type in object_types:
                if self.type == object_type['name'] and 'onCollision' in object_type:
                    # onCollision 함수 호출
                    object_type['onCollision'](self, other)
                    break
