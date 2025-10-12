# 객체 인식 기반 스마트 주차 모니터링 시스템 개발

# 프로젝트 개요
## 연구 목표
- 최신 객체 인식 모델 사용 실시간 주차 상태를 탐지하는 스마트 주차 관리 시스템 개발
- 주차 공간 객체 인식을 위한 자동 라벨링 시스템 설계 및 구현
- 언제, 어디서나 누구나 사용할 수 있는 웹·앱 기반의 서비스 구현

## 프로젝트 배경 및 필요성
### 프로젝트 배경
- 전통적인 무선 자기 센서(Wireless Magnetometer) 방식은 설치 비용이 높고 유지보수가 복잡하며, 특히 대규모 주차장에서는 확장성에 한계가 존재한다[2].
- 실시간 주차장 영상을 기반으로 한 객체 인식 기술을 통해 차량의 주차 여부와 공간 상태를 정확하게 파악할 수 있으며, 이를 바탕으로 운전자에게 주차 가능 공간 정보를 실시간으로 제공할 수 있다.
- 최근 딥러닝 기술의 발전으로 인해 인공지능 기반의 객체 탐지 및 인스턴스 분할 기술은 기존 주차 관리 시스템의 한계를 극복할 수 있는 대안으로 주목받고 있다.

### 프로젝트 필요성
- 인공지능 기반의 접근법은 기존 센서 기반 솔루션 대비 경제적으로 저렴하며, 주차 공간 인식의 정확성을 향상시킬 수 있다[6].
- 그러나, CNN 기반의 객체 인식 모델인 Faster R-CNN, Mask R-CNN, YOLO는 정확도가 비교적 높은 편이지만, 새로운 환경이나 객체에 적응하기 위해 막대한 재훈련 또는 미세 조정 비용을 필요하다[7].
- Transformer 기반 아키텍처를 통해 영상 및 시각 정보와 언어 정보를 효과적으로 결합하여 더 정확한 객체 탐지를 가능하게 한다 [7].
- 따라서 스마트 주차 시스템 구현을 위해 Transformer 기반 객체 인식 모델의 도입이 필요하다.

## 문제정의 및 주요 기여점
### CNN 기반 모델 성능평가 결과
이전 실험에서는 Faster R-CNN, Mask R-CNN, YOLOv12 세 가지 객체 인식 모델을 대상으로 한 주요 평가 결과에서 정밀도, 재현율, F1-Score 모두 94% 이상의 우수한 성능을 보였다. 

| 모델          | 정밀도 (Precision) | 재현율 (Recall) | F1-Score | mAP@0.5 | mAP@0.5:0.95 | FPS    |
|---------------|-------------------|-----------------|----------|---------|---------------|--------|
| Faster R-CNN  | 0.9886            | 1.0000          | 0.9942   | 99.01   | 98.71         | 29.68  |
| Mask R-CNN    | 0.9442            | 0.9754          | 0.9595   | 84.76   | 42.99         | 23.70  |
| YOLO v12      | 0.9989            | 0.9986          | 0.9987   | 99.46   | 98.74         | 118.23 |

- CNN 기반 모델은 새로운 주차장 환경에서 객체 탐지 모델의 적응성이 부족하게 나타난다.
![1.오탐사례](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/1.%EC%98%A4%ED%83%90%EC%82%AC%EB%A1%80.png)

### 문제점
- 다양한 주차 환경에서의 일반화 문제
- 새로운 주차장 환경에 대한 객체 탐지 모델의 적응성 부족, 그리고 정확도와 속도를 모두 만족시키는 모델 선정의 어려움
- 학습되지 않은 신규 주차장에서 빈 주차 공간이나 주차된 차량을 제대로 객체 인식하지 못하는 문제

### 주요 기여점
- CNN 모델이 가진 근본적인 한계인 ‘사전 정의된 카테고리에의 의존’을 극복하기 위해, Transformer 기반 Grounding DINO 모델을 도입하여 스마트 주차장 객체 인식의 성능을 향상시키고 새로운 환경에 대한 적응력을 높이고자 한다[7][8].
- 본 연구는 컴퓨터 비전 기술을 활용한 주차 공간 인식 정확도 향상과 기존 주차관리 방식의 한계를 극복하고, 객체 인식 기반 주차관리 시스템의 기반 기술을 설계하고 구현하고자 한다.


