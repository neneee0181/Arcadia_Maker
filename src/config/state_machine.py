from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, \
    SDLK_UP


def start_event(e):
    return e[0] == 'START'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def jump_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def jump_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def jump_time_out(e):
    return e[0] == 'JUMP_TIME_OUT'


class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def start(self, state):
        self.cur_state = state

        print(f'Enter into {state}')
        self.cur_state.enter(self.o, ('START', 0))

    def add_event(self, e):
        # print(f'    DEBUG: New event {e} added to event Que')
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            # print(f'Handling event: {e}, Current state: {self.cur_state}, Next state: {next_state}')
            if event(e):
                print(f'Exit from {self.cur_state}')
                self.cur_state.exit(self.o, e)

                if callable(next_state) and not isinstance(next_state, type):
                    print("Calling next_state as function.")
                    next_state = next_state(e)

                self.cur_state = next_state
                print(f'Enter into {self.cur_state}')
                self.cur_state.enter(self.o, e)
                return

        # print(f'        Warning: Event [{e}] at State [{self.cur_state}] not handled')
