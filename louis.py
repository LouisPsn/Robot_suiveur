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
    # lower_blue = np.array([60, 140, 160]) 
    # upper_blue = np.array([180, 255, 255])  
    # Threshold of red in HSV space 
    lower_red = np.array([50,25,25])
    upper_red = np.array([310,255,255])
  
    # preparing the mask to overlay 
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # cv2.imshow('frame', frame) 
    # cv2.imshow('mask', mask)
    
    height, width = mask.shape
    
    left = 0
    right = 0
    
    check = False
    
    for i in range (width//2, width - 1):
        print(mask[height//2, i])
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
        print(mask[height//2, i])
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
    
    
    if (er < 0.01 and er > -0.01):
        # same motor speed
        vL = 360
        vR = 360
    elif er > 00.01 :
        # the robot need to turn right (left motor turn faster)
        theta = math.atan(er/x)
        r = x/math.sin(theta)
        rL = r + robot_width//2
        rR = r - robot_width//2
        
        DL = rL * theta
        DR = rR * theta
        
        vL = 360
        vR = DR/DL*360
    else:
        # the robot need to turn left (right motor turn faster)
        er = abs(er)
        theta = math.atan(er/x)
        r = x/math.sin(theta)
        rL = r - robot_width//2
        rR = r + robot_width//2
        
        DL = rL * theta
        DR = rR * theta
        
        vL = DL/DR*360
        vR = 360
    
    return vL, vR

def command_motors(vL, vR):
    dxl_io.set_wheel_mode([1])
    dxl_io.set_moving_speed({1: -vL}) # Degrees / s
    dxl_io.set_moving_speed({2: vR}) # Degrees / s


def main():
    while(1):
        er = analyse_image()
        vL, vR  = compute_speed(er)
        # command_motors(vL, vR)
        

main()