from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import sync

WIDTH=1024
HEIGHT=768

def is_square(cnt):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04*peri, True)
    if len(approx) == 4:
        x,y,w,h = cv2.boundingRect(approx)
        ar = w/float(h)
        if ar >= 0.9 and ar <= 1.1:
            return True
    return False

def find_anchors(image):
    #cv2.imwrite("/home/pi/Desktop/img.png", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("/home/pi/Desktop/gray.png", gray)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
    #cv2.imwrite("/home/pi/Desktop/thresh.png", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    sqrs = []
    for c in cnts:
        M = cv2.moments(c)
        if M['m00'] == 0:
            continue
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print("Found contour at %dx%d" % (cx,cy))
        if is_square(c):
            print("Found anchor at %dx%d" % (cx,cy))
            sqrs.append((cx,cy))

    return sqrs

def vertex_comp(a, b):
    if abs(a[0]-b[0]) > 200:
        return a[0]-b[0]
    if abs(a[1]-b[1]) > 200:
        return a[1]-b[1]
    return 0

def capture(queues={}):
    msg_render = queues['msg_render_capture']
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (WIDTH,HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(WIDTH,HEIGHT))

    # allow the camera to warmup
    time.sleep(0.1)

    sync.wait_on(msg_render, 'anchor_start')
    anchors = []
    # anchor calibration
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        anchors = find_anchors(image)
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        if len(anchors) == 4:
            print("Found all four anchors")
            break
    msg_render.put('anchor_done')
    anchors = sorted(anchors, cmp=vertex_comp)
    anchors = [anchors[3], anchors[2], anchors[0], anchors[1]]
    anchors_flipped = [(a[1],a[0]) for a in anchors]
    print(anchors)

    render_points = np.float32([[HEIGHT,0],[0,0],[0,WIDTH],[HEIGHT,WIDTH]])
    capture_points = np.float32(anchors)
    perspectiveT = cv2.getPerspectiveTransform(capture_points, render_points)

    time.sleep(2)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        cropped = cv2.warpPerspective(image, perspectiveT, (HEIGHT,WIDTH))
        cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
        #cv2.imwrite("/home/pi/Desktop/cropped.png", cropped)
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        bitval = lambda x: 0 if int(x[1])+int(x[0]) > 300 else 1
        bitseq = [bitval(cropped[v]) for v in [(HEIGHT-1,0), (HEIGHT-1, WIDTH-1), (0, WIDTH-1), (0,0), ]]
        print(bitseq)
        # break

def screenshot(queues={}):
    camera = PiCamera()
    camera.resolution = (WIDTH,HEIGHT)
    time.sleep(10)

    camera.capture('/home/pi/Desktop/img.png')
    print('Image captured')

if __name__ == '__main__':
    image = cv2.imread("capture.png")
    print(find_anchors(image))
