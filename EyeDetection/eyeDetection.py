from __future__ import division
import numpy as np
import cv2
import os.path
import time
import sys
import pyautogui

pyautogui.FAILSAFE = False


eyeXYFrames = []

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('trained_cascade.xml')
#cv2gpu.init_cpu_detector('haarcascade_eye_tree_eyeglasses.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
pupil_params = cv2.SimpleBlobDetector_Params()
glint_params = cv2.SimpleBlobDetector_Params()

cap = cv2.VideoCapture(0)

def getXYofPupils():
    global cap
    pupilXYs = []
    #Array will be like: [[leftpupilX,leftpupilY], [rightpupilX,rightpupilY]]
    foundbotheyes = 0
    while 1:
        ret, imgCap = cap.read()
        img = imgCap.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        circles = None
        for (x,y,w,h) in faces:
            #Select region of interest by cropping image
            facecenterX = x+w/2
            facecenterY = y+h/2

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            savedFace = roi_color.copy()
            
            #eyes = eye_cascade.detectMultiScale(roi_gray)
            eyes = eye_cascade.detectMultiScale(roi_color, 1.1, 2, 0, (30,30), (70, 70))
            if len(eyes) == 2:
                (ex0, ey0, ew0, eh0) = eyes[0]
                (ex1, ey1, ew1, eh1) = eyes[1]
                
                #Make the left eye in the frame eye0 for calcuation purposes
                if ex1 < ex0:
                    tmpx = ex1
                    tmpy = ey1
                    tmpw = ew1
                    tmph = eh1
                    ex1 = ex0
                    ey1 = ey0
                    ew1 = ew0
                    eh1 = eh0
                    ex0 = tmpx
                    ey0 = tmpy
                    ew0 = tmpw
                    eh0 = tmph
                
                
                ceye0 = roi_color[ey0:ey0+eh0,ex0:ex0+ew0]
                ceye1 = roi_color[ey1:ey1+eh1,ex1:ex1+ew1]
                
                gceye0 = cv2.cvtColor(ceye0, cv2.COLOR_BGR2GRAY)
                gceye0 = cv2.fastNlMeansDenoising(gceye0,None,10,7)
                cv2.bitwise_not(gceye0, gceye0)
                gceye0 = cv2.medianBlur(gceye0, 3)
                gceye0 = cv2.equalizeHist(gceye0)
                #ret,gceye0 = cv2.threshold(gceye0, 175, 255, cv2.THRESH_BINARY)
                #gceye0 = cv2.adaptiveThreshold(gceye0,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

                gceye1 = cv2.cvtColor(ceye1, cv2.COLOR_BGR2GRAY)
                gceye1 = cv2.fastNlMeansDenoising(gceye1,None,10,7)
                cv2.bitwise_not(gceye1, gceye1)
                gceye1 = cv2.medianBlur(gceye1, 3)
                gceye1 = cv2.equalizeHist(gceye1)
                #gceye1 = cv2.adaptiveThreshold(gceye1,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

                #cv2.imshow('threshold_eye0',gceye0)
                #circles0 = cv2.HoughCircles(gceye0,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=20,minRadius=7,maxRadius=25)
                #circles0 = cv2.HoughCircles(gceye0,cv2.HOUGH_GRADIENT,2,50,param1=50,param2=20,minRadius=7,maxRadius=13)
                circles0 = cv2.HoughCircles(gceye0,cv2.HOUGH_GRADIENT,2,50,param1=150,param2=20,minRadius=7,maxRadius=10)
                eye0x = 0
                eye0y = 0
                eye1x = 0
                eye1y = 0
                if circles0 is not None:
                    for i in circles0[0,:]:
                        eye0x = x+ex0+i[0]
                        eye0y = y+ey0+i[1]
                        cv2.circle(ceye0,(i[0],i[1]),i[2],(0,255,0),1) # draw the outer circle
                        cv2.circle(ceye0,(i[0],i[1]),2,(0,0,255),1) # draw the center of the circle
                        
                #circles1 = cv2.HoughCircles(gceye1,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=20,minRadius=7,maxRadius=25)
                #circles1 = cv2.HoughCircles(gceye1,cv2.HOUGH_GRADIENT,2,50,param1=50,param2=20,minRadius=7,maxRadius=13)
                circles1 = cv2.HoughCircles(gceye1,cv2.HOUGH_GRADIENT,2,50,param1=150,param2=20,minRadius=7,maxRadius=10)
                if circles1 is not None:
                    for i in circles1[0,:]:
                        #print "eye1: Center:", (x+ex1+i[0], y+ey1+i[1]), "Radius:", i[2]
                        eye1x = x+ex1+i[0]
                        eye1y = y+ey1+i[1]
                        cv2.circle(ceye1,(i[0],i[1]),i[2],(0,255,0),1) # draw the outer circle
                        cv2.circle(ceye1,(i[0],i[1]),2,(0,0,255),1) # draw the center of the circle    
                    
                    if circles0 is not None:
                        foundbotheyes = 1
                        pupilXYs.append([eye0x-facecenterX, eye0y-facecenterY])
                        pupilXYs.append([eye1x-facecenterX, eye1y-facecenterY])
                        break
            
        if foundbotheyes:
            break

    
    return pupilXYs




