import random

from pico2d import *
import src.config.game_framework as game_framework

import src.config.game_world as game_world
from src.object.grass import Grass
from src.object.boy import Boy
from src.object.ball import Ball
from src.object.zombie import Zombie

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    # fill here
    global balls
    balls = [Ball(random.randint(100, 1500), 60, 0) for _ in range(30)]
    game_world.add_objects(balls, 1)

    # 충돌 정보를 등록
    game_world.add_collision_pair('boy:ball', boy, None)
    for ball in balls:
        game_world.add_collision_pair('boy:ball', None, ball)
        game_world.add_collision_pair('zombie:ball', None, ball)

    #zombie 5 add
    zombies = [Zombie() for _ in range(5)]
    game_world.add_objects(zombies, 1)

    for zombie in zombies:
        game_world.add_collision_pair('zombie:ball', zombie, None)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass