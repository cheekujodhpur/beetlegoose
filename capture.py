from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def capture(queues={}):
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (1024,768)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1024,768))

    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

def screenshot(queues={}):
    camera = PiCamera()
    camera.resolution = (1024,768)
    time.sleep(10)

    camera.capture('/home/pi/Desktop/img.png')
    print('Image captured')

if __name__ == '__main__':
    capture()
