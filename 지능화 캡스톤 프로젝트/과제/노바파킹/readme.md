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

