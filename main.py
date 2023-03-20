import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGame:
    def __init__(self):
        self.points = []
        self.lengths = []
        self.currLen = 0
        self.allowedLen = 150
        self.prvHead = 0,0

    def update(self,imgMain,currHead):
        px,py = self.prvHead
        cx,cy = currHead
        self.points.append([cx,cy])
        dist = math.hypot(cx-px,cy-py)
        self.lengths.append(dist)
        self.currLen += dist
        self.prvHead = currHead

        if self.currLen > self.allowedLen:
            for i, length in enumerate(self.lengths):
                self.currLen -= length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currLen <= self.allowedLen:
                    break
        if (self.points):
            for i,point in enumerate(self.  points):
                if i !=0:
                    cv2.line(imgMain,self.points[i-1],self.points[i],(0,255,0),20)
            cv2.circle(imgMain, self.points[-1], 10, (255, 0, 255), cv2.FILLED)
        return imgMain

game = SnakeGame()
while True:
    success, img= cap.read()
    img = cv2.flip(img, 1)
    hands,img = detector.findHands(img, flipType=False)
    if hands:
        lmList = hands[0]["lmList"]
        pointIndex = lmList[8][0:2]
        img = game.update(img,pointIndex)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
 