# 방법 및 구현 (Methodology & Implementation)
본 논문에서는 Transformer 기반 Grounding DINO를 활용한 주차 모니터링 시스템을 설계하고, 자동 라벨링 기반의 효율적인 데이터셋 구축 방법을 제시하였으며, 실시간 주차 상태 모니터링이 가능한 웹·앱 기반 통합 서비스 플랫폼을 구현하여 그 성능을 시험한 내용을 다룬다. 
## 스마트 주차 모니터링 시스템 구성도
![2.구성도](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/2.%EA%B5%AC%EC%84%B1%EB%8F%84.png)   

## Grounding DINO 모델 아키텍처
Grounding DINO 모델은 텍스트와 이미지 특징을 트랜스포머로 결합해 객체를 탐지하는 모델이다.
![3.GroundingDINO](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/3.GroundingDINO.png)

## 스마트 주차 모니터링 시스템 구성
### 주요 모듈 설명
- 데이터 수집 모듈 : 주차장 모형에 설치된 CCTV를 통해 실시간 영상 데이터 수집한다. 
- 데이터 처리 모듈 : 수집된 영상 데이터를 전처리하고, 객체 인식 모델에 입력할 수 있는 형태로 변환한다.
- AI 학습모듈 : Transformer 기반 Grounding DINO 모델을 사용하여 주차 차량과 주차 공간 라벨데이터를 학습한다.
- AI 추론모듈 : 학습모델 데이터를 사용하여 객체를 추론하고 평가한다.
- 주차 공간 감시 모듈 : 실시간으로 인식한 정보를 바탕으로 주차 공간의 상태(empty, occupied)를 실시간으로 감시한다.
- 사용자 인터페이스 : 주차 공간 상태 정보를 사용자에게 시각적으로 제공한다.
- 서버연계 모듈 : 주차 공가정보, 차량데이터, 통계 정보 등을 저장관리하고 알림을 사용자에게 알린다.

### 자동 라벨링 방법
- 초기 데이터셋 구성 : 소수의 수동 라벨링 된 이미지로 초기 데이터셋을 구성한다.
- 사전학습 모델 활용 : 사전 훈련된 Grounding DINO 사전 학습된 모델을 활용한다.
- 라벨데이터 생성
   - (주차점유) : 사전 학습된 모델을 사용하여 새로운 주차장 이미지에 대해서 주차상태를 추론한다.
   - (평균 주차공간 계산) : 다수의 주차점유 데이터를 기반으로 아래의 수식으로 평균 주차공간을 계산한다.
   ![4.수식1](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/4.%EC%88%98%EC%8B%9D1.png)

- (빈주차공간) : 빈 주차공간 객체 라벨링 작업은 주차점유 공간을 뺀 나머지 공간에 대해서 빈공간의 라벨데이터를 생성한다
   ![5.수식2](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/5.%EC%88%98%EC%8B%9D2.png)
![6.라벨링예시](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/6.%EB%9D%BC%EB%B2%A8%EB%A7%81%EC%98%88%EC%8B%9C.png)
   
### 실시간 주차 모니터링 프로세스
- 웹캠 비디오 입력 : 주차장에 설치한 CCTV 카메라에서 실시간으로 입력되는 비디오 스트림(RTSP: Real-Time Streaming Protocol)을 입력받는다. 
   - 카메라에서 전송되는 비디오 스트림을 처리하기 위한 객체를 생성한다.
   - 주차 공간 탐지를 위해 모델을 초기화한다.
- 주차공간 탐지 : 비디오 스트림을 프레임 단위로 처리하여 객체를 탐지한다.
   - 주차 공간 탐지 및 차량 탐지하고 주차 상태를 분석한다.
   - 객체 추적 결과 바운딩 박스 좌표와 클래스 라벨을 추출한다.
   - 주차 공간의 상태를 시각적으로 표시하고 처리된 비디오를 출력한다.
- 주차 빈공간 탐지 : 현재 주차 가능한 공간 수를 표시한다.
- 알림 서비스: 실시간 주차공간 정보를 사용자에게 알린다.
![7.실시간모니터링프로세스](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/7.%EC%8B%A4%EC%8B%9C%EA%B0%84%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4.png)

## 실험 구성 및 평가 방법 (Experiment Settings)
### 하드웨어 및 소프트웨어 환경
- OS : Ubuntu 25.04
- GPU : NVIDIA RTX 5070ti 16G
- 메모리 : 32GB
- 소프트웨어 : PyTorch, TensorFlow, Detectron2
- 개발환경 : PyCharm, xCode, Android Studio
   
### 학습 데이터셋
- 건수 : 14,908장의 주차장 학습 이미지
- 다양성 : 다양한 날씨(sunny, overcast, rainy), 주차장 유형(UFPR04, UFPR05, PUCPR)
- 라벨링 : 각 이미지에는 차량의 바운딩 박스와 주차 공간의 상태(Empty, Occupied) 라벨링 데이터 사용
- 데이터구성 : 학습세트(11,177건), 검증세트(2,486건), 테스트세트(1,245)
- 출처 : https://web.inf.ufpr.br/vri/databases/parking-lot-database/

### Auto label 데이터
- 건수 : 36장의 주차장 학습 이미지
- 다양성 : 미니주차장  세트#1, 세트 #2
- 라벨링 : 각 이미지에는 차량의 바운딩 박스와 주차 공간의 상태(Empty, Occupied) 라벨링
- 데이터구성 : 학습(36건), 테스트(13)

### 미니 주차장 세트
미니카 주차장 놀이매트 마우스패드 토미카주차장, 레이싱 미니카 세트 등 국내 온라인 쇼핑몰에서 구입하여 미니 세트장을 만들어서 시험에 활용하였다.
- 물품 구매 : https://www.coupang.com/vp/products/8142207053?itemId=23139423921, https://www.coupang.com/vp/products/8093050293 
![8.미니주차장세트](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/8.%EB%AF%B8%EB%8B%88%EC%A3%BC%EC%B0%A8%EC%9E%A5%EC%84%B8%ED%8A%B8.png)

### 모델별 성능 평가 및 비교
- 세 가지 객체 인식 모델의 성능을 다음과 같은 지표를 사용하여 평가 진행
   - 정밀도(Precision) : 모델이 occupied 으로 예측한 주차 공간 중 실제로 사용중인 비율
   - 재현율(Recall) : 실제 사용 중인 주차 공간 중 모델이 정확히 occupied 으로 예측한 비율
   - F1-Score : 정밀도와 재현율의 조회 평균
   - 평균 정밀도(mAP) : 여러 IoU임계값 에서의 평균 정밀도
   - 처리속도(FPS) : 초당 처리할 수 있는 프레임 수
- IoU (Intersection over Union) : 객체 탐지 평가 지표 사용
   
![IoU](https://github.com/chohi22/Industrial-AI/blob/main/%EC%A7%80%EB%8A%A5%ED%99%94%20%EC%BA%A1%EC%8A%A4%ED%86%A4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%EA%B3%BC%EC%A0%9C/%EB%85%B8%EB%B0%94%ED%8C%8C%ED%82%B9/%EB%B3%B4%EA%B3%A0%EC%84%9C/IoU.png)
   - 출처 : https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/


# 결과 및 분석 (Results & Analysis)
## Grounding DINO 학습결과
![9.학습결과](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/9.%ED%95%99%EC%8A%B5%EA%B2%B0%EA%B3%BC.png)

## 노바파킹 세부 기능
### 객체인식 트래킹 알고리즘
RTSP 프로토콜로 수신한 CCTV 영상의 각 프레임에서 객체를 탐지하고, 이전 프레임의 트랙과 IoU 기준으로 매칭하여 동일 객체의 ID를 부여하고 유지한다.

- 알고리즘 1. IoU 기반 Tracking-by-Detection
```python
1: Input Tracking-by-Detection(dets_xyxy, dets_score, dets_cls)
2: for t in tracks: t.age += 1
3: A = [t.bbox for t in tracks]
4: iou = IoU_matrix(A, dets_xyxy) # IoU 계산
5: if max(iou) ≥ T:
6:  Assign detection to track (ID preserved) # 매칭된 트랙 ID 유지
7: else:
8:  create new track with new ID
9: Return updated track set with IDs and states.
```

![10.트래킹출력](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/10.%ED%8A%B8%EB%9E%98%ED%82%B9%EC%B6%9C%EB%A0%A5.png)

### 불법주차 챠랑 검출
주차면 ROI를 활용해 불법주차 차량을 검출 하고 체류 시간을 기준으로 불법 주차 차량을 구별한다.
- 알고리즘 2. ROI 기반 Parking-violation-Detection
```python
   1: Input Tracking-by-Detection(dets_xyxy, dets_score, dets_cls)
   2: for t in tracks: 
   3:     veh_poly ← bbox_to_polygon(t.bbox)  #polygon 생성
   4:     if exists in IoU (veh_poly , dets_xyxy)   #IoU 계산      
   5:           match ← ("NO_PARK", j)
   6:     if last_event_time >= curtime + t     # 체류 판단 
   7:           emit_event(t, match)
   8: Return illegal_parking_events.   
```
![11.불법주차a](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/11.%EB%B6%88%EB%B2%95%EC%A3%BC%EC%B0%A8a.png)

![11.불법주차b](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/11.%EB%B6%88%EB%B2%95%EC%A3%BC%EC%B0%A8b.png)



## Auto Label 구현 결과
주차장의 차량 객체 인식 결과를 바탕으로 주차공간 박스 집합의 IoU를 확인해 빈 주차공간을 판별한 뒤, 각 주차공간에 ‘occupied’와 ‘empty’ 레이블을 부여한다.
![12.autolabel](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/12.autolabel.png)

### 주차공간 박스 집합
- 알고리즘 3. AverageBox
```python
   1: Input AverageBox(indices I, boxes XYXY, image_width W, image_height H)
   2: for i in I: 
   3:     (x1, y1, x2, y2) ← XYXY[i]
   4:     Sx1+=x1; Sy1+=y1; Sx2+=x2; Sy2+=y2      
   5: ax1=round(Sx1/n), ay1=round(Sy1/n), ax2=round(Sx2/n), ay2=round(Sy2/n)  # 평균(반올림):
   6: ax1=clamp(ax1, 0, W-1), ax2=clamp(ax2, 0, W-1), ay1=clamp(ay1, 0, H-1), ay2=clamp(ay2, 0, H-1) # 경계 클리핑
   7: x_left=min(ax1, ax2), x_right=max(ax1, ax2), y_top =min(ay1, ay2), y_bottom=max(ay1, ay2) # 좌표 정규화
   8: Return (x_left, y_top, x_right, y_bottom): 평균 박스.   
```


## 미학습 신규 주차장 추론 결과
트랜스포머 기반 Grounding DINO 객체 탐지 모델은 학습되지 않은 신규 주차장에서도 94% 이상의 객체 탐지 성능을 보여 준다. 다시 말해, CNN 기반의 모델들 보다 새로운 환경에 대한 적응력이 우수한 모델이라고 볼 수 있다.
![13.newplot](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/13.newplot.png)


## Grounding DINO 모델 성능 비교
Grounding DINO 객체 탐지 모델은 학습되지 않은 신규 주차장에서도 94% 이상의 객체 탐지 성능을 보여주었다. 이는 CNN 기반 모델들보다 새로운 환경에 대한 적응력이 우수함을 확인할 수 있었다.  

| 모델           | 정밀도   | 재현율   | F1-Score | mAP@0.5 | mAP@0.5:0.95 | FPS    |
|----------------|-----------|-----------|-----------|----------|---------------|--------|
| Faster R-CNN   | 0.9886    | 1.0000    | 0.9942    | 99.01    | 98.71         | 29.68  |
| Mask R-CNN     | 0.9442    | 0.9754    | 0.9595    | 84.76    | 42.99         | 23.70  |
| YOLO v12       | 0.9989    | 0.9986    | 0.9987    | 99.46    | 98.74         | 118.23 |
| Grounding DINO | 0.9567    | 0.9834    | 0.9698    | 95.23    | 89.45         | 42.15  |

## 미학습 환경에서의 일반화 성능
미학습 환경에서도 94.12%의 높은 탐지 성능을 달성하여 Faster  R-CNN(78.34%) 대비 20.1%, YOLO v12(81.67%) 대비 15.2%의 성능 향상을 확인하였다.

| 환경조건     | Grounding DINO | Faster R-CNN | YOLO v12 | 개선율   |
|--------------|----------------|---------------|-----------|----------|
| 학습된 주차장 | 95.23%         | 99.01%        | 99.46%    | -4.2%   |
| 미학습 주차장 | 94.12%         | 78.34%        | 81.67%    | +15.6%  |


## AI 스마트 주차장 대시보드
세종특별자치시청 주차장의 실시간 현황을 모니터링하고 관리하는 웹 기반 대시보드를 가정하고 개발하였다. Mapbox GL JS를 활용한 인터랙티브 지도와 실시간 데이터 시각화를 통해 주차장 운영 상황을 한눈에 파악할 수 있다.
![14.deshboard](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/14.deshboard.png)
![15.deshboard](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/15.deshboard.png)
![16.deshboard](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/16.deshboard.png)

### 주요기능
  - 실시간 주차장 현황 모니터링: 총 주차면, 점유 주차면, 장애인 주차면 실시간 표시
  - 인터랙티브 지도: Mapbox GL JS 기반 주차장 위치 표시 및 클릭 이벤트 처리
  - CCTV 모니터링: 주차장 내 CCTV 카메라 상태 및 위치 정보 제공
  - 폴리곤 영역 표시: 주차장 구역별 시각적 구분 및 클릭 이벤트
  - 실시간 데이터 업데이트: 주기적으로 자동 데이터 갱신

## AI 스마트 주차장 모바일
React와 TypeScript를 기반으로 구축된 주차장 관리 시스템으로 네이버 지도 API를 활용하여 실시간 주차장 정보를 제공하고, CCTV 모니터링을 통해 스마트한 주차 경험을 제공하는 반응형웹 애플리케이션이다.
![17.mogile.gif](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/17.mobileweb.gif)


## AI 스마트 주차장 모바일 App
### 안드로이드 화면
![18.android](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/18.android.png)

### IOS 화면
![19.ios](https://github.com/chohi22/Industrial-AI/blob/main/%EC%BD%9C%EB%A1%9C%ED%82%A4%EC%9B%80/%EA%B0%9D%EC%B2%B4%20%EC%9D%B8%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EC%8A%A4%EB%A7%88%ED%8A%B8%20%EC%A3%BC%EC%B0%A8%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EB%B0%9C/images/19.ios.png)

### 주요기능
- 웹 기반 주차장 관리 시스템을 네이티브 앱으로 래핑
- React Native WebView를 통한 웹-네이티브 브리지 통신
- 네트워크 오류 시 자동 재시도 및 폴백 메커니즘
- TypeScript를 활용한 타입 안전성 보장


# 한계점 및 토론 (Limitations & Discussions)
## 한계점 및 개선점
### 한계점
- 조명 변화에 따른 객체 인식 저하 : 불빛이 없는 야간에는 객체 탐지 인식률이 저하되는 문제가 발생
- 실험실 환경 한계 : 실제 주차장 CCTV의 조도·색온도·기상·카메라 배치(높이 · 초점거리 · 왜곡) 등 현장 특성이 충분히 반영되지 못함
- 렌즈 왜곡 문제 : 실제 주차면이 직사각형이 아니거나 카메라 각도 와 굴절 · 렌즈 왜곡되어 IoU 오차 발생

### 개선점
- MLOps: 모델 학습 파이프라인, 추론 파이프라인, ROI 자동 보정 등 데이터 수집->학습->배포->모니터링->재학습까지의 과정을 자동화하므로써 지속적인 모델 개선이 필요하다.
- 강화학습 : 주차공간 관심 구역(ROI)을 강화학습으로 자동 생성 뒤, 후보정 작업을 통해 개선할 필요가 있다

# 향후 연구 방향
## 기대효과
- 야외주차장 인공지능 기반 주차관리 체계구축
- 물리적 센서 설치 비용절감 및 유지보수 비용절감
- 지역내 스마트 주차환경구축으로 시민 편의성 증가 및 민원 감소
- 불법주정차 감소
- 화재 등 안전·사고 예방 가능
- 수요가 집중되는 시간대에 유휴 주차 공간 정보를 사용자에게 실시간으로 제공함으로써, 주차장을 찾는 데 소요되는 시간과 차량 대기 시간 감소
- 이로 인한 대기오염까지 감소 예상
 
## 연구 결론 
본 연구에서는 Faster R-CNN, Mask R-CNN, YOLO, Grounding DINO 객체 인식 모델을 활용한 주차 모니터링 시스템 프로토타입 개발을 진행하였습니다. 
- 수작업 라벨링 방식의 비효율적인 문제를 자동 레벨링을 방법을 제시
- 기존 CNN 기반의 모델들은 새로운 환경이나 객체에 적응하기 위해 막대한 재훈련 또는 미세 조정 비용을 필요하여 트랜스포머 기반 Grounding DINO모델을 제안한다. 
- 객체 인식 트래킹, 불법 주차 인식 등 노바파킹(NOVA Parking) 만의 특화된 기능을 구현하고 시험하였다.
실시간 주차 모니터링 시스템 구현을 위한 단계별 접근 방법을 제시하였다.
인공지능 기술을 활용한 시스템은 전통적인 무선 자기센서(Wireless Magnetometer) 방식과 달리 개별 센서 설치가 불필요하여 초기 구축비용과 지속적인 유지보수 비용을 현저히 절감효과를 가져올 수 있을 것으로 기대합니다.

## 향후 연구 방향 
- 엣지 컴퓨팅 최적화 : 주차장 현장의 엣지 디바이스에서 효율적으로 동작할 수 있는 경량화된 모델 연구
- 환경 변화 적응성 : 환경 변화에 따른 객체 인식 정확도를 높이기 위해 도메인 적응 및 모델 기반 데이터 증감 연구
- 비지도 학습 : 라벨링 된 데이터 없이도 주차 패턴을 학습할 수 있는 비지도 학습 연구

 # 참고문헌
 - [1]” 효율적인 주차 환경을 위한 입출차 데이터 기반 주차 공간 파악 시스템”, https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003113913
 - [2] “SMART PARKING WITH PIXEL-WISE ROI SELECTION FOR  VEHICLE DETECTION USING YOLOV8, YOLOV9, YOLOV10, AND YOLOV11” https://arxiv.org/html/2412.01983v2
 - [3] “Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks” https://arxiv.org/abs/1506.01497
 - [4] “Real-time image-based parking occupancy detection using deep learning” https://ceur-ws.org/Vol-2087/paper5.pdf
 - [5] “Searching for parking costs the UK£23.3 billion a year,” http://inrix.com/press-releases/parking-pain-uk/, accessed: 201805-18.
 - [6] ”Auxiliary Domain-guided Adaptive Detection in Adverse Weather Conditions” https://openaccess.thecvf.com/content/ACCV2024/html/Fu_Auxiliary_Domain-guided_Adaptive_Detection_in_Adverse_Weather_Conditions_ACCV_2024_paper.html
 - [7] “Grounding DINO: Marrying DINO with Grounded  Pre-Training for Open-Set Object Detection” https://link.springer.com/chapter/10.1007/978-3-031-72970-6_3
 - [8] “COUNTGD: Multi-Modal Open-World Counting” https://proceedings.neurips.cc/paper_files/paper/2024/hash/57c56985d9afe89bf78a8264c91071aa-Abstract-Conference.html
 - [9] 파이토치 트랜스포머를 활용한 자연어 처리와 컴퓨터비전 심층학습, 위키북스
 - [10] A Camera-based Smart Parking System Employing  Low-complexity Deep Learning for Outdoor  Environments, https://ieeexplore.ieee.org/document/8966901