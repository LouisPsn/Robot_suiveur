import cv2
import numpy as np
import pypot.dynamixel

# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])

def setup_motors():
    dxl_io.set_wheel_mode([1, 2])

def command_motors(vL, vR):
    dxl_io.set_moving_speed({1: -vL, 2: vR})

# Set up camera
cap = cv2.VideoCapture(5)
if not cap.isOpened():
    print("Error: Cannot access the camera")
    exit()

def main():
#    setup_motors()

    saved_direction = [0, 0]

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break
            
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except:
                continue
            cv2.waitKey(14)
            # cv2.imshow("gray", gray)
            
            lower_black = np.array([0])
            upper_black = np.array([120])
            
            mask = cv2.inRange(gray, lower_black, upper_black)
            # cv2.imshow("mask", mask)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (29,29))
            morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)


            # mask = cv2.erode(mask, None, iterations=2)
            # mask = cv2.dilate(mask, None, iterations=2)

            contours, _ = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                x, _, w, _ = cv2.boundingRect(c)

                center_x = x + w // 2
                _, width, _ = frame.shape

                if center_x > width/2 + width/4:
                    command_motors(40, 300)
                    saved_direction = [40, 300]
                elif center_x < width/4:
                    command_motors(300, 40)
                    saved_direction = [300, 40]
                else:
                    command_motors(300, 300)
                    saved_direction = [300, 300]
            else:
                if saved_direction[0] == saved_direction[1]:
                    command_motors(0, 0)
                else:
                    command_motors(saved_direction[0], saved_direction[1])

    except KeyboardInterrupt:
        print("Program interrupted by user.")

    finally:
        cap.release()
        command_motors(0, 0)
    

main()