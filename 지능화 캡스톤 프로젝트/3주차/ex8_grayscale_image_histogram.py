import cv2
import numpy as np
import matplotlib.pyplot as plt

# Lenna.png 파일을 Grayscale로 읽기
image = cv2.imread('Lenna.png', cv2.IMREAD_GRAYSCALE)

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load the image.")
    exit()

# 히스토그램 계산 (OpenCV의 calcHist 사용)
hist = cv2.calcHist([image], [0], None, [256], [0, 256])

# 원본 Grayscale 이미지 출력
cv2.imshow('Grayscale Image', image)

# 히스토그램 출력
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.plot(hist, color='gray')  # 히스토그램을 회색으로 출력
plt.xlim([0, 256])  # x축 범위
plt.show()

# 'q' 키를 누르면 Grayscale 창 종료
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()