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

def setup_motors():
    dxl_io.set_wheel_mode([1, 2])

def print_image(frame ):
    cv2.imshow('Image avec rectangle englobant', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    
    
def analyse_image():
    if not cap.isOpened():
        print("Erreur lors de l'ouverture de la caméra")
    else:
        # Lire une trame de la caméra
        _, frame = cap.read()
        _, frame = cap.read()
    #frame = cv2.imread('test.jpeg', 0)
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    except:
        pass

    #lower_blue = np.array([60, 140, 160]) 
    #upper_blue = np.array([180, 255, 255])  
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        
        #frame_123 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        #cv2.rectangle(frame_123, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.circle(frame_123, (x + w // 2 , y + h // 2), 5, (0, 255, 0), -1 )
        #print_image(frame_123)
        height, width = frame.shape[:2]
        center_robot_x = width
        center_robot_y = height
        
        center_detect_x = x + w // 2
        center_detect_y = y + h // 2

        _, width, _ = frame.shape
        
        #er = (center_x/width - 0.5)*2*200
        #er = 0    
    else:
        center_detect_x = 0
        center_detect_y =0
        center_robot_x = 0
        center_robot_y = 0
        
    # print(er)
    
    return center_detect_x, center_detect_y, center_robot_x, center_robot_y  
    
    
    

def compute_speed(center_detect_x, center_detect_y, center_robot_x, center_robot_y):
    # All distance are integers in milimeters
    # All angle are in °
    
    hard_virage = False
    ecart_en_x = center_robot_x - center_detect_x
    ecrat_en_y = center_robot_y - center_detect_y
    
    if (ecrat_en_y < 0):
            hard_virage = True
            
    if (ecart_en_x < 35 and ecart_en_x > -35 ):
        # same motor speed
        return 360, 360
    elif ecart_en_x > 1 :
        if (ecart_en_x > 0.5 * center_robot_x): #Petit virage à gauche car l'ecart entre le centre du rectangle et du robot est faible 
            if(hard_virage):
                return 180, 0
            else:  
                return 180,90
        else:
            if(hard_virage):
                return 360, 0
            else:  
                return 360, 90
            
    else:
        if (ecart_en_x < 1.5 * center_robot_x): #petit virage a droite
            if(hard_virage):
                return 0, 1800
            else:  
                return 90, 180
        else:
            if(hard_virage):
                return 0, 360
            else:  
                return 90, 360

def command_motors(vL, vR):
    dxl_io.set_moving_speed({1: -vL, 2: vR})


def main():
    setup_motors()
    try:
        while(1):
            center_detect_x, center_detect_y, center_robot_x, center_robot_y = analyse_image()
            vL, vR  = compute_speed(center_detect_x, center_detect_y, center_robot_x, center_robot_y)
            command_motors(vL, vR)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally: 
        cap.release()
        command_motors(0, 0)
        
main()