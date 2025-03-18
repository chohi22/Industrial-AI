import cv2
import numpy as np
import matplotlib.pyplot as plt

# Grayscale 이미지 읽기
image = cv2.imread('Hawkes.jpg', cv2.IMREAD_GRAYSCALE)

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load Hawkes.jpg.")
    exit()


# 히스토그램 스트래칭
def histogram_stretching(img):
    # 픽셀값의 최소값과 최대값 계산
    min_pixel = np.min(img)
    max_pixel = np.max(img)

    # 스트래칭 공식: ((pixel - min) / (max - min)) * 255
    stretched = ((img - min_pixel) / (max_pixel - min_pixel) * 255).astype(np.uint8)
    return stretched


stretched_image = histogram_stretching(image)

# 결과 표시 (원본과 스트래칭된 이미지 비교)
cv2.imshow('Original Image', image)
cv2.imshow('Stretched Image', stretched_image)

# Matplotlib를 사용하여 히스토그램 비교
plt.figure(figsize=(10, 5))

# 원본 이미지의 히스토그램
plt.subplot(1, 2, 1)
plt.title('Original Image Histogram')
plt.hist(image.ravel(), bins=256, range=[0, 256], color='black')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

# 스트래칭된 이미지의 히스토그램
plt.subplot(1, 2, 2)
plt.title('Stretched Image Histogram')
plt.hist(stretched_image.ravel(), bins=256, range=[0, 256], color='black')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# 'q' 키를 눌러 종료
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
