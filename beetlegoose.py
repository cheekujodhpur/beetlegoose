import os
import sys
import multiprocessing as mp
from render import render
from capture import capture, screenshot

if __name__ == '__main__':
    queues = {
        'rendered_img': mp.Queue(),
        'captured_img': mp.Queue(),
        'ball_location': mp.Queue(),
    }
    p_render = mp.Process(target=render, name='render_loop', args=(queues,))
    p_render.start()
    
    # capture()
    p_capture = mp.Process(target=screenshot, name='capture_loop', args=(queues,))
    p_capture.start()
    while True:
        pass
    # TODO start game
