import itertools
import os
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
print("TF version:", tf.__version__)
print("Hub version:", hub.__version__)
print("GPU is", "available" if tf.test.is_gpu_available() else "NOT AVAILABLE")

module_selection = ("mobilenet_v2_100_224", 224) #@param ["(\"mobilenet_v2_100_224\", 224)", "(\"inception_v3\", 299)"] {type:"raw", allow-input: true}
handle_base, pixels = module_selection
MODULE_HANDLE ="https://tfhub.dev/google/imagenet/{}/feature_vector/4".format(handle_base)
IMAGE_SIZE = (pixels, pixels)
print("Using {} with input size {}".format(MODULE_HANDLE, IMAGE_SIZE))
BATCH_SIZE = 32 #@param {type:"integer"}
data_dir = 'C:\\Users\\naNU\\Desktop\\drone\\ia_photos'

# Note https://www.tensorflow.org/tutorials/images/classification
# has a different method to load data which uses cache. may be better

datagen_kwargs = dict(rescale=1./255, validation_split=.20)
dataflow_kwargs = dict(target_size=IMAGE_SIZE, batch_size=BATCH_SIZE, interpolation="bilinear")
valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagen_kwargs)
valid_generator = valid_datagen.flow_from_directory(data_dir, subset="validation", shuffle=False, **dataflow_kwargs)
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rotation_range=40, horizontal_flip=True, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, **datagen_kwargs)
train_generator = train_datagen.flow_from_directory(data_dir, subset="training", shuffle=True, **dataflow_kwargs)

print("Building model with", MODULE_HANDLE)
# Explicitly define the input shape so the model can be properly loaded by the TFLiteConverter
model = tf.keras.Sequential([tf.keras.layers.InputLayer(input_shape=IMAGE_SIZE + (3,)), hub.KerasLayer(MODULE_HANDLE, trainable=True), tf.keras.layers.Dropout(rate=0.2), tf.keras.layers.Dense(train_generator.num_classes, kernel_regularizer=tf.keras.regularizers.l2(0.0001))])
model.build((None,)+IMAGE_SIZE+(3,))
model.summary()
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.005, momentum=0.9), loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True, label_smoothing=0.1), metrics=['accuracy'])

steps_per_epoch = train_generator.samples // train_generator.batch_size
validation_steps = valid_generator.samples // valid_generator.batch_size
hist = model.fit(train_generator, epochs=10, steps_per_epoch=steps_per_epoch, validation_data=valid_generator, validation_steps=validation_steps).history

plt.figure()
plt.ylabel("Loss (training and validation)")
plt.xlabel("Training Steps")
plt.ylim([0,2])
plt.plot(hist["loss"])
plt.plot(hist["val_loss"])
plt.figure()
plt.ylabel("Accuracy (training and validation)")
plt.xlabel("Training Steps")
plt.ylim([0,1])
plt.plot(hist["accuracy"])
plt.plot(hist["val_accuracy"])

def get_class_string_from_index(index):
   for class_string, class_index in valid_generator.class_indices.items():
      if class_index == index:
         return class_string
x, y = next(valid_generator)
image = x[1, :, :, :]
true_index = np.argmax(y[0])
plt.imshow(image)
plt.axis('off')
plt.show()
# Expand the validation image to (1, 224, 224, 3) before predicting the label
prediction_scores = model.predict(np.expand_dims(image, axis=0))
predicted_index = np.argmax(prediction_scores)
print("True label: " + get_class_string_from_index(true_index))
print("Predicted label: " + get_class_string_from_index(predicted_index))

# Save created model
saved_model_path = "C:\\Users\\naNU\\Desktop\\drone\\ia_model"
tf.keras.models.save_model(model, saved_model_path)
