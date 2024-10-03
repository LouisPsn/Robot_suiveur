import cv2
import numpy as np

def getHisto(color_h_min:int, color_h_max:int, frame):
    #_, frame = cap.read() 
    # It converts the BGR color space of image to HSV color space 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL) 
    h = cv2.extractChannel(hsv,0)   
    s = cv2.extractChannel(hsv,1)

    cv2.imshow("h", h)
    #cv2.imshow("s", s)
    #cv2.imshow("v", v)

    # Threshold of blue in HSV space 
    # lower_blue = np.array([60, 140, 160]) 
    # upper_blue = np.array([180, 255, 255])  
    # Threshold of red in HSV space 
  
    # preparing the mask to overlay 
    mask1 = cv2.inRange(h, np.array([color_h_min]), np.array([color_h_max]))
    
    
    mask2 = cv2.inRange(s, np.array([0]), np.array([255]))
    
    
    mask = cv2.bitwise_and(mask1, mask2)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.imshow("mask", mask)
    frame = cv2.bitwise_and(frame, mask)
    return frame
    
    

# img = cv2.imread("./parcours.png")
# cv2.imshow("base",img)
#cv2.imshow("red",getHisto(0,20, img))
# cv2.imshow("green",getHisto(80,120, img))
#cv2.imshow("blue",getHisto(160,180, img))

cap = cv2.VideoCapture(5)

while(True):
    _, frame = cap.read()
    cv2.imshow("base",frame)
    cv2.imshow("result", getHisto(140, 180, frame))
    cv2.waitKey(14)

