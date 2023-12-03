from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import cv2 as cv #sudo apt install python3-opencv
import time
import os
import prog
import security_functions as security


VIDEO_STORAGE = '/home/pi/Videos/Camera_0'


def getVidName():
    #generate absolute folder name and create folder if does not exist
    foldername = VIDEO_STORAGE + time.strftime('/%m-%d-%Y')
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    #generate file name
    filename = foldername+time.strftime('/%H-%M-%S') + '.h264'
    return filename

def isNewHour(filename):
    file_hour = filename[-13:-11]
    cur_hour = time.strftime('%H')
    if file_hour != cur_hour:
        return True
    else:
        return False


#setup the pi camera
#picam2 = Picamera2(tuning="/usr/share/libcamera/ipa/raspberrypi/imx219_noir.json")
picam2 = Picamera2()
#picam2 = Picamera2()
picam2.video_configuration.main.size = (800, 600)
picam2.video_configuration.main.align()
picam2.configure('video')
picam2.start()

#video
encoder = H264Encoder()
vid_output = getVidName()
picam2.start_encoder(encoder, vid_output)
recording = True

prog.start()
while prog.isRunning():
    #keep saving pictures for use in other programs
    img = picam2.capture_array("main")
    cv.imwrite("Camera_Files/lock_cam_buff.jpg", img)
    os.rename("Camera_Files/lock_cam_buff.jpg", "Camera_Files/lock_cam.jpg")
    
    #manage recording
    lock = security.lockState()
    if lock == '0' or lock == '1': 
        #record video when unlocked and locked
        if not recording:
            vid_output = getVidName()
            picam2.start_encoder(encoder, vid_output)
            recording = True
            prog.namePrint("Video recording started")
        #record video to new file every hour
        if isNewHour(vid_output):
            vid_output = getVidName()
            picam2.stop_encoder()
            picam2.start_encoder(encoder, vid_output)
    elif lock == '2':
        #do not record video when home
        if recording:
            picam2.stop_encoder()
            recording = False
            prog.namePrint("Video recording stopped")

#cleanup
picam2.stop()
if recording:
    picam2.stop_encoder()
prog.end()