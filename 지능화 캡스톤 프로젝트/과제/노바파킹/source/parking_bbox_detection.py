#!/usr/bin/env python3
"""
주차장 실시간 감지 시스템
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time
from datetime import datetime
from pathlib import Path
import json

class ParkingBboxDetector:
    def __init__(self, model_path, class_names=None):
        self.model_path = model_path
        self.model = YOLO(model_path)
        
        # 클래스 이름 설정
        if class_names is None:
            self.class_names = {0: 'empty', 1: 'occupied'}
        else:
            self.class_names = class_names
            
        # 클래스별 색상 설정
        self.class_colors = {
            'empty': (0, 255, 0),      # 녹색 (사용 가능)
            'occupied': (0, 0, 255),   # 빨간색 (사용 중)
        }
        
        # 통계 초기화
        self.reset_statistics()
        
    def reset_statistics(self):
        """통계 초기화"""
        self.stats = {
            'total_detections': 0,
            'empty_count': 0,
            'occupied_count': 0,
            'frame_count': 0,
            'start_time': time.time()
        }
        
    def detect_parking_spaces(self, frame, conf_threshold=0.3):

        results = self.model.predict(
            source=frame,
            conf=conf_threshold,
            iou=0.5,
            task='detect',
            verbose=False
        )
        
        detection_result = {
            'empty_spaces': [],
            'occupied_spaces': [],
            'total_empty': 0,
            'total_occupied': 0,
            'boxes': []
        }
        
        if results and len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            
            for i, box in enumerate(boxes):
                # 바운딩박스 좌표 (xyxy 형식)
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                confidence = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                
                # 클래스 이름 가져오기
                class_name = self.class_names.get(class_id, f'class_{class_id}')
                
                box_info = {
                    'bbox': (x1, y1, x2, y2),
                    'confidence': confidence,
                    'class_id': class_id,
                    'class_name': class_name,
                    'color': self.class_colors.get(class_name, (255, 255, 255))
                }
                
                detection_result['boxes'].append(box_info)
                
                # 클래스별 분류
                if class_name == 'empty':
                    detection_result['empty_spaces'].append(box_info)
                    detection_result['total_empty'] += 1
                elif class_name == 'occupied':
                    detection_result['occupied_spaces'].append(box_info)
                    detection_result['total_occupied'] += 1
        
        return detection_result
    
    def draw_bounding_boxes(self, frame, detection_result):

        annotated_frame = frame.copy()
        height, width = frame.shape[:2]
        
        # 각 박스 그리기
        for box_info in detection_result['boxes']:
            x1, y1, x2, y2 = box_info['bbox']
            confidence = box_info['confidence']
            class_name = box_info['class_name']
            color = box_info['color']

            
            # # 라벨 텍스트 준비
            # label = f"{class_name}: {confidence:.2f}"
            if class_name == 'occupied':
                # 바운딩박스 그리기 (두꺼운 선)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

                label = "car"

                # 텍스트 크기 계산
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)

                # 라벨 배경 그리기
                label_y = y1 - 10 if y1 - 10 > text_height else y1 + text_height + 10
                cv2.rectangle(annotated_frame,
                             (x1, label_y - text_height - 5),
                             (x1 + text_width + 10, label_y + 5),
                             color, -1)

                # 라벨 텍스트 그리기 (흰색)
                cv2.putText(annotated_frame, label,
                           (x1 + 5, label_y),
                           font, font_scale, (255, 255, 255), thickness)

        return annotated_frame
    
    def draw_statistics_overlay(self, frame, detection_result):
        annotated_frame = frame.copy()
        height, width = frame.shape[:2]
        
        # 통계 업데이트
        self.stats['frame_count'] += 1
        self.stats['empty_count'] = detection_result['total_empty']
        self.stats['occupied_count'] = detection_result['total_occupied']
        self.stats['total_detections'] = detection_result['total_empty'] + detection_result['total_occupied']
        
        # 상단 통계 패널
        panel_height = 100
        panel_color = (0, 0, 0, 180)  # 반투명 검은색
        
        # 반투명 배경
        overlay = annotated_frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, annotated_frame, 0.3, 0, annotated_frame)
        
        # 통계 텍스트
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        thickness = 2
        
        # Occupancy 정보 (빨간색)
        occupancy_text = f"Occupancy: {self.stats['occupied_count']}"
        cv2.putText(annotated_frame, occupancy_text, (20, 40), 
                   font, font_scale, (0, 0, 255), thickness)
        
        # Available 정보 (녹색)
        available_text = f"Available: {self.stats['empty_count']}"
        cv2.putText(annotated_frame, available_text, (20, 80), 
                   font, font_scale, (0, 255, 0), thickness)
        
        # 총 공간 정보 (흰색)
        total_text = f"Total: {self.stats['total_detections']}"
        cv2.putText(annotated_frame, total_text, (width - 200, 40), 
                   font, font_scale, (255, 255, 255), thickness)
        
        # 점유율 계산 및 표시
        if self.stats['total_detections'] > 0:
            occupancy_rate = (self.stats['occupied_count'] / self.stats['total_detections']) * 100
            rate_text = f"Rate: {occupancy_rate:.1f}%"
            cv2.putText(annotated_frame, rate_text, (width - 200, 80), 
                       font, font_scale, (255, 255, 255), thickness)
        
        return annotated_frame
    
    def process_video(self, video_path, output_path=None, max_frames=None, realtime=False):
        
        # 비디오 열기
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"비디오 열기 실패: {video_path}")
            return
        
        # 비디오 정보
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"비디오 정보: {width}x{height}, {fps}FPS, {total_frames}프레임")
        
        # 최대 프레임 설정
        process_frames = min(max_frames, total_frames) if max_frames else total_frames
        
        # 출력 비디오 설정
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 처리 시작
        frame_count = 0
        start_time = time.time()
        paused = False
        
        try:
            while frame_count < process_frames:
                if not paused:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    frame_count += 1
                    
                    # 주차 공간 감지
                    detection_result = self.detect_parking_spaces(frame)
                    
                    # 바운딩박스 그리기
                    annotated_frame = self.draw_bounding_boxes(frame, detection_result)
                    
                    # 통계 오버레이
                    annotated_frame = self.draw_statistics_overlay(annotated_frame, detection_result)
                    
                    # 진행률 표시
                    progress = frame_count / process_frames
                    progress_text = f"Frame: {frame_count}/{process_frames} ({progress*100:.1f}%)"
                    cv2.putText(annotated_frame, progress_text, (10, height - 20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    # 출력 저장
                    if out:
                        out.write(annotated_frame)
                    
                    # 화면 표시
                    cv2.imshow('Parking Bbox Detection', annotated_frame)
                    
                    # 진행률 로깅
                    if frame_count % 100 == 0:
                        elapsed = time.time() - start_time
                        print(f" 진행률: {progress*100:.1f}% | 점유: {detection_result['total_occupied']} | 가용: {detection_result['total_empty']} | 경과: {elapsed:.1f}초")
                    
                    # 실시간 재생
                    if realtime and fps > 0:
                        time.sleep(1.0 / fps)
                
                # 키보드 입력
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Exit")
                    break
        
        except KeyboardInterrupt:
            print("\n Ctrl+C 중단")
        
        finally:
            cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()
        
        # 최종 통계
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n 처리 완료!")
        print(f"    최종 통계:")
        print(f"  - 처리 프레임: {frame_count}")
        print(f"  - 점유 공간: {self.stats['occupied_count']}")
        print(f"  - 가용 공간: {self.stats['empty_count']}")
        print(f"  - 총 공간: {self.stats['total_detections']}")
        print(f"  - 처리 시간: {total_time:.2f}초")
        print(f"  - 평균 FPS: {frame_count/total_time:.2f}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='주차장 바운딩박스 감지')
    parser.add_argument('--video', type=str, default='./video/office20250605-093156-1749083516.mp4', help='입력 비디오 경로')
    parser.add_argument('--model', type=str, 
                       default='./runs/detect/yolov12n_test_6/weights/best.pt',
                       help='YOLO 모델 경로')
    parser.add_argument('--output', type=str, help='출력 비디오 경로')
    parser.add_argument('--conf', type=float, default=0.6, help='신뢰도 임계값')
    parser.add_argument('--max-frames', type=int, help='최대 처리 프레임 수')
    parser.add_argument('--realtime', action='store_true', help='실시간 재생')
    
    args = parser.parse_args()

    
    try:
        # 감지기 초기화
        detector = ParkingBboxDetector(args.model)
        
        # 비디오 처리
        detector.process_video(
            video_path=args.video,
            output_path=args.output,
            max_frames=args.max_frames,
            realtime=args.realtime
        )
        
    except Exception as e:
        print(f" 오류 발생: {e}")

if __name__ == "__main__":
    main() 