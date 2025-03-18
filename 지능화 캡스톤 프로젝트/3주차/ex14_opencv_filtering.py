import cv2
import numpy as np


# 2D 필터 적용 함수
def apply_filter(image, kernel, filter_name):
    filtered_image = cv2.filter2D(image, -1, kernel)
    cv2.imshow(f"{filter_name}", filtered_image)
    cv2.imwrite(f"{filter_name}.jpg", filtered_image) # 필터 적용된 결과 저장

    return filtered_image

# 1. 평균 값 필터(3x3)
average_filter = np.ones((3, 3), np.float32) / 9.0
# 2. 샤프닝 필터(3x3)
sharpening_filter = np.array([[0,-1, 0],
                            [-1, 5,-1],
                            [0,-1, 0]], np.float32)
# 3. 라플라시안 필터(3x3)
laplacian_filter = np.array([[0, 1, 0],
                            [1,-4, 1],
                            [0, 1, 0]], np.float32)


image = cv2.imread('desert.jpg', cv2.IMREAD_COLOR)

apply_filter(image, average_filter,"Average Filter") # 평균 값 필터 적용
apply_filter(image, sharpening_filter,"Sharpening Filter") # 샤프닝 필터 적용
apply_filter(image, laplacian_filter,"Laplacian Filter") # 라플라시안 필터 적용

# 종료 처리
cv2.waitKey(0)
cv2.destroyAllWindows()
