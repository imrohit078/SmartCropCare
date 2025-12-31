# import tensorflow as tf
# from tf_keras.preprocessing import image
# import numpy as np
# import os

# # Load model
# # model_path = os.path.join("model", "model.h5")
# model_path = 'D:/6 month/Ai Projects/crop_disease_project/crop_app/model/model.h5'

# model = tf.keras.models.load_model(model_path)

# # Load labels
# # with open(os.path.join("model", "labels.txt"), 'r') as f:
# with open('D:/6 month/Ai Projects/crop_disease_project/crop_app/model/labels.txt', 'r')as f:
#     class_names = [line.strip() for line in f]

# # Predict function
# def predict_disease(img_path):
#     img = image.load_img(img_path, target_size=(224, 224))
#     img_array = image.img_to_array(img) / 255.0
#     img_array = np.expand_dims(img_array, axis=0)

#     predictions = model.predict(img_array)
#     predicted_index = np.argmax(predictions)
#     return class_names[predicted_index]



