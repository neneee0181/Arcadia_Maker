import time

from pico2d import *
import src.config.config as config


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time
        # print(f'Frame Time: {frame_time}, Frame Rate: {frame_rate}')
        # events = get_events()
        # for event in events:
        #     if event.type == SDL_KEYDOWN and event.key == SDLK_LEFTBRACKET:  # 소리 불륨 낮추기
        #         if config.sound_size > 0:
        #             config.sound_size -= 1
        #         pass
        #     elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHTBRACKET:  # 소리 볼륨 높이기
        #         if config.sound_size < config.sound_size:
        #             config.sound_size += 1
        #         pass

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
