import os
import sys
import multiprocessing as mp
from .render import render
from .capture import capture


def start():
    p_render = mp.Process(target=render, name='render_loop')
    p_render.start()
    
    # capture()
    p_capture = mp.Process(target=capture, name='capture_loop')
    p_capture.start()
    while True:
        pass
    # TODO start game
