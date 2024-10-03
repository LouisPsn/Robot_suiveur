import cv2 
import numpy as np 
import math
import pypot.dynamixel
import time


# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])


def get_coordinate():
    print("Enter x :")
    x = input()
    print("Enter y :")
    y = input()
    print("Enter theta :")
    theta = input()
    x = int(x)
    y = int(y)
    theta = int(theta)

    return x, y, theta


def compute_motor_command(x, y, theta_util):
    wheel_perimeter = 162
    robot_width = 145
    
    if (y < 0):
        dxl_io.set_wheel_mode([1])
        dxl_io.set_moving_speed({2: 60}) # Degrees / s
        dxl_io.set_moving_speed({1: 60}) # Degrees / s
        time.sleep(3)
        y = -y
        x = -x        
    
    
    theta_i = math.atan(x/y)
    distance = math.sqrt(x**2 + y**2)
    theta = math.pi - 2*(math.pi/2 - theta_i)
    r = (distance/2)/math.sin(theta/2)
    
    if x > 0:
        rL = r + robot_width/2
        rR = r - robot_width/2
        
        DL = rL * theta
        DR = rR * theta
        
        vL = 720
        vR = 720*(DR/DL)
        wait_time = (DL/wheel_perimeter)/(vL/360)
    else:
        print("ici")
        rL = -r - robot_width/2
        rR = -r + robot_width/2
        
        DL = rL * -theta
        DR = rR * -theta
        
        vR = 720
        vL = 720*(DL/DR)
        wait_time = (DR/wheel_perimeter)/(vR/360)
    
    rotation = theta_util*(math.pi/180) - theta
    
    print("theta_i : ", theta_i*180/math.pi)
    print("theta : ", theta*180/math.pi)
    print("rotation : ", rotation*180/math.pi)
    print("r : ", r)
    print("DL : ", DL)
    print("DR : ", DR)
    print("vL : ", vL)
    print("vR : ", vR)
    
    return vL, vR, wait_time, rotation
    
    
    
    


def send_command_to_motors(vL, vR, wait_time, rotation):
    dxl_io.set_moving_speed({2: vL}) # Degrees / s
    dxl_io.set_moving_speed({1: -vR}) # Degrees / s
    print(wait_time)
    time.sleep(wait_time)
    
    wait_rot = abs(rotation/math.pi)
    dxl_io.set_moving_speed({2: -360}) # Degrees / s180
    dxl_io.set_moving_speed({1: -360}) # Degrees / s
    time.sleep(wait_rot)
    
    dxl_io.set_moving_speed({2: 0}) # Degrees / s
    dxl_io.set_moving_speed({1: 0}) # Degrees / s
    
    


def main():
    while(1):
        x, y, theta = get_coordinate()
        vL, vR, wait_time, rotation = compute_motor_command(x, y, theta)
        send_command_to_motors(vL, vR, wait_time, rotation)


main()