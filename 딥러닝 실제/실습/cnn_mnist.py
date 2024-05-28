import numpy as np 
from tensorflow.keras.datasets import mnist 
from tensorflow.keras.models import Sequential   
from tensorflow.keras.layers import Dense      
#from keras.utils import np_utils 

import np_utils 
import matplotlib.pyplot as plt


# 1. 학습 및 테스트데이터 준비

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))
train_images = train_images.astype("float32") / 255
test_images = test_images.astype("float32") / 255


# 2. CNN 분류기 모델링 

from tensorflow import keras
from tensorflow.keras import layers
inputs = keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(inputs)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
outputs = layers.Dense(10, activation="softmax")(x)
cnn_cls = keras.Model(inputs=inputs, outputs=outputs)

cnn_cls.summary()

cnn_cls.compile(optimizer="rmsprop",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"])

# 3. Convolution Neural Network 분류기 학습 및 성능평가 ###############
history = cnn_cls.fit(train_images, train_labels, epochs=10, batch_size=64)         
test_loss, test_acc = cnn_cls.evaluate(test_images, test_labels)
print(f"테스트 정확도: {test_acc:.3f}")     
print(f"테스트 Loss: {test_loss:.3f}")             

#plt.plot(history.history['loss'])
plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
#plt.legend([ 'Loss'], loc='upper left')
