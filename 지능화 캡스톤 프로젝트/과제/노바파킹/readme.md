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

![자동라벨링 예시](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/autolabel_ex.png)


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


### 실험 구성 및 평가 방법 
#### 하드웨어 및 소프트웨어 환경
   - OS : Ubuntu 25.04
   - GPU : NVIDIA RTX 5070ti 16G
   - 메모리 : 32GB
   - 소프트웨어 : PyTorch, TensorFlow, Detectron2
   - 개발환경 : PyCharm

#### 학습 데이터셋
   - 건수 : 14,908장의 주차장 학습 이미지
   - 다양성 : 다양한 날씨(sunny, overcast, rainy), 주차장 유형(UFPR04, UFPR05, PUCPR)
   - 라벨링 : 각 이미지에는 차량의 바운딩 박스와 주차 공간의 상태(Empty, Occupied) 라벨링 데이터 사용
   - 데이터구성 : 학습세트(11,177건), 검증세트(2,486건), 테스트세트(1,245)
   - 출처 : https://web.inf.ufpr.br/vri/databases/parking-lot-database/

#### Auto label 데이터
   - 건수 : 24장의 주차장 학습 이미지
   - 다양성 : 다양한 카메라 위치(30m, 40m, 50m, 60m, 70m,75m) 
   - 라벨링 : 각 이미지에는 차량의 바운딩 박스와 주차 공간의 상태(Empty, Occupied) 라벨링
   - 데이터구성 : 학습(16건), 검증(5건), 테스트(3)


#### 모델별 성능 평가 및 비교
   - 세 가지 객체 인식 모델의 성능을 다음과 같은 지표를 사용하여 평가 진행
      - 정밀도(Precision) : 모델이 occupied 으로 예측한 주차 공간 중 실제로 사용중인 비율
      - 재현율(Recall) : 실제 사용 중인 주차 공간 중 모델이 정확히 occupied 으로 예측한 비율
      - F1-Score : 정밀도와 재현율의 조회 평균
      - 평균 정밀도(mAP) : 여러 IoU임계값 에서의 평균 정밀도
      - 처리속도(FPS) : 초당 처리할 수 있는 프레임 수
   - IoU (Intersection over Union) : 객체 탐지 평가 지표 사용
   
![IoU](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/IoU.png)
   - 출처 : https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/


#### 객체 인식 모델 성능 비교 결과
   - 본 실험에서는 Faster R-CNN, Mask R-CNN, YOLOv12 세 가지 객체 인식 모델을 대상으로 주요 평가 지표에 따라 성능을 비교하였다. 평가 항목은 Precision, Recall, F1-score, mAP@0.5, mAP@0.5:0.95, FPS로 구성하였다.
![평가표](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/evel_grid.png)
  
   - 그 결과, YOLO v12 모델은 정밀도(Precision), 재현율(Recall), F1-Score 등 전체 평가 지표에서 우수한 성능을 보였다.
![챠트](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/eval_chart1.png)
   - Faster R-CNN과 Mask R-CNN 모델은 Precision과 mAP@0.5 지표에서 강점을 보였으며, 이는 상대적으로 정밀한 탐지 능력을 요구하는 환경에 적합하다는 것을 보여준다.
   - 그러나 두 모델 모두 추론 속도 측면에서는 YOLOv12보다 크게 낮아 실시간 응용에는 다소 제한적일 수 있다. 정밀한 인식이 필요한 환경에 더 적합한 것을 시험을 통해 알 수 있었다.
   - 결론적으로, YOLO v12는 정확도와 속도를 모두 갖춘 모델로서, 실시간 주차 공간 모니터링 시스템에 실시간 감시 모델로 적합한 모델로 평가됩니다.

![챠트](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/eval_chart2.png)

## 결과 및 분석 (Results & Analysis)
### Faster R-CNN
![Faster R-CNN](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/faster_r-cnn.png)


### Mask R-CNN
![Mask R-CNN](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/mask_r-cnn.png)


### YOLO 12
![yolo12](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/yolo12n.png)


### Auto Label 구현 결과 
![yolo12](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/autolabel.png)


### 실시간 주차 감시 구현

   - 객체 인식 모델의 학습 결과와 성능 비교 분석을 통해, 본 연구에서는 YOLO 12n이 주차 모니터링 시스템에 가장 적합한 모델임을 제안한다.
   - YOLO 12n은 실시간 처리 능력과 정확도를 제공하며 주차 관리 시스템과 같은 실시간 운용에 필요한 특성을 균형 있게 갖추고 있기 때문이다.

![실시간감시](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/detect_system.png)   


## 한계점 및 토론 (Limitations & Discussions)
### 한계점 및 개선점
   - 1) 한계점 
      - CCTV 영상 촬영 문제 : 영상장비 촬영 각도에 따라서 차량에 의해 가려지는 주차면 사각지대 문제
      - 스트리밍 영상 문제 : 프레임 단위로 변경되는 영상 신호에 따라서 오탐 하는 경우 존재
      - Auto label 정확도 : 학습되지 않은 신규 주차장의 빈 주차공간 및 주차된 차량을 제대로 객체 인식 못 하는 문제

   - 2) 개선점 
      - 모델 경량화 : 모델 양자화, 증류 등의 기업을 활용한 모델 경량화하여 저사양의 하드웨어 에서도 실행 가능하도록 개선 필요.
      - 악천후 대응 : 저조도 환경에, 비, 눈, 안개등의 악천후 상황에서도 안정적으로 동작하는 모델 개선 필요
      - 프라이버시 보호 : 영상 처리 과정에서 번호판, 개인 식별 정보 등을 자동으로 마스킹 처리 연구
      - 객체인식 데이터 활용 : 폴리곤 형태의 라벨 데이터를 활용해서 모델 정확도 향상

## 향후 연구방향
### 연구 결론 
   - 본 연구에서는 Faster R-CNN, Mask R-CNN, YOLO 객체 인식 모델을 활용한 주차 모니터링 시스템 프로토타입 개발을 진행하였습니다. 
      - 기존 수작업 라벨링 방식의 비효율적인 문제를 자동 레벨링을 방법을 제시
      - 세 가지 객체 인식 모델을 분석한 결과, YOLO v12이 실시간 처리 능력과 정확도의 균형 측면에서 실시간 주차 모니터링 시스템에 적합한 모델임을 확인하였다.
      - 실시간 주차 모니터링 시스템 구현을 위한 단계별 접근 방법을 제시하였다.
   - 인공지능 기술을 활용한 시스템은 전통적인 무선 자기센서(Wireless Magnetometer) 방식과 달리 개별 센서 설치가 불필요하여 초기 구축비용과 지속적인 유지보수 비용을 현저히 절감효과를 가져올 수 있을 것으로 기대합니다.

### 향후 연구 방향 
   - 엣지 컴퓨팅 최적화 : 주차장 현장의 엣지 디바이스에서 효율적으로 동작할 수 있는 경량화된 모델 연구
   - 환경 변화 적응성 : 환경 변화에 따른 객체 인식 정확도를 높이기 위해 도메인 적응 및 모델 기반 데이터 증감 연구
   - 비지도 학습 : 라벨링 된 데이터 없이도 주차 패턴을 학습할 수 있는 비지도 학습 연구

## 참고문헌
   - [1] “10 monster traffic jams from around the world,” https://www.bbc.com/news/magazine-19716687, accessed: 2018-05-18.
   - [2] “Searching for parking costs the UK£23.3 billion a year,” http://inrix.com/press-releases/parking-pain-uk/, accessed: 201805-18.
   - [3] “SMART PARKING WITH PIXEL-WISE ROI SELECTION FOR  VEHICLE DETECTION USING YOLOV8, YOLOV9, YOLOV10, AND YOLOV11” https://arxiv.org/html/2412.01983v2
   - [4] “Real-time image-based parking occupancy detection using deep learning” https://ceur-ws.org/Vol-2087/paper5.pdf
   - [5] “Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks” https://arxiv.org/abs/1506.01497
   - [6] ”Auxiliary Domain-guided Adaptive Detection in Adverse Weather Conditions” https://openaccess.thecvf.com/content/ACCV2024/html/Fu_Auxiliary_Domain-guided_Adaptive_Detection_in_Adverse_Weather_Conditions_ACCV_2024_paper.html





# 주차장 실시간 감시 구현 내용

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

