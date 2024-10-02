import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2

# Set up camera
cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()

    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    except:
        pass

    lower_blue = np.array([60, 140, 160]) 
    upper_blue = np.array([180, 255, 255])  

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, _, w, _ = cv2.boundingRect(c)
        
        center_x = x + w // 2
        _, width, _ = frame.shape

        er = (center_x/width - 0.5)*2*200
        
        print(er)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break