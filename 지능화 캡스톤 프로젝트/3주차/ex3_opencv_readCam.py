import cv2

# 카메라 장치 열기 (디폴트: 0번째 웹캠)
camera = cv2.VideoCapture(0)

# 카메라가 제대로 열렸는지 확인
if not camera.isOpened():
    print("Error: Unable to access the camera.")
    exit()

while True:
    # 카메라로부터 프레임 읽기
    ret, frame = camera.read()

    # 프레임 읽기 실패 시 루프 종료
    if not ret:
        print("Failed to read frame from camera.")
        break

    # 프레임 화면에 출력
    cv2.imshow('Live Camera', frame)

    # 'q' 키 입력 시 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting camera stream by user request.")
        break

# 카메라 자원 해제 및 모든 창 닫기
camera.release()
cv2.destroyAllWindows()