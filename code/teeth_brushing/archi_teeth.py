import tensorflow as tf
import numpy as np
import os
from PIL import Image
import scipy

import warnings
warnings.filterwarnings('ignore')

from keras.preprocessing.image import ImageDataGenerator

# Define the data generators
train_gen = ImageDataGenerator(
    rescale=(1./255),
    rotation_range=0.4,
    shear_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_generator = train_gen.flow_from_directory(
    r'C:\Users\ayabe\vs projects\new_data\train',
    target_size=(512, 512),
    batch_size=32,
    color_mode='grayscale',  # Ensure images are loaded as grayscale
    class_mode='binary'
)

# Load a batch of images and extract the first image
images, labels = next(train_generator)

# Print the shape of the first image in the batch
print("Shape of the first image in the batch:", images[0].shape)

# Continue with the rest of your code...

print('Testing Set:')
test_gen = ImageDataGenerator(rescale=(1./255))

test_generator = test_gen.flow_from_directory(
    r'C:\Users\ayabe\vs projects\new_data\test',
    target_size=(512, 512),
    batch_size=32,
    color_mode='grayscale',  # Ensure images are loaded as grayscale
    class_mode='binary'
)

from keras.callbacks import Callback

class CustomCallback(Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('accuracy') > 0.95:
            print('Accuracy above 95% -- Stopping Training')
            self.model.stop_training = True

my_callback = CustomCallback()

from keras.callbacks import LearningRateScheduler

def lr_update(epoch, lr):
    if epoch <= 5:
        return 0.005
    else:
        return lr * 0.99

lr_scheduler = LearningRateScheduler(lr_update)

from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout

model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(512, 512, 1)),  # Updated input shape for grayscale images
    MaxPool2D((2, 2)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPool2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPool2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

print(model.summary())

from keras.optimizers import Adam

model.compile(loss='binary_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    epochs=20,
    callbacks=[my_callback, lr_scheduler]
)

model.save('saved_model/my_model1.h5')
print("Model saved to 'saved_model/my_model1.h5'")
