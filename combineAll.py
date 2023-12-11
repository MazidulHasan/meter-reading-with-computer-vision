import cv2
import argparse
import numpy as np
from csvWork.saveDataInCSVFile import saveAsCSVFile
from roiCreation import roiCreation
import ast

def print_all_digits(imageName):
    # print("Image Name", imageName)
    # parser = argparse.ArgumentParser()
    # # parser.add_argument("-p", "--path", default="assets/tmp.jpeg")
    # parser.add_argument("-p", "--path", default="unzip/"+imageName)
    # args = vars(parser.parse_args())

    # # test: dbs.jpg | ocbc.jpg
    # img_color = cv2.imread(args["path"])
    # img_color = cv2.resize(img_color, None, None, fx=0.5, fy=0.5)
    # img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # blurred = cv2.GaussianBlur(img, (7, 7), 0)
    # blurred = cv2.bilateralFilter(blurred, 5, sigmaColor=50, sigmaSpace=50)
    # edged = cv2.Canny(blurred, 130, 150, 255)

    # cv2.imshow("Outline of device", edged)
    # cv2.waitKey(0)

    # cnts, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # # sort contours by area, and get the largest
    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

    # cv2.drawContours(img_color, cnts, 0, (75, 0, 130), 4)
    # cv2.imshow("Target Contour", img_color)
    # cv2.waitKey(0)

    # x, y, w, h = cv2.boundingRect(cnts[0])
    # roi = img[y : y + h, x : x + w]
    # cv2.imshow("ROI", roi)

    # # img_name = re.search("(?<=\/)(.*)(?=\.jpg)", args["path"]).group(1)

    # # cv2.imwrite(f"inter/{img_name}-roi.png", roi)
    # cv2.imwrite(f"inter/ocbm4-roi.png", roi)
    # cv2.waitKey(0)

    roiCreation(imageName)
    # more refine the image
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    CYAN = (255, 255, 0)
    DIGITSDICT = {
        (1, 1, 1, 1, 1, 1, 0): 0,
        (0, 1, 1, 0, 0, 0, 0): 1,
        (1, 1, 0, 1, 1, 0, 1): 2,
        (1, 1, 1, 1, 0, 0, 1): 3,
        (0, 1, 1, 0, 0, 1, 1): 4,
        (1, 0, 1, 1, 0, 1, 1): 5,
        (1, 0, 1, 1, 1, 1, 1): 6,
        (1, 1, 1, 0, 0, 1, 0): 7,
        (1, 1, 1, 1, 1, 1, 1): 8,
        (1, 1, 1, 1, 0, 1, 1): 9,
    }
    roi_color = cv2.imread("inter/ocbm4.1-roi.png")

    # resize
    # height, width, _ = roi_color.shape
    # crop_top = int(height * 0.05)
    # crop_bottom = int(height * 0.7)
    # crop_right = int(width * 0.83)
    # roi_color = roi_color[crop_top:crop_bottom, :crop_right, :]
    # cv2.imshow("First data", roi_color)

    roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)

    RATIO = roi.shape[0] * 0.2

    roi = cv2.bilateralFilter(roi, 5, 30, 60)
    trimmed = roi
    # trimmed = roi[int(RATIO) :, int(RATIO) : roi.shape[1] - int(RATIO)]
    roi_color = roi_color[int(RATIO) :, int(RATIO) : roi.shape[1] - int(RATIO)]
    # cv2.imshow("Blurred and Trimmed", trimmed)
    cv2.waitKey(0)

    edged = cv2.adaptiveThreshold(
        trimmed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 3
    )
    # cv2.imshow("Edged", edged)
    cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 5))
    dilated = cv2.dilate(edged, kernel, iterations=1)

    # cv2.imshow("Dilated", dilated)
    cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    # make more thick
    dilated = cv2.dilate(dilated, kernel, iterations=1)
    

    # cv2.imshow("Dilated x2", dilated)
    cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (18, 1),)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # cv2.imshow("Eroded", eroded)
    cv2.waitKey(0)

    h = roi.shape[0]
    ratio = int(h * 0.08)
    eroded[-ratio:,] = 0
    eroded[:, :ratio] = 0

    # cv2.imshow("Eroded + Black", eroded)
    cv2.waitKey(0)

    cnts, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digits_cnts = []

    canvas = trimmed.copy()
    cv2.drawContours(canvas, cnts, -1, (255, 255, 255), 1)
    # cv2.imshow("All Contours", canvas)
    cv2.waitKey(0)

    canvas = trimmed.copy()
    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if h > 20:
            digits_cnts += [cnt]
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
            cv2.drawContours(canvas, cnt, 0, (255, 255, 255), 1)
            # cv2.imshow("Digit Contours", canvas)
            cv2.waitKey(0)

    print(f"No. of Digit Contours: {len(digits_cnts)}")


    # cv2.imshow("Digit Contours", canvas)
    cv2.waitKey(0)


    sorted_digits = sorted(digits_cnts, key=lambda cnt: cv2.boundingRect(cnt)[0])

    canvas = trimmed.copy()


    for i, cnt in enumerate(sorted_digits):
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
        cv2.putText(canvas, str(i), (x, y - 3), FONT, 0.3, (0, 0, 0), 1)

    # cv2.imshow("All Contours sorted", canvas)
    cv2.waitKey(0)

    digits = []
    canvas = roi.copy()
    for cnt in sorted_digits:
        (x, y, w, h) = cv2.boundingRect(cnt)
        roi = eroded[y : y + h, x : x + w]
        print(f"W:{w}, H:{h}")
        # convenience units
        # qW, qH = int(w * 0.25), int(h * 0.15)
        qW, qH = int(w * 0.40), int(h * 0.20)
        fractionH, halfH, fractionW = int(h * 0.05), int(h * 0.5), int(w * 0.25)

        # seven segments in the order of wikipedia's illustration
        sevensegs = [
            ((0, 0), (w, qH)),  # a (top bar)
            ((w - qW, 0), (w, halfH)),  # b (upper right)
            ((w - qW, halfH), (w, h)),  # c (lower right)
            ((0, h - qH), (w, h)),  # d (lower bar)
            ((0, halfH), (qW, h)),  # e (lower left)
            ((0, 0), (qW, halfH)),  # f (upper left)
            # ((0, halfH - fractionH), (w, halfH + fractionH)) # center
            (
                (0 + fractionW, halfH - fractionH),
                (w - fractionW, halfH + fractionH),
            ),  # center
        ]

        # initialize to off
        on = [0] * 7

        for (i, ((p1x, p1y), (p2x, p2y))) in enumerate(sevensegs):
            region = roi[p1y:p2y, p1x:p2x]
            print(
                f"{i}: Sum of 1: {np.sum(region == 255)}, Sum of 0: {np.sum(region == 0)}, Shape: {region.shape}, Size: {region.size}"
            )
            if np.sum(region == 255) > region.size * 0.5:
                on[i] = 1
            print(f"State of ON: {on}")

        digit = DIGITSDICT[tuple(on)]
        print(f"Digit is: {digit}")
        digits += [digit]
        cv2.rectangle(canvas, (x, y), (x + w, y + h), CYAN, 1)
        cv2.putText(canvas, str(digit), (x - 5, y + 6), FONT, 0.3, (0, 0, 0), 1)
        # cv2.imshow("Digit", canvas)
        # cv2.waitKey(0)

    print(f"Digits on the token are: {digits}")
    stringDigit = digits
    result_integer = int(''.join(map(str, stringDigit)))
    if result_integer > 1000:
        digits[0] =0
        digits[1] =0
        digits[2] =0
    
    saveAsCSVFile(imageName,digits)
