from pico2d import open_canvas, close_canvas
import src.config.game_framework as game_framework
import src.mode.logo_mode as start_mode
import src.config.config as config
# 마우스 커서 숨기기
from ctypes import c_int
from pico2d import SDL_ShowCursor, SDL_DISABLE


open_canvas(config.screen_width, config.screen_height)
SDL_ShowCursor(c_int(SDL_DISABLE))
game_framework.run(start_mode)
close_canvas()
