import cv2
import numpy as np

# 이미지 읽기
image = cv2.imread('Candies.png')

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load the image.")
    exit()

# BGR 이미지를 HSV 색 공간으로 변환
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 붉은색 범위 설정 (2개의 설정 필요, OpenCV에서 빨간색은 양 끝 값에 걸칩니다)
lower_red1 = np.array([0, 100, 100])  # 빨간색 하한 (Hue: 0도 근처)
upper_red1 = np.array([10, 255, 255])  # 빨간색 상한
lower_red2 = np.array([160, 100, 100])  # 빨간색 하한 (Hue: 160도 근처)
upper_red2 = np.array([179, 255, 255])  # 빨간색 상한

# 마스크 생성 (두 범위의 빨간색 마스크를 생성 후 합치기)
mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)

# 원본 이미지에서 붉은색 캔디 추출
red_candies = cv2.bitwise_and(image, image, mask=red_mask)

# 결과 출력
cv2.imshow('Original Image', image)  # 원본 이미지
cv2.imshow('Red Mask', red_mask)  # 붉은색 영역 마스크
cv2.imshow('Red Candies', red_candies)  # 붉은색 캔디 추출 결과

# 'q' 키를 눌러 종료
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 창 닫기
cv2.destroyAllWindows()
