import numpy as np
import cv2


def Recognize(img):
    smoth_img = cv2.medianBlur(img, 15)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    threshold_img = cv2.medianBlur(threshold_img, 15)

    contours0, _ = cv2.findContours(threshold_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    wagon_s = 0.0
    height, width = img.shape[:2]
    maxS = (height * width) / 2     # Детектится контур картинки. Отбросим его таким фильтром
    wagon_box = None # Бокс под контур вагона
    for cnt in contours0:
        rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        tmp = cv2.contourArea(cnt)
        if maxS > tmp > wagon_s:
            cv2.drawContours(img, [box], 0, (255, 0, 0), 4)
            wagon_box = box
            wagon_s = tmp
    cv2.imshow('Capture', img)
    print(wagon_s)
    cv2.waitKey()
    cv2.destroyAllWindows()

