import itertools
import os
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
print("TF version:", tf.__version__)

# Make a list of classes
from glob import glob
os.chdir('C:\\Users\\naNU\\Desktop\\drone\\ia_photos\\')
class_names = glob("*") # Reads all the folders in which images are present
class_names = sorted(class_names) # Sorting them
name_id_map = dict(zip(class_names, range(len(class_names))))

# Load model and classify images
saved_model_path = "C:\\Users\\naNU\\Desktop\\drone\\ia_model"
remodel = tf.keras.models.load_model(saved_model_path)
pixels = 224
images_path = glob("C:\\Users\\naNU\\Desktop\\drone\\ia_predict\\*")
#os.system(f"dir {images_path}")
for img_path in images_path:
  # Note - do same steps here to preprocess as I did in model create
  # resize, bilinear, rescale
  img = tf.keras.preprocessing.image.load_img(img_path, target_size=(pixels, pixels), interpolation="bilinear")
  img_array = tf.keras.preprocessing.image.img_to_array(img)
  img_array = tf.expand_dims(img_array, 0)
  img_array = np.array(img_array).astype('float32')/255
  #print(img_array)
  predictions = remodel.predict(img_array)
  score = tf.nn.softmax(predictions[0])
  #print("{}, {:.2f} confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))
  plt.imshow(img)
  plt.axis('off')
  plt.title(str(class_names[np.argmax(score)]) + "," + str(round(100 * np.max(score),1)) + "%")
  plt.show()
