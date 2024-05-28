import numpy as np 
from tensorflow.keras.datasets import mnist 
from tensorflow.keras.models import Sequential   
from tensorflow.keras.layers import Dense      
from tensorflow.python.keras.utils import np_utils
from tensorflow.keras.utils import to_categorical

import matplotlib.pyplot as plt


# 1. 학습 및 테스트데이터 준비
(X_train, y_train), (X_test, y_test) = mnist.load_data()

Y_train = np_utils.to_categorical(y_train)
Y_test = np_utils.to_categorical(y_test)


print(y_train.shape)
print(Y_train.shape)

L, W, H = X_train.shape
X_train = X_train.reshape(-1, W * H)
X_test = X_test.reshape(-1, W * H)

X_train = X_train / 255.0   # 정규화
X_test = X_test / 255.0     # 정규화 


# 2. 분류 DNN 분류기 모델링 
Nin = X_train.shape[1] #784
Nh_l = [100, 50]
Nout = 10   # number of class
 
dnn_cls = Sequential()
dnn_cls.add(Dense(Nh_l[0], activation='relu', input_shape=(Nin,)))
dnn_cls.add(Dense(Nh_l[1], activation='relu'))
dnn_cls.add(Dense(Nout,activation='softmax'))
dnn_cls.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])

#dnn_cls.summary()


# 3. Deep Neural Network 분류기 학습및 성능평가 ###############
history = dnn_cls.fit(X_train, Y_train, epochs=10, batch_size=10, validation_split=0.2)          
performace_test = dnn_cls.evaluate(X_test, Y_test, batch_size=10)       
        
print('Test Loss and Accuracy ->', performace_test)

#plt.plot(history.history['loss'])
plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
#plt.legend([ 'Loss'], loc='upper left')