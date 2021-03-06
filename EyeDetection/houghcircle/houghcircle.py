import cv2
import numpy as np

#img = cv2.imread("eye0.jpg", 0)
#img = cv2.imread("screencap7eye0.jpg", 0)
#img = cv2.imread("screencap7eye1.jpg", 0)
#origimg = cv2.imread("eyecolor.jpg")
#origimg = cv2.imread("eye1_hough.jpg")
origimg = cv2.imread("./savedpics/lefteye9.png")
#origimg = cv2.imread("eye0_hough.jpg")

cv2.imshow("original", origimg)
cv2.waitKey(0)
img = origimg.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("img_gray", img)
cv2.imwrite("img_gray.jpg", img)
cv2.waitKey(0)
#img = cv2.adaptiveThreshold(img,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
#cv2.imshow("img_grayinvblurequiadpthresg", img)
#cv2.imwrite("img_grayinvblurequiadpthresg.jpg", img)
#cv2.waitKey(0)

cv2.bitwise_not(img, img)
cv2.imshow("img_grayinv", img)
cv2.imwrite("img_grayinv.jpg", img)
cv2.waitKey(0)
img = cv2.medianBlur(img,3)
cv2.imshow("img_grayinvblur", img)
cv2.imwrite("img_grayinvblur.jpg", img)
cv2.waitKey(0)
img = cv2.equalizeHist(img)
cv2.imshow("img_grayinvblurequi", img)
cv2.imwrite("img_grayinvblurequi.jpg", img)
cv2.waitKey(0)
#img = cv2.adaptiveThreshold(img,205, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,13,2)
#img = cv2.adaptiveThreshold(img,205, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,37,7)
#cv2.imshow("img_grayinvblurequiadpthresg", img)
#cv2.imwrite("img_grayinvblurequiadpthresg.jpg", img)
#cv2.waitKey(0)

#Center w/o thresholding: 39.5, 32.5 radius = 12.34908867

#param1 - refers to the edge threshold that will be used by the Canny edge detector
#(applied to a grayscale image). cvCanny() accepts two thresholds and is internally
#invoked by cvHoughCircles(). Therefore the higher (first) threshold is set to param1
#(passed as argument into cvHoughCircles()) and the lower (second) threshold is set
#to half of this value.

#param2- Is the value for accumulator threshold. This value is used in the accumulator
#plane that must be reached so that a line is retrieved.
#The smaller it is, the more false circles may be detected.

#Too many circles found on screencap7eye1

#dp = Inverse ratio of the accumulator resolution to the image resolution.
#For example, if dp=1 , the accumulator has the same resolution as the input image.

#minDist = Minimum distance between the centers of the detected circles. If the parameter
#is too small, multiple neighbor circles may be falsely detected in addition to a true one.
#If it is too large, some circles may be missed.

#cv2.HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) 

#Works on eye0
#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=20,minRadius=0,maxRadius=20)
#Works on screencap7eye0
#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=20,minRadius=0,maxRadius=20)
#For screencap7eye1, change minDist to 50 to reduce number of false detections, radius 25 seems to work better
#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=20,minRadius=7,maxRadius=25)
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,50,param1=150,param2=20,minRadius=7,maxRadius=10)
#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,50,param1=200,param2=20,minRadius=7,maxRadius=10)
if circles is not None:
        
    print circles
    #circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
           cv2.circle(origimg,(i[0],i[1]),i[2],(0,255,0),1) # draw the outer circle
           cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),1) # draw the outer circle
           cv2.circle(origimg,(i[0],i[1]),2,(0,0,255),1) # draw the center of the circle
           cv2.circle(img,(i[0],i[1]),2,(0,0,255),1) # draw the center of the circle


    cv2.imshow("centers", origimg)
    cv2.imwrite("coloreyecenters.jpg", origimg)
    cv2.imwrite("grayeyecenters.jpg", img)
    cv2.waitKey(0)
else:
    print "No circle"