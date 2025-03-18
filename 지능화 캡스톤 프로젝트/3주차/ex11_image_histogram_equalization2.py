import cv2
import matplotlib.pyplot as plt

# Grayscale 이미지 읽기
image = cv2.imread('Hawkes.jpg', cv2.IMREAD_GRAYSCALE)

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load Hawkes.jpg.")
    exit()

# 히스토그램 평활화 적용
equalized_image = cv2.equalizeHist(image)

# 결과 표시 (원본과 평활화된 이미지 비교)
cv2.imshow('Original Image (Grayscale)', image)
cv2.imshow('Equalized Image (Grayscale)', equalized_image)

# 히스토그램 비교 (Matplotlib)
plt.figure(figsize=(10, 5))

# 원본 이미지의 히스토그램
plt.subplot(1, 2, 1)
plt.title('Original Image Histogram')
plt.hist(image.ravel(), bins=256, range=[0, 256], color='black')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

# 평활화된 이미지의 히스토그램
plt.subplot(1, 2, 2)
plt.title('Equalized Image Histogram')
plt.hist(equalized_image.ravel(), bins=256, range=[0, 256], color='black')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# 'q' 키를 눌러 창 닫기
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()