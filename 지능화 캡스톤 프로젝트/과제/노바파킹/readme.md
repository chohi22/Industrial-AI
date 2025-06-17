# 객체 인식 기반 스마트 주차 모니터링 시스템 개발

## 연구 목표
   - Faster R-CNN, Mask R-CNN, YOLO 최신 객체 인식 모델을 비교·분석
   - 각 모델의 성능을 평가하고 최적의 모델을 제안
   - 주차 공간 객체 인식을 위한 자동 라벨링 시스템을 설계하고 구현
   - 실시간 주차 상태를 모니터링 할 수 있는 스마트 주차 관리 시스템을 개발


## 스마트 주차 모니터링 시스템 설계
   - 데이터 수집 모듈 : 주차장 모형에 설치된 CCTV를 통해 실시간 영상 데이터 수집한다. 
   - 데이터 처리 모듈 : 수집된 영상 데이터를 전처리하고 객체 인식 모델에 입력할 수 있는 형태로 변환한다.
   - AI 학습모듈 : Faster R-CNN, Mask R-CNN, YOLO 딥러닝 모델을 사용하여 주차된 차량과 주차 공간 라벨데이터를 학습한다.
   - AI 추론모듈 : 학습모델 데이터를 사용하여 객체를 추론하고 평가한다.
   - 주차 공간 감시 모듈 : 실시간으로 인식한 정보를 바탕으로 주차 공간의 상태(empty, occupied)를 실시간으로 감시한다.
   - 사용자 인터페이스 : 주차 공간 상태 정보를 사용자에게 시각적으로 제공한다.
   - 서버연계 모듈 : 주차 공가정보, 차량데이터, 통계 정보 등을 저장관리하고 알림을 사용자에게 알린다.
![시스템 개요](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B0%9C%EB%85%90%EB%8F%84.png)

## 자동 라벨링 방법
   - 초기 데이터셋 구성 : 소수의 수동 라벨링 된 이미지로 초기 데이터셋을 구성한다.
   - 사전학습 모델 활용 : 사전 훈련된 Faster R-CNN, Mask R-CNN 사전 학습된 모델을 활용한다.
   - YOLO 모델  라벨링 : 사전 학습된 모델을 사용하여 새로운 이미지에 대한 자동 라벨링을 수행한다.
![bound box](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/boundbox.png)
   - class_id : 0 = Empty, 1 = occupied
   - x_center : 전체 이미지 너비 기준 비율 x좌표
   - y_center : 전체 이미지 너비 기준 비율 y좌표
   - with : 박스 너비 비율
   - height : 박스 높이 비율

   ![bound box](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/autolabel_ex.png)


## 실시간 주차 모니터링 프로세스
   - 웹캠 비디오 입력 : 주차장에 설치한 고해상도 CCTV 카메라에서 실시간으로 입력되는 비디오 스트림(RTSP: Real-Time Streaming Protocla)을 입력받는다. 
      - 카메라에서 실시간으로 입력되는 비디오 스트림을 처리하기 위한 객체를 생성한다.
      - 주차 공간 탐지를 위해 YOLO12n 모델을 초기화한다.
   - 주차공간 탐지 : 비디오 스트림을 프레임 단위로 처리하여 객체를 탐지한다.
      - 주차 공간 탐지 및 차량 탐지하고 주차 상태를 분석한다.
      - 객체 추적 결과 바운딩 박스 좌표와 클래스 라벨을 추출한다.
      - 주차 공간의 상태를 시각적으로 표시하고 처리된 비디오를 출력한다.
   - 주차 빈공간 탐지 : 현재 주차 가능한 공간 수를 표시한다.
   - 알림 서비스: 실시간 주차공간 정보를 사용자에게 알린다.


![실시간 감시](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/realtime_detect.png)


# 주차장 실시간 감시 구현

## 시스템 소개

이 시스템은 YOLO 모델을 사용하여 실시간으로 주차 공간의 점유 상태를 감지하는 프로그램입니다. 주차 공간이 비어있는지 차량이 주차되어 있는지를 자동으로 감지하고, 시각적으로 표시합니다.

## 주요 기능

- 실시간 주차 공간 감지
- 빈 공간/점유 공간 구분
- 실시간 통계 정보 표시


## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install opencv-python numpy ultralytics
```

2. YOLO 모델 준비:
   - 학습된 YOLO 모델 파일(.pt)이 필요합니다
   - 기본 경로: `./runs/detect/yolov12n_test_6/weights/best.pt`

## 실행 방법

### 기본 실행
```bash
python parking_bbox_detection.py
```

### 옵션을 사용한 실행
```bash
python parking_bbox_detection.py --video [비디오경로] --model [모델경로] --output [출력경로] --conf [신뢰도] --realtime
```

### 실행 옵션 설명

- `--video`: 입력 비디오 파일 경로
  - 기본값: `./video/office20250605-093156-1749083516.mp4`
- `--model`: YOLO 모델 파일 경로
  - 기본값: `./runs/detect/yolov12n_test_6/weights/best.pt`
- `--output`: 결과 비디오 저장 경로 (선택사항)
- `--conf`: 감지 신뢰도 임계값 (0.0 ~ 1.0)
  - 기본값: 0.6
- `--max-frames`: 처리할 최대 프레임 수 (선택사항)
- `--realtime`: 실시간 재생 모드 활성화

## 실행 예시

1. 기본 설정으로 실행:
```bash
python parking_bbox_detection.py
```

2. 커스텀 비디오와 모델로 실행:
```bash
python parking_bbox_detection.py --video ./my_video.mp4 --model ./my_model.pt
```

3. 실시간 재생 모드로 실행:
```bash
python parking_bbox_detection.py --realtime
```

4. 모든 옵션을 사용한 실행:
```bash
python parking_bbox_detection.py --video ./input.mp4 --model ./model.pt --output ./result.mp4 --conf 0.5 --max-frames 1000 --realtime
```

## 실행 중 단축키

- `q`: 프로그램 종료


## 출력 정보

실행 중 화면에 표시되는 정보:
- 현재 점유된 주차 공간 수
- 가용 주차 공간 수
- 총 주차 공간 수
- 점유율 (%)
- 처리 진행률

