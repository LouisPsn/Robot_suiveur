import cv2
from motor import command_motors
import numpy as np
from color_constant import *

def lineFollow(mask, frame, save_direction, dxl):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, _, w, _ = cv2.boundingRect(c)
        
        center_x = x + w // 2
        _, width, _ = frame.shape
        
        if center_x > width/2 + width/4:
            command_motors(20, 220, dxl)
            save_direction = True
        elif center_x < width/4:
            command_motors(220, 20, dxl)
            save_direction = True
        else:
            command_motors(220, 220, dxl)
            save_direction = False
    else:
        if not save_direction:
            command_motors(0, 0, dxl)


def blackLineFolow(cap:cv2.VideoCapture, save_direction:bool, dxl):
    _, frame = cap.read()

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        return

    lower_black = np.array([0])
    upper_black = np.array([80])
    
    mask = cv2.inRange(gray, lower_black, upper_black)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (29,29))
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    lineFollow(morph, frame, save_direction, dxl)

def redLineFolow(cap:cv2.VideoCapture, save_direction:bool, dxl):
    _, frame = cap.read()

    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    except:
        return

    mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask = mask1 | mask2

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    lineFollow(mask, frame, save_direction, dxl)



def yellow_detected(cammera:cv2.VideoCapture):
    _, frame = cammera.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, LOWER_YELLOW, UPPER_YELLOW)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    return np.any(mask)