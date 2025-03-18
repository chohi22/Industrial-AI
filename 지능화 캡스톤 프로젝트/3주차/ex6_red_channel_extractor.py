import cv2
import numpy as np

# 이미지 읽기
image = cv2.imread('Candies.png')

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load the image.")
    exit()

# BGR 채널 분리
blue, green, red = cv2.split(image)

# Red 채널이 지정된 숫자 이상인 값만 추출 (숫자 예: 150)
threshold = 150
# 빨간색 값이 threshold 이상인 마스크 생성
red_mask = cv2.inRange(red, threshold, 255)

# 원본 이미지에서 빨간색 성분만 유지
red_extracted = cv2.bitwise_and(image, image, mask=red_mask)

# 결과 출력
cv2.imshow('Original Image', image)  # 원본 이미지
cv2.imshow('Red Mask', red_mask)  # 빨간색 마스크
cv2.imshow('Red Extracted Image', red_extracted)  # 빨간색 성분 추출 이미지

# 'q' 키를 누르면 창 닫기
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 창 닫기
cv2.destroyAllWindows()