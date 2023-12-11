import cv2

def moreRefineImage(imageNmae):
    initial_cropped_image = cv2.imread("inter/"+imageNmae)
    # Further crop and resize for the front image
    # new_x1, new_y1, new_x2, new_y2 = 10, 20, 300, 115  # Adjust these coordinates
    new_x1, new_y1, new_x2, new_y2 = 4, 3, 300, 115  # Adjust these coordinates
    further_cropped_image_front = initial_cropped_image[new_y1:new_y2 + 1, new_x1:new_x2 + 1]
    resized_further_cropped_image_front = cv2.resize(further_cropped_image_front, (150, 50))
    # cv2.imshow("Filtered image", resized_further_cropped_image_front)
    cv2.imwrite(f"inter/ocbm4.1-roi.png", resized_further_cropped_image_front)

    # Further crop and resize for the after image
    # further_cropped_image_after = initial_cropped_image[20:115, 290:370]  # Adjust these coordinates
    further_cropped_image_after = initial_cropped_image[23:120, 290:370]  # Adjust these coordinates
    resized_further_cropped_image_after = cv2.resize(further_cropped_image_after, (50, 50))
    # cv2.imshow("After image", resized_further_cropped_image_after)
    cv2.imwrite(f"inter/ocbm4.2-roi.png", resized_further_cropped_image_after)
    # cv2.waitKey(0)