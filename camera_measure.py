import cv2 
import numpy as np 

# Set up camera
cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read() 
    cv2.imshow('frame', frame) 

    cv2.waitKey(14)

cv2.destroyAllWindows() 
cap.release()