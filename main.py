import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGame:
    def __init__(self,pathFood="apple.png"):
        self.points = []
        self.lengths = []
        self.currLen = 0
        self.allowedLen = 150
        self.prvHead = 0,0
        self.imgFood = cv2.imread(pathFood,cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood,_ = self.imgFood.shape
        self.foodPoint = 0,0
        self.randomFoodLoc()
        self.score = 0
    
    def randomFoodLoc(self):
        self.foodPoint = random.randint(0,1000),random.randint(0,600)

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

        
        rx, ry = self.foodPoint
        if rx - self.wFood//2 < cx < rx + self.wFood//2 and ry - self.hFood//2 < cy < ry + self.hFood//2:
            self.randomFoodLoc()
            self.allowedLen += 40
            self.score += 1


        if (self.points):
            for i,point in enumerate(self.  points):
                if i !=0:
                    cv2.line(imgMain,self.points[i-1],self.points[i],(0,255,0),20)
            cv2.circle(imgMain, self.points[-1], 10, (255, 0, 255), cv2.FILLED)
        rx,ry = self.foodPoint
        # if not (rx - self.wFood//2 < 1280 and ry - self.hFood//2 < 720):
        #     self.randomFoodLoc()
        print(rx - (self.wFood//2),ry - (self.hFood//2))
        if not (rx - (self.wFood//2) > 0 and ry - (self.hFood//2) > 0):
            self.randomFoodLoc()
            rx,ry = self.foodPoint
        imgMain = cvzone.overlayPNG(imgMain,self.imgFood,(rx - (self.wFood//2),ry - (self.hFood//2) ))  
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
 
