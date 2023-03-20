import cvzone
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 640)

while True:
    success, img = cap.read(

    )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    print(cv2.waitKey(1))
