import cv2 
import numpy as np 

# Set up camera
cap = cv2.VideoCapture(0)

_, frame = cap.read() 
cv2.imshow('frame', frame) 