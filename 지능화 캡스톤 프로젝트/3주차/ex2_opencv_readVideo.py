import cv2

# 동영상 파일 읽기
video = cv2.VideoCapture('test_video.mp4')  # 파일 이름 지정

# 동영상 파일이 제대로 열렸는지 확인
if not video.isOpened():
    print("Error: Unable to open the video file.")
    exit()

while True:
    # 비디오의 프레임을 읽기
    ret, frame = video.read()

    # 프레임을 제대로 읽었는지 확인
    if not ret:
        print("Video playback completed.")
        break

    # 프레임을 화면에 출력
    cv2.imshow('Video Frame', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("Playback interrupted by user.")
        break

# 동영상 파일 닫기 및 모든 창 닫기
video.release()
cv2.destroyAllWindows()