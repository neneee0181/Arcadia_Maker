from pico2d import load_image

from src.config.config import screen_width, screen_height


class StartBackground:
    def __init__(self):
        self.image = load_image('./src/asset/kenney_pixel-platformer/SampleB.png')

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, screen_width // 2, screen_height // 2, screen_width, screen_height)

    def update(self):
        pass
