import cv2
cv2.setUseOptimized(True)
cv2.setNumThreads(4)
import numpy as np
import imutils
from divideROI import moreRefineImage

def roiCreation(imageName):
    old_img = cv2.imread("unzip/"+imageName)

    # Color filtering
    lower_bound = np.array([36, 214, 0])
    upper_bound = np.array([90, 255, 207])
    img = cv2.inRange(old_img, lower_bound, upper_bound)

    # cv2.imshow("Binary Mask", img)

    gray = cv2.cvtColor(old_img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

    edged = cv2.Canny(bfilter, 50, 200)  # Edge detection

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            location = approx
            break

    mask = np.zeros(img.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))

    # Crop 70% from the top
    initial_cropped_image = gray[x1:x2 + 1, y1:y2 + 1]
    # cv2.imshow("initial_cropped_image", initial_cropped_image)
    

    # rotate
    rotation_angle = .9  # Adjust this value as needed
    height, width = initial_cropped_image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), rotation_angle, 1.0)

    # Perform the rotation on the original image
    rotated_image = cv2.warpAffine(initial_cropped_image, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR)
    cv2.imwrite(f"inter/ocbm4-roi.png", rotated_image)
    moreRefineImage("ocbm4-roi.png")
    
    # cv2.waitKey(0)