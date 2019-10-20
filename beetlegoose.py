import os
import sys
import multiprocessing as mp
from render import render
from capture import capture, screenshot
from time import sleep

if __name__ == '__main__':
    queues = {
        'msg_render_capture': mp.Queue(),
        'rendered_img': mp.Queue(),
        'captured_img': mp.Queue(),
        'ball_location': mp.Queue(),
    }
    p_render = mp.Process(target=render, name='render_loop', args=(queues,))
    p_render.start()
    
    # capture()
    p_capture = mp.Process(target=capture, name='capture_loop', args=(queues,))
    p_capture.start()

    sleep(5)
    p_render.join()
    p_capture.join()
