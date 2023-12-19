# -*- coding: utf-8 -*-
"""MOBILE NET.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P_PVQkzCsOJaO8RaYjV5CgSrenB5dUof
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from google.colab import drive
import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

drive.mount('/content/drive')

directory = '/content/drive/MyDrive/data'
Train_data = pd.DataFrame(columns=['path', 'class'])
Test_data = pd.DataFrame(columns=['path', 'class'])


for filename in os.listdir(directory):
    for filename2 in os.listdir(directory+'/'+filename):
        for images in os.listdir(directory+'/'+filename+'/'+filename2):
            if filename =='train':
                Train_data = Train_data._append({'path': directory+'/'+filename+'/'+filename2+'/'+images , 'class': filename2}, ignore_index=True)
            else :
                Test_data = Test_data._append({'path': directory+'/'+filename+'/'+filename2+'/'+images , 'class': filename2}, ignore_index=True)

Train_data

Test_data

batch_size = 24
size = (224,224,3)
img_width = img_hight = size[0]
clases = ['COVID19', 'NORMAL']

data_gen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = data_gen.flow_from_dataframe(Train_data, x_col='path', y_col='class',
                                            image_size=(img_hight, img_width), target_size=(
                                            img_hight, img_hight),
                                            batch_size=batch_size, class_mode='binary',
                                            classes=clases, subset='training')

val_data = data_gen.flow_from_dataframe(Train_data, x_col='path', y_col='class',
                                            image_size=(img_hight, img_width), target_size=(
                                            img_hight, img_hight),
                                            batch_size=batch_size, class_mode='binary',
                                            classes=clases, subset='validation')

test_data = data_gen.flow_from_dataframe(Test_data, x_col='path', y_col='class',
                                            image_size=(img_hight, img_width), target_size=(
                                            img_hight, img_hight),
                                            batch_size=batch_size, class_mode='binary',
                                            classes=clases,shuffle=False)

model = MobileNet(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

for layer in model.layers:
        layer.trainable = False

x = model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

#modelo
model = Model(inputs=model.input, outputs=predictions)

model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

model_3 = model.fit(train_data,validation_data= val_data, epochs=30, batch_size=32)

plt.figure(figsize=(12, 5))
#GRAFICO DE ACCRURACY
plt.subplot(1, 2, 1)
plt.plot(model_3.history['accuracy'], label='Training Accuracy')
plt.plot(model_3.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# GRAFICO LOSS
plt.subplot(1, 2, 2)
plt.plot(model_3.history['loss'], label='Training Loss')
plt.plot(model_3.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

predictions = model_3.model.predict(test_data)
y_pred = np.round(predictions).flatten()

y_true = test_data.classes

accuracy = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"F1-Score: {f1:.4f}")
print(f"Recall (Sensibilidad): {recall:.4f}")
print(f"Precision: {precision:.4f}")