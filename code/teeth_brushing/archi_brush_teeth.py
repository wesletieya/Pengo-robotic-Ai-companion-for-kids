import tensorflow as tf
import numpy as np #Linear Algebra
import os #Manipulate Files
from PIL import Image #Manipulate Images

import warnings
warnings.filterwarnings('ignore') #ignores warnings

from keras.preprocessing.image import ImageDataGenerator
print('Training Set:')
train_gen = ImageDataGenerator(
    rescale=(1./255), #Rescales pixel values (originally 0-256) to 0-1
    rotation_range=0.4, #Rotates the image up to 40 degrees in either direction
    shear_range=0.2, #shears the image up to 20 degrees
    width_shift_range=0.2, #shifts the width by up to 20 %
    height_shift_range=0.2, #shifts the height by up to 20 %
    horizontal_flip=True, #flips the image along the horizontal axis
    fill_mode='nearest' #fills pixels lost during transformations with its nearest pixel
    )

train_generator = train_gen.flow_from_directory(
    r'C:\Users\ayabe\vs projects\new_data\train',
    target_size=(512,512),
    batch_size=32,
    class_mode='binary'
)

print('Testing Set:')
test_gen = ImageDataGenerator(rescale=(1./255))

test_generator = test_gen.flow_from_directory(
    r'C:\Users\ayabe\vs projects\new_data\test',
    target_size=(512,512),
    batch_size=32,
    class_mode='binary'
)


from keras.callbacks import Callback

#creates a custom callback class
class CustomCallback(Callback):
    """
    This callback will stop the model from training once the model reaches 95% accuracy on the training data
    """
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('accuracy') > 0.95:
            print('Accuracy above 95% -- Stopping Training')
            self.model.stop_training = True #stops model training

my_callback = CustomCallback()


from keras.callbacks import LearningRateScheduler

#creates a function that updates the learning rate based on the epoch number
def lr_update(epoch, lr):
    """
    For the first 5 epochs the learning rate will be 0.005.
    From epoch 6 and on, the learning rate will be reduced 1% per epoch
    """
    if epoch <= 5:
        return 0.005
    else:
        return lr * 0.99
    
lr_scheduler = LearningRateScheduler(lr_update)

from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout


model = Sequential([
    Conv2D(16, (3,3), activation='relu', input_shape=(512,512,1)),
    MaxPool2D((2,2)),
    Conv2D(32, (3,3), activation='relu'),
    MaxPool2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPool2D((2,2)),
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