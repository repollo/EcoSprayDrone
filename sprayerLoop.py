import itertools
import os
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import cv2
from datetime import datetime
from PIL import Image
from glob import glob
from time import sleep
from pathlib import Path
import socket
HOST = "127.0.0.1"  # IP is local loop back
PORT = 65432  # Just a high number unused port
print("TF version:", tf.__version__)

# update this to determine what to spray - names pulled from image classifier folder names in model
weed_list = ["weed", "weed2"] 

# Make a list of image classifier folder names in model
os.chdir('C:\\Users\\naNU\\Desktop\\drone\\ia_photos\\')
class_names = glob("*") # Reads all the folders in which images are present
class_names = sorted(class_names) # Sorting them
name_id_map = dict(zip(class_names, range(len(class_names))))

# Set up run directory with all model classes and unknown class
# so we can sort captured images into these folders
# put them in sequentially increasing directory order
os.chdir('C:\\Users\\naNU\\Desktop\\drone\\ia_predict\\')
last_subfolder = [f.name for f in os.scandir('.') if f.is_dir()]
rundir = str(int(last_subfolder[-1]) + 1)
os.mkdir(rundir)
os.chdir(rundir)
for directory in class_names:
  os.makedirs(directory, exist_ok = True)
os.makedirs("unknown", exist_ok = True)

# Load model
saved_model_path = "C:\\Users\\naNU\\Desktop\\drone\\ia_model"
remodel = tf.keras.models.load_model(saved_model_path)
pixels = 224

# Open webcam connection
cam = cv2.VideoCapture(0) #this is our webcam on usb, 0 index is webcam on laptop
cv2.namedWindow("Drone_View")

# start infinite loop until escape, log all results
os.chdir('C:\\Users\\naNU\\Desktop\\drone\\ia_predict\\')
mylog = open("runlog.txt", "a")
mylog.write("Run Number - " + str(rundir) + "\n")

while True:
  # Snapshot from webcam
  ret, frame = cam.read()
  if not ret:
    print("failed to grab frame from drone cam, stopping")
    break
  cv2.imshow("Drone_View", frame)
  date = datetime.now().strftime("%m_%d_%I_%M_%S_%p_%f") #note: keep it short and don't allow : in filename - error
  img_name = "cap_" + date + ".jpg"
  cv2.imwrite(img_name, frame)

  # Break up snapshot from webcam into 4 smaller images
  images_path = glob("cap_*")
  for image_path in images_path:
    im = Image.open(image_path)
    width, height = im.size
    w1 = width / 2
    h1 = height / 2
    im1 = im.crop((0,0,w1,h1))
    im2 = im.crop((w1,0,width,h1))
    im3 = im.crop((0,h1,w1,height))
    im4 = im.crop((w1,h1,width,height))
    im1.save(str(os.path.splitext(Path(image_path))[0]+'_1.jpg'))
    im2.save(str(os.path.splitext(Path(image_path))[0]+'_2.jpg'))
    im3.save(str(os.path.splitext(Path(image_path))[0]+'_3.jpg'))
    im4.save(str(os.path.splitext(Path(image_path))[0]+'_4.jpg'))

  weedfound = 0

  # Classify Images
  images_path = glob("cap_*")
  for img_path in images_path:
    # Note - do same steps here to preprocess as I did in model create
    # resize, bilinear, rescale
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(pixels, pixels), interpolation="bilinear")
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    img_array = np.array(img_array).astype('float32')/255
    predictions = remodel.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    scored_img_path = str(os.path.splitext(Path(img_path))[0] + "-" + str(class_names[np.argmax(score)]) + "-" + str(round(100 * np.max(score),1)) + '.jpg')
    # log this result in a text file
    mylog.write(scored_img_path + "-" + str(class_names[np.argmax(score)]) + "-" + str(round(100 * np.max(score),1)) + "%\n")
    # record the score of the prediction and move the file into its new home
    if np.max(score) > 0.7:
      os.rename(img_path,str(rundir + "\\" + str(class_names[np.argmax(score)]) + "\\" + scored_img_path))
      # decide if this is a weed and flag it
      if str(class_names[np.argmax(score)]) in weed_list:
        weedfound = 1
        print("Found weed " + scored_img_path)  
    else:
      os.rename(img_path,str(rundir + "\\unknown\\" + scored_img_path))
 
  # Activate the sprayer if weed found
  if weedfound == 1:
    print("found weeds, going to activate sprayer")
    # Tell python 2.7 process running in mission planner listening on this host/port to turn on sprayer by sending "1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      s.sendall(b"1")
      data = s.recv(1024)
    print(f"Received {data!r}")
    #print("didn't actually call sprayer, results in an error for now, instead keep taking photos")
  else:
    # Turn off sprayer
    # Tell python 2.7 process running in mission planner listening on this host/port to turn on sprayer by sending "1"
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #  s.connect((HOST, PORT))
    #  s.sendall(b"1")
    #  data = s.recv(1024)
    #print(f"Received {data!r}")
    print("Turn off sprayer")

  k = cv2.waitKey(1)
  if k%256 == 27:
    # ESC pressed
    print("Escape hit, closing...")
    break

  # break #remove this to make a continuous loop
  sleep(0.1)
  
# end infinite loop

# Release all resources
cam.release()
cv2.destroyAllWindows()
mylog.close()
