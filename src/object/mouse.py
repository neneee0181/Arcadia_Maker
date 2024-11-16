from pico2d import *


class Mouse:
    image = None

    def __init__(self, x=-100, y=-100, velocity=1):
        if Mouse.image == None:
            Mouse.image = load_image('./src/asset/button/hand_open.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        events = get_events()
        for event in events:
            if event.type == SDL_MOUSEMOTION:
                self.x, self.y = event.x, get_canvas_height() - event.y
        pass

    def get_bb(self):
        # fill here
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
        pass

    def handle_collision(self, group, other):
        pass