calibImg = cv2.imread('Calibration.jpg')
calibImgBkup = calibImg.copy()
cv2.namedWindow('Calibration', cv2.WINDOW_AUTOSIZE)

cv2.imshow('Calibration', calibImg)
while 1:
    k = cv2.waitKey(0)
    #Space key
    if k == 32:
        break
    elif k == ord('q'):
        cap.release()
        sys.exit(0)


#calibCircles are the points to draw
calibCircles = [[10,10], [10,470], [10, 930], [640,10], [640,470], [640, 930], [1270,10], [1270,470], [1270, 930]]
#calibPoints are the true x,y values for the mapping
calibPoints = [[10,65], [10,527], [10,990], [10,65], [10,527], [10,990], [1270,65], [1270,527], [1270,990]]

#These hold the pupil x to actual x, and pupil y to actual y
leftEyeXs = []
leftEyeYs = []
rightEyeXs = []
rightEyeYs = []



for i in range(0, len(calibCircles)-1):
    cv2.destroyAllWindows()
    calibImg = calibImgBkup.copy()
    cv2.circle(calibImg,(calibCircles[i][0],calibCircles[i][1]),5,(0,0,255),10)
    cv2.imshow('Calibration #' + str(i+1), calibImg)
    counter = 0
    record = 0
    while 1:
        if record:
            capturedXYpairs = getXYofPupils()
            leftEyeXYs = capturedXYpairs[0]
            rightEyeXYs = capturedXYpairs[0]
            
            leftEyeXs.append([leftEyeXYs[0], calibPoints[i][0]])
            leftEyeYs.append([leftEyeXYs[1], calibPoints[i][1]])

            rightEyeXs.append([rightEyeXYs[0], calibPoints[i][0]])
            rightEyeYs.append([rightEyeXYs[1], calibPoints[i][1]])

            counter += 1
            print "Counter =", counter
        
        k = cv2.waitKey(10)
        if k == ord('a'):
            print "Starting to record"
            #Start recording frames
            record = 1
        elif k == ord('z'):
            if counter >= 10:
                print "Have enough frames"
                cv2.destroyAllWindows()
                break
        elif k == ord('q'):
            cap.release()
            sys.exit(0)


cv2.destroyAllWindows()


while 1:
    capturedXYpairs = getXYofPupils()
    k = cv2.waitKey(10)
    if k == ord('q'):
        break

print leftEyeXs
print rightEyeXs

cap.release()
cv2.destroyAllWindows()
sys.exit(0)