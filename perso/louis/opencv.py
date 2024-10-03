import cv2
import numpy as np
import pypot.dynamixel

# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])

def command_motors(vL, vR):
    dxl_io.set_wheel_mode([1])
    dxl_io.set_moving_speed({1: -vL})
    dxl_io.set_moving_speed({2: vR})

# Set up camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur : Impossible d'accéder à la caméra")
    exit()

def main():
    while(1):
        _, frame = cap.read()

        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        except:
            continue

        lower_blue = np.array([140, 20, 0]) 
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
            if center_x > width/2 + width/4:
                command_motors(90, 180)
            elif center_x < width/4:
                command_motors(180, 90)
            else:
                command_motors(180, 180)
        else:
            command_motors(0, 0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            command_motors(0, 0)
            break

main()
