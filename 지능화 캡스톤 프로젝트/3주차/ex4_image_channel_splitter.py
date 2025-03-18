import cv2

# 이미지 읽기
image = cv2.imread('Lenna.png')

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("Error: Unable to load the image.")
    exit()

# B, G, R 채널 분리
blue, green, red = cv2.split(image)

# 원본 이미지 출력
cv2.imshow('Original Image', image)

# 각 성분 출력
cv2.imshow('Blue Channel', blue)
cv2.imshow('Green Channel', green)
cv2.imshow('Red Channel', red)

# 'q' 키를 누르면 종료
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 창 닫기
cv2.destroyAllWindows()