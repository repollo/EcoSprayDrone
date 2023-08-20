# Run on startup command in crontab
# @reboot python3 /home/nanu/Desktop/drone/droneSprayer_v1.py > /home/nanu/Desktop/drone/$(date +"%m_%d_%I_%M_%S_%p").out 2>&1

# import the necessary packages
#import math
import os
import platform
import time
from datetime import datetime
from glob import glob

import cv2
#import numpy as np
#from tflite_support.task import core
#from tflite_support.task import processor
#cv2from tflite_support.task import vision

# Check if we're on a Raspberry Pi
if platform.system().lower() == "linux" and "raspberry" in platform.uname()[4].lower():
    from picamera import PiCamera
    import RPi.GPIO as GPIO
else:
    # We're not on a Pi, so use stubs
    from picamera_stub import PiCamera
    import gpio_stub as GPIO


#set up the camera
camera = PiCamera() #declare camera
crop_size = 224 #from mobilenet model
# TO DO: change camera pixels used to get wider view. Test it still works/centers on camera/gets clear images
width = 1500 #6*crop_size #3280
height = 1000 #4*crop_size #2464
camera.resolution = (width,height) 

#set up motors
sprayerPIN = 2
enablePIN = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(sprayerPIN, GPIO.OUT)
GPIO.setup(enablePIN, GPIO.OUT)
#sprayer=GPIO.PWM(sprayerPIN, 50) #50 hz
#sprayer.start(0)
#alternate
GPIO.output(sprayerPIN, GPIO.LOW)
GPIO.output(enablePIN, GPIO.HIGH)

# Visualization parameters for text on classification images
_ROW_SIZE = 10  # pixels
_LEFT_MARGIN = 10  # pixels
_TEXT_COLOR = (0, 0, 255)  # red
_FONT_SIZE = 0.5
_FONT_THICKNESS = 1
_FPS_AVERAGE_FRAME_COUNT = 10
# Initialize the image classification model. This is the custom trained model based on mobilenet
base_options = core.BaseOptions(
  file_name="/home/nanu/Desktop/drone/model/drone_ub_qonly_meta.tflite", use_coral=False, num_threads=4)
# Enable Coral by this setting
classification_options = processor.ClassificationOptions(
  max_results=1, score_threshold=0.0)
options = vision.ImageClassifierOptions(
  base_options=base_options, classification_options=classification_options)
classifier = vision.ImageClassifier.create_from_options(options)

#create run directory to save photos and go there
dronedir = '/home/nanu/Desktop/drone/'
date = datetime.now().strftime("%m_%d_%I_%M_%S_%p_%f")
rundir = dronedir+date
os.makedirs(rundir)
os.chdir(rundir)

# Various useful functions
def categorizeImage(crop_image,crop_name):
  # Convert the image from BGR to RGB as required by the TFLite model.
  rgb_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
  re_size = (224,224)
  rgb_image=cv2.resize(rgb_image,re_size)
  # Return variables
  returnPlant = "dirt"
  returnScore = 0.0
  firstScore = ""
  firstPlant = ""
  secondScore = ""
  secondPlant = ""
  # Create TensorImage from the RGB image
  tensor_image = vision.TensorImage.create_from_array(rgb_image)
  #tensor_image = vision.TensorImage.create_from_array(image)
  # List classification results
  categories = classifier.classify(tensor_image)

  # Show classification results on the image
  for idx, category in enumerate(categories.classifications[0].categories):
    category_name = category.category_name
    score = round(category.score, 2)
    result_text = category_name + ' (' + str(score) + ')'
    text_location = (_LEFT_MARGIN, (idx + 2) * _ROW_SIZE)
    cv2.putText(crop_image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)
    #Let's get 2 results and if one is a weed, bias towards action. Still return category name if dirt or non-weed are present though
    if category_name.startswith("weed") and score > 2.0 and returnPlant == "dirt":
      returnPlant = category_name
      returnScore = score
    if returnScore == 0.0:
      returnPlant = category_name
      returnScore = score
    if idx == 0:
      firstScore = score
      firstPlant = category_name
    if idx == 1:
      secondScore = score
      secondPlant = category_name
  #write out the marked up, classified image to filesystem
  cv2.imwrite(firstPlant+"_"+str(firstScore)+"_"+secondPlant+"_"+str(secondScore)+"_"+crop_name,crop_image)
  return returnPlant,returnScore
def takePhoto(prepend):
    #snapshot from camera and save. assumes we're already in correct directory
    date = datetime.now().strftime("%m_%d_%I_%M_%S_%p_%f") #note: keep it short and don't allow : in filename - error
    photo_name = prepend + "_" + date + ".jpg"
    camera.capture(photo_name)
    image = cv2.imread(photo_name) #pull up image and get shape
    height = image.shape[0]
    width = image.shape[1]
    return photo_name,image,height,width
  
try:
  while True:
    search_filename,search_image,height,width = takePhoto("search_")
    time.sleep(1)
    search_image = cv2.imread("/home/nanu/Desktop/drone/model/test/2_weedGrass_3.24_dirt_1.05_3.0_1.0_search__06_13_01_54_31_PM_864384.jpg") #testing
    print("Analyzing photo: ",search_filename) #testing
    plant_name,score = categorizeImage(search_image,search_filename)
    #if we find weed, spray it
    if plant_name.startswith("weed") and score > 1.5:
      print("Found weed: ",plant_name," score: ",score," filename: ",search_filename," Turning on sprayer")
      GPIO.output(sprayerPIN, GPIO.HIGH)
      GPIO.output(enablePIN, GPIO.LOW)
      time.sleep(1)
      print("Turning off sprayer")
      GPIO.output(sprayerPIN, GPIO.LOW)
      GPIO.output(enablePIN, GPIO.HIGH)
  
except KeyboardInterrupt:
  sprayer.stop()
  GPIO.cleanup()
