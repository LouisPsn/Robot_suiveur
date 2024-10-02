import cv2 
import numpy as np 
import math
import pypot.dynamixel

# Set up camera
cap = cv2.VideoCapture(0)

# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])


def analyse_image():
    
    image_width = 400
    
    _, frame = cap.read() 
    # It converts the BGR color space of image to HSV color space 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
      
    # Threshold of blue in HSV space 
    lower_blue = np.array([60, 35, 140]) 
    upper_blue = np.array([180, 255, 255])  
    # Threshold of red in HSV space 
    # lower_red = np.array([50,25,25])
    # upper_red = np.array([310,255,255])
  
    # preparing the mask to overlay 
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # cv2.imshow('frame', frame) 
    # cv2.imshow('mask', mask)
    
    height, width = mask.shape
    
    left = 0
    right = 0
    
    check = False
    
    for i in range (width//2, width - 1):
        if (mask[height//2, i] - mask[height//2, i + 1] > 10 or mask[height//2, i] - mask[height//2, i + 1] < -10):
            if check == False:
                left = i
                check = True
            else:
                right = i
            if i < width - 1 + 5:
                i += 5
            else:
                i = width - 1
    
    
    for i in range (0, width//2 - 1):
        if (mask[height//2, i] - mask[height//2, i + 1] > 10 and mask[height//2, i] - mask[height//2, i + 1] < -10):
            if check == False:
                left = i
                check = True
            else:
                right = i
            if i < width//2 - 1 + 5:
                i += 5
            else:
                i = width//2 - 1
    er = (left + right)//2 - width//2
    
    er = i - width//2
    er = er * image_width
    
    return er   
    
    
    

def compute_speed(er):
    # All distance are integers in milimeters
    # All angle are in °
    x = 100
    robot_width = 145
    robot_height = 100
    wheel_perimeter = 162
    
    vL = 0
    vR = 0
    
    print(er)
    
    if (er < 0.01 and er > -0.01):
        # same motor speed
        dxl_io.set_moving_speed({1: -360}) # Degrees / s
        dxl_io.set_moving_speed({2: 360}) # Degrees / s
    elif er > 00.01 :
        # the robot need to turn right (left motor turn faster)
        dxl_io.set_moving_speed({1: -360}) # Degrees / s
        dxl_io.set_moving_speed({2: 0}) # Degrees / s
    else:
        # the robot need to turn left (right motor turn faster)
        dxl_io.set_moving_speed({1: 0}) # Degrees / s
        dxl_io.set_moving_speed({2: 360}) # Degrees / s
    

def command_motors(vL, vR):
    dxl_io.set_wheel_mode([1])


def main():
    while(1):
        er = analyse_image()
        compute_speed(er)        

main()

cv2.destroyAllWindows() 
cap.release()