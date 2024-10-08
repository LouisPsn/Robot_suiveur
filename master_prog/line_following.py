import cv2
from motor import command_motors
import numpy as np
from color_constant import *

def blackLineFolow(cap:cv2.VideoCapture, save_direction:bool, dxl):
    _, frame = cap.read()
            
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
    lower_black = np.array([0])
    upper_black = np.array([110])
            
    mask = cv2.inRange(gray, lower_black, upper_black)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (29,29))
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, _, w, _ = cv2.boundingRect(c)

        center_x = x + w // 2
        _, width, _ = frame.shape

        if center_x > width/2 + width/4:
            command_motors(30, 300, dxl)
            save_direction = True
        elif center_x < width/4:
            command_motors(300, 30, dxl)
            save_direction = True
        else:
            command_motors(300, 300, dxl)
            save_direction = False
    else:
        if not save_direction:
            command_motors(0, 0, dxl)
    return save_direction

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

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, _, w, _ = cv2.boundingRect(c)

        center_x = x + w // 2
        _, width, _ = frame.shape

        if center_x > width/3 + width/3:
            command_motors(20, 300, dxl)
            save_direction = True
        elif center_x < width/3:
            command_motors(300, 20, dxl)
            save_direction = True
        else:
            command_motors(300, 300, dxl)
            save_direction = False
    else:
        if not save_direction:
            command_motors(300, 20, dxl)
    return save_direction



def yellow_detected(cammera:cv2.VideoCapture):
    _, frame = cammera.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, LOWER_YELLOW, UPPER_YELLOW)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    return np.any(mask)