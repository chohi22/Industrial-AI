import cv2

# 이미지 읽기
image = cv2.imread('Lenna.png')

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load the image.")
    exit()

# BGR 이미지를 HSV 색 공간으로 변환
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# HSV 성분 분리
hue, saturation, value = cv2.split(hsv_image)

# 결과 출력
cv2.imshow('Original Image', image)  # 원본 이미지
cv2.imshow('Hue Channel', hue)  # 색상(H) 채널
cv2.imshow('Saturation Channel', saturation)  # 채도(S) 채널
cv2.imshow('Value Channel', value)  # 명도(V) 채널

# 'q' 키를 눌러 종료
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 창 닫기
cv2.destroyAllWindows()