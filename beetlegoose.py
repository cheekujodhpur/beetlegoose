import cv2
import numpy as np
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
    locque = queues['msg_location_render']
    itr = 0

    while True:
        sync.wait_on(capque, 'image_captured')
        framenum = int(capque.get())

        with capimg.get_lock(), rendimg[framenum].get_lock():
            captured_img = np.frombuffer(capimg.get_obj())
            rendered_img = np.frombuffer(rendimg[framenum].get_obj())
            diff = np.abs(captured_img - rendered_img)
            diff = diff.reshape((768,1024,3)).astype(np.uint8)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
            thresh = 255-thresh


            blob_params = cv2.SimpleBlobDetector_Params()
            params.minThreshold = 100
            params.maxThreshold = 150

            params.filterByArea = True
            params.minArea = 2000

            params.filterByCircularity = True
            params.minCircularity = 0.9

            params.filterByConvexity = True
            params.minConvexity = 0.8

            params.filterByIntertia = True
            params.minIntertiaRatio = 0.8
            detector = cv2.SimpleBlobDetector(params)

            keypoints = detector.detect(im)
            for kpt in keypoints:
                print("[kpt:] ", kpt.pt, kpt.size)

            #top = max(areas, key=lambda x:x[1])
            #print("[location] ", top)
            # cv2.imwrite("/home/pi/Desktop/diff%d.png" % itr, diff[1])
            # itr+=1
            #cv2.imwrite("/home/pi/Desktop/capture.png", captured_img.reshape((768,1024,3)))
            #cv2.imwrite("/home/pi/Desktop/render.png", rendered_img.reshape((768,1024,3)))
            locque.put((512,330))

if __name__ == '__main__':
    queues = {
        'msg_render_capture': mp.Queue(),
        'msg_capture_location': mp.Queue(),
        'msg_location_render': mp.Queue(),
        'captured_img': mp.Array(ctypes.c_double, 1024*768*3),
        'rendered_imgs': [mp.Array(ctypes.c_double, 1024*768*3) for i in range(16)]
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
