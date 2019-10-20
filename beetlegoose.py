import cv2
import multiprocessing as mp
from render import render
from capture import capture, screenshot
from time import sleep
import ctypes
import sync

def calculate_location(queues={}):
    capimg = queues['captured_img']
    rendimg = queues['rendered_imgs']
    capque = queues['msg_capture_location']
    sync.wait_on(capque, 'image_captured')
    framenum = int(capque.get())

    with capimg.get_lock(), rendimg[framenum].get_lock():
        captured_img = np.frombuffer(capimg.get_obj())
        rendered_img = np.frombuffer(rendimg[framenum].get_obj())
        print(np.mean(captured_img - rendered_imgs))

if __name__ == '__main__':
    queues = {
        'msg_render_capture': mp.Queue(),
        'msg_capture_location': mp.Queue(),
        'captured_img': mp.Array(ctypes.c_uint8, 1024*768*3),
        'rendered_imgs': [mp.Array(ctypes.c_uint8, 1024*768*3) for i in range(16)]
    }
    p_render = mp.Process(target=render, name='render_loop', args=(queues,))
    p_render.start()
    
    # capture()
    p_capture = mp.Process(target=capture, name='capture_loop', args=(queues,))
    p_capture.start()

    p_location = mp.Process(target=calculate_location, name='location_loop', args=(queues,))
    p_location.start()

    sleep(5)
    p_render.join()
    p_capture.join()
    p_location.join()
