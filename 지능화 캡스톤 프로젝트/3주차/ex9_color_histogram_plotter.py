import cv2
import numpy as np
import matplotlib.pyplot as plt

# Lenna.png 파일을 BGR로 읽기
image = cv2.imread('Lenna.png')

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load the image.")
    exit()

# 히스토그램 계산
colors = ('b', 'g', 'r')  # BGR 각 채널의 색상
hist_data = {}

plt.figure()
plt.title("Color Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")

# 각 채널에 대해 히스토그램을 계산하고 플롯
for i, color in enumerate(colors):
    hist = cv2.calcHist([image], [i], None, [256], [0, 256])  # 채널별 히스토그램 계산
    plt.plot(hist, color=color, label=f'{color.upper()} Channel')  # 히스토그램 플롯
    hist_data[color] = hist  # 히스토그램 데이터 저장
    plt.xlim([0, 256])  # x축 범위 설정

# 범례 추가
plt.legend()
plt.show()

# 원본 이미지 출력
cv2.imshow('Original Image', image)

# 'q' 키를 눌러 종료
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()