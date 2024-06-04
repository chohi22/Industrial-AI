
from keras import datasets
from tensorflow.keras.applications import vgg16 as vgg
from tensorflow.keras.layers import Dropout, Dense, GlobalAveragePooling2D,BatchNormalization
from tensorflow.keras import Model


import matplotlib.pyplot as plt



# 1. 학습 및 테스트데이터 준비

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

train_images = train_images.astype("float32") / 255
test_images = test_images.astype("float32") / 255


# 2. VGG를 이용한 전이학습(transfer learning) 모델

input_shape = (32, 32, 3)

base_model = vgg.VGG16(weights='imagenet', 
                       include_top=False, 
                       input_shape=input_shape)

# 2.1 VGG16 모델의 세 번째 블록에서 마지막 층 추출
last = base_model.get_layer('block3_pool').output

# VGG16 모델의 가중치 동결
for layer in base_model.layers:
     layer.trainable = False

# 2.2 상위 층에 분류층 추가
x = GlobalAveragePooling2D()(last)
x= BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
pred = Dense(10, activation='softmax')(x)
vgg_cls= Model(base_model.input, pred)

vgg_cls.compile(optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"])

vgg_cls.summary()


# 3. Convolution Neural Network 분류기 학습 및 성능평가 ###############

history = vgg_cls.fit(train_images, train_labels, epochs=50, batch_size=30)         
test_loss, test_acc = vgg_cls.evaluate(test_images, test_labels)
print(f"테스트 정확도: {test_acc:.3f}")     
print(f"테스트 Loss: {test_loss:.3f}")             

#plt.plot(history.history['loss'])
plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
