import cv2

# Read the image
image = cv2.imread('Lenna.png', cv2.IMREAD_GRAYSCALE)

# Display the image
cv2.imshow('Lenna', image)

# Wait for a key press and close the image window
cv2.waitKey(0)
cv2.destroyAllWindows()