import cv2
import pytesseract
import threading
import time
from pytesseract import Output

cv2.namedWindow("Capture", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Capture", 1280, 720)
last_detection_time = 0.0   # Время, когда в последний раз задетектился номер вагона
yes_new_data = False        # Флаг о наличии задетекченных номеров


def MakeJSON():
    print("Make JSON")


def OCR(image):
    global last_detection_time
    global yes_new_data
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 3 --psm 6'

    details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')

    numbers = []
    total_boxes = len(details['text'])
    # Убираем 'пустые' слова
    for nm in range(total_boxes):
        if details['text'][nm] == 8:
            numbers.append(details['text'][nm])
            last_detection_time = time.time()
            yes_new_data = True
    print(numbers)

    if len(numbers) == 0:
        if (time.time() - last_detection_time) > 30.0 and yes_new_data is True:
            MakeJSON()

    for sequence_number in range(total_boxes):
        if int(details['conf'][sequence_number]) > 30:
            (x, y, w, h) = (
                details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],
                details['height'][sequence_number])
            # threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Capture', image)

    # with open('result_text.txt', 'w', newline="") as file:
    #     csv.writer(file, delimiter=" ").writerows(parse_text)


def RTSP_Cpture():
    vcap = cv2.VideoCapture("http://10.29.34.176:8080/video")
    # vcap = cv2.VideoCapture("rtsp://10.22.116.83:8080/h264_pcm.sdp")
    ret, frame = vcap.read()
    return frame


if __name__ == '__main__':
    while True:
        img = RTSP_Cpture()
        # image = cv2.imread('test.png')
        OCR(img)
        cv2.waitKey(1)
