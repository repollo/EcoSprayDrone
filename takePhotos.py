import os
import platform
import time
from datetime import datetime


# Check if we're on a Raspberry Pi
if platform.system().lower() == "linux" and "raspberry" in platform.uname()[4].lower():
    from picamera import PiCamera
    import RPi.GPIO as GPIO
else:
    # We're not on a Pi, so use stubs
    from picamera_stub import PiCamera
    import gpio_stub as GPIO


#set up camera
camera = PiCamera() #declare camera
width = 1500 #max 2592, 1944. for some reason, the display of image is 90 degrees rotated so it appears wider then high
height = 1000
camera.resolution = (width,height) 

#create run directory to save photos and go there
weederdir = '/home/nanu/Desktop/weeder/'
date = datetime.now().strftime("%m_%d_%I_%M_%S_%p_%f")
rundir = weederdir+date
os.makedirs(rundir)
os.chdir(rundir)

count = 0
while count < 600:
  date = datetime.now().strftime("%m_%d_%I_%M_%S_%p_%f") #note: keep it short and don't allow : in filename - error
  photo_name = date + ".jpg"
  camera.capture(photo_name)
  time.sleep(1)
  count = count + 1
