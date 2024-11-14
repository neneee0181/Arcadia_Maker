from pico2d import open_canvas, delay, close_canvas
import src.config.game_framework as game_framework
import src.logo_mode as start_mode

open_canvas(1600, 600)
game_framework.run(start_mode)
close_canvas()
