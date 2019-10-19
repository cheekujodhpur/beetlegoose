#!/usr/bin/env python

import cv2
import numpy as np

# global declares
width = 640
height = 480
size = (height,width,3)
def generate_frames(size,non_white,box_size):
    total_bits = 16
    frames = []
    for i in range(total_bits):
        raw = np.zeros(size)

        raw[:box_size,:box_size] =\
        raw[-box_size:,:box_size] =\
        raw[-box_size:,-box_size:] =\
        raw[:box_size,-box_size:] = non_white

        if (1 & i):
            raw[:box_size,:box_size,:] = 1
        if (2 & i):
            raw[-box_size:,:box_size,:] = 1
        if (4 & i):
            raw[-box_size:,-box_size:,:] = 1
        if (8 & i):
            raw[:box_size,-box_size:,:] = 1

        scaled = raw*255
        scaled = scaled.astype(np.uint8)
        frames.append(scaled)
    return frames

def render():
    frames = generate_frames(size, np.array([0.75, 0.25, 0.25 ]), 25)

    i = 0
    N = len(frames)
    advance_frame_id = lambda x:(x+1)%N
    capture = cv2.VideoCapture(0)
    game_name = "Game"
    cv2.namedWindow( game_name, cv2.WINDOW_NORMAL )

    while True:
        # read frame from camera
        ret, frame = capture.read()
        if not ret:
            Exception( "Could not read from camera" )

        cv2.imshow( game_name, frames[i] )
        i = advance_frame_id(i)
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break
