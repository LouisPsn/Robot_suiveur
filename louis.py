import cv2 
import numpy as np 
import math
import pypot.dynamixel

# Set up camera
cap = cv2.VideoCapture(0)

# Set up motors
# ports = pypot.dynamixel.get_available_ports()
# if not ports:
#     exit('No port')
# dxl_io = pypot.dynamixel.DxlIO(ports[0])


def analyse_image():
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
        
        
        er = (center_x/width - 0.5)*2*400
    else:
        er = 0    
        
    # print(er)
    
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
    
    
    if (er < 5 and er > -5):
        # same motor speed
        vL = 360
        vR = 360
    elif er > 5 :
        # the robot need to turn right (left motor turn faster)
        theta = math.atan(er/x)
        r = x/math.sin(theta)
        rL = r + robot_width//2
        rR = r - robot_width//2
        
        DL = rL * theta
        DR = rR * theta
        
        vL = 360
        vR = int(DR/DL*360)
    else:
        # the robot need to turn left (right motor turn faster)
        er = abs(er)
        theta = math.atan(er/x)
        r = x/math.sin(theta)
        rL = r - robot_width//2
        rR = r + robot_width//2
        
        DL = rL * theta
        DR = rR * theta
        
        vL = int(DL/DR*360)
        vR = 360
    
    print(vL, vR)
    
    return vL, vR

def command_motors(vL, vR):
    dxl_io.set_wheel_mode([1])
    dxl_io.set_moving_speed({1: -vR}) # Degrees / s
    dxl_io.set_moving_speed({2: vR}) # Degrees / s


def main():
    while(1):
        er = analyse_image()
        vL, vR  = compute_speed(er)
        # command_motors(vL, vR)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        
        

main()