import cv2 
import numpy as np 
import math
import pypot.dynamixel
import time


# Initialisation des moteurs
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])


# Récupère les consignes utilisateurs
def get_coordinate():
    print("Path method :")
    method = int(input())
    print("Enter x :")
    x = int(input())
    print("Enter y :")
    y = int(input())
    print("Enter theta :")
    theta = int(input())
    theta = theta

    return x, y, theta, method


# Calcule les commandes moteurs en fonction des consignes utilisateurs
def compute_motor_command_1(x, y, theta_util):
    wheel_perimeter = 161.16
    robot_width = 145
    v_rot = 180
    
    # Retourne le robot si la coordonnée en ordonnée est négative
    if (y < 0):
        time_sleep = ((robot_width/2)*math.pi)/(wheel_perimeter*(v_rot/360))
        dxl_io.set_wheel_mode([1])
        dxl_io.set_moving_speed({2: v_rot}) # Degrees / s
        dxl_io.set_moving_speed({1: v_rot}) # Degrees / s
        time.sleep(time_sleep)
        
        y = -y
        x = -x
        theta_util -= 180
    
    
    # Calcule des coordonnées du cercle suivi par le robot
    if y != 0:
        theta_i = math.atan(x/y)
    else:
        if x > 0:
            theta_i = math.pi/2
        else:
            theta_i = -math.pi/2
    distance = math.sqrt(x**2 + y**2)
    theta = math.pi - 2*(math.pi/2 - theta_i)
    r = (distance/2)/math.sin(theta/2)
    
    # Cas de rotation vers la gauche
    if x > 0:
        rL = r + robot_width/2
        rR = r - robot_width/2
        
        DL = rL * theta
        DR = rR * theta
        
        vL = 720
        vR = 720*(DR/DL)
        wait_time = (DL/wheel_perimeter)/(vL/360)
    # Cas de rotation vers la droite
    else:
        rL = -r - robot_width/2
        rR = -r + robot_width/2
        
        DL = rL * -theta
        DR = rR * -theta
        
        vR = 720
        vL = 720*(DL/DR)
        wait_time = (DR/wheel_perimeter)/(vR/360)
    
    # Calcul de la rotation final en fonction de la position du robot après translation et en fonction de la rotation utilisateur
    
    rotation = theta_util*(math.pi/180) - theta
    
    return vL, vR, wait_time, rotation
    
    
def compute_motor_command_2(x, y, theta_util):
    if (x != 0 or y != 0):
        wheel_perimeter = 161.16
        robot_width = 145
        v_rot = 180
        v_trans = 1080
        
        print("x : ", x)
        print("y : ", y)
        
        # Retourne le robot si la coordonnée en ordonnée est négative
        if (y < 0):
            time_sleep = ((robot_width/2)*math.pi)/(wheel_perimeter*(v_rot/360))
            dxl_io.set_wheel_mode([1])
            dxl_io.set_moving_speed({2: v_rot}) # Degrees / s
            dxl_io.set_moving_speed({1: v_rot}) # Degrees / s
            time.sleep(time_sleep)
            
            y = -y
            x = -x
            theta_util -= 180
        
        if y != 0:
            theta = math.atan(x/y)
        else:
            if x > 0:
                theta = math.pi/2
            else:
                theta = -math.pi/2

        print("theta : ", theta)

        if theta > 180:
            theta -= 360
        if theta < -180:
            theta += 360

        if theta < 0:
            sens = -1
        else:
            sens = 1
            
        # Rotation Initial du robot
        wait_rot = ((robot_width/2)*theta)/(wheel_perimeter*(v_rot/360))
        dxl_io.set_moving_speed({2: v_rot*sens}) # Degrees / s
        dxl_io.set_moving_speed({1: v_rot*sens}) # Degrees / s
        time.sleep(wait_rot)
        dxl_io.set_moving_speed({2: 0}) # Degrees / s
        dxl_io.set_moving_speed({1: 0}) # Degrees / s    
        
        
        # Calcul de la distance à parcourir
        distance = math.sqrt(x**2 + y**2)
        
        # Transalation du robot
        wait_trans = distance/(wheel_perimeter*(v_trans/360))
        dxl_io.set_moving_speed({2: v_trans}) # Degrees / s
        dxl_io.set_moving_speed({1: -v_trans}) # Degrees / s
        time.sleep(wait_trans)
        dxl_io.set_moving_speed({2: 0}) # Degrees / s
        dxl_io.set_moving_speed({1: 0}) # Degrees / s
        
        
        
        
        # Préparation de la rotation finale
        rotation = (theta_util*math.pi/180 - theta)*180/math.pi
        
        if rotation > 180:
            rotation -= 360
        if rotation < -180:
            rotation += 360
            
        if rotation < 0:
            sens = -1
        else:
            sens = 1
        
        print("rotation finale : ", rotation)
        
        rotation = rotation*math.pi/180
        
        # Rotation finale du robot
        wait_rot = ((robot_width/2)*rotation*sens)/(wheel_perimeter*(v_rot/360))
        print("wait rot", wait_rot)
        dxl_io.set_moving_speed({2: v_rot*sens}) # Degrees / s
        dxl_io.set_moving_speed({1: v_rot*sens}) # Degrees / s
        time.sleep(wait_rot)
        dxl_io.set_moving_speed({2: 0}) # Degrees / s
        dxl_io.set_moving_speed({1: 0}) # Degrees / s
        
def send_command_to_motors(vL, vR, wait_time, rotation):
    robot_width = 145
    wheel_perimeter = 161.16
    
    dxl_io.set_moving_speed({2: vL}) # Degrees / s
    dxl_io.set_moving_speed({1: -vR}) # Degrees / s
    time.sleep(wait_time)
    dxl_io.set_moving_speed({2: 0}) # Degrees / s
    dxl_io.set_moving_speed({1: 0}) # Degrees / s
    
    v_rot = 180
    
    while rotation > math.pi:
        rotation -= math.pi*2
    while rotation < -math.pi:
        rotation += math.pi*2
    
    if rotation < 0:
        sens = -1
    else:
        sens = 1
    
    wait_rot = ((robot_width/2)*rotation*sens)/(wheel_perimeter*(v_rot/360))
    dxl_io.set_moving_speed({2: v_rot*sens}) # Degrees / s
    dxl_io.set_moving_speed({1: v_rot*sens}) # Degrees / s
    time.sleep(wait_rot)
    dxl_io.set_moving_speed({2: 0}) # Degrees / s
    dxl_io.set_moving_speed({1: 0}) # Degrees / s
    
    
def main():
    while(1):
        x, y, theta_util, method = get_coordinate()
        
        if method == 1:
            vL, vR, wait_time, rotation = compute_motor_command_1(x, y, theta_util)
            send_command_to_motors(vL, vR, wait_time, rotation)
        elif method == 2:
            compute_motor_command_2(x, y, theta_util)


main()