import os
import numpy as np
import tensorflow as tf
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.models import Sequential
from tf_keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tf_keras.callbacks import EarlyStopping, ModelCheckpoint

# Set dataset paths
train_dir = r"C:/Users/rkroh\Downloads/archive/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train"
valid_dir = r"C:/Users/rkroh\Downloads/archive/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid"


img_height, img_width = 224, 224
batch_size = 32


train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=20, zoom_range=0.2, horizontal_flip=True)
valid_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical'
)

valid_data = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical'
)


labels = list(train_data.class_indices.keys())
with open("D:/6 month/Ai Projects/crop_disease_project/crop_app/model/labels.txt", "w") as f:
    for label in labels:
        f.write(label + "\n")


model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(len(labels), activation='softmax')
])


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True),
    ModelCheckpoint('D:/6 month/Ai Projects/crop_disease_project/crop_app/model/model.h5', save_best_only=True)
]


history = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=25,
    callbacks=callbacks
)






