from pico2d import open_canvas, delay, close_canvas
import src.config.game_framework as game_framework
import src.logo_mode as start_mode
import src.config.config as config

open_canvas(config.screen_width, config.screen_height)
game_framework.run(start_mode)
close_canvas()
