import os
import numpy as np
import tensorflow as tf
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.models import Sequential, load_model
from tf_keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tf_keras.applications import MobileNetV2
from tf_keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

train_dir = r"D:/6 month/Ai Projects/crop_disease_project/crop_app\dataset/New Plant Diseases Dataset(Augmented)/train"
valid_dir = r"D:/6 month/Ai Projects/crop_disease_project/crop_app\dataset/New Plant Diseases Dataset(Augmented)/valid"
model_path = r"D:/6 month/Ai Projects/crop_disease_project/crop_app/model/mobilenet_model.h5"
labels_path = r"D:/6 month/Ai Projects/crop_disease_project/crop_app/model/labels.txt"

img_size = (224, 224)
batch_size = 32

train_gen = ImageDataGenerator(rescale=1./255, rotation_range=20, zoom_range=0.2, horizontal_flip=True)
val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    train_dir, target_size=img_size, batch_size=batch_size, class_mode='categorical'
)
val_data = val_gen.flow_from_directory(
    valid_dir, target_size=img_size, batch_size=batch_size, class_mode='categorical', shuffle=False
)

labels = list(train_data.class_indices.keys())
with open(labels_path, 'w') as f:
    for label in labels:
        f.write(label + '\n')

base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False  

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(len(labels), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

callbacks = [
    EarlyStopping(patience=3, restore_best_weights=True),
    ModelCheckpoint(model_path, save_best_only=True)
]

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=5,
    callbacks=callbacks
)

print("✅ Training complete. Model saved to:", model_path)

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training vs Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

model = load_model(model_path)
val_data.reset()
predictions = model.predict(val_data)
y_true = val_data.classes
y_pred = np.argmax(predictions, axis=1)

print("\n📋 Classification Report:")
print(classification_report(y_true, y_pred, target_names=labels))

cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(16, 12))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
