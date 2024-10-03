# La position est toujours connue
# teta (θ) est l'angle
# meters and radians

# Connu : x, y, theta de départ
#         x, y, theta d'arrivée

# Ecart entre 2 roues : 14,5 cm

import pypot.dynamixel
import math
from time import sleep
motors_id = [1, 2]

import math

def getActuAngle(dxl, wheel_radius, wheel_distance):
    left_motorposition = dxl.get_present_position([1])[0]
    right_motorposition = dxl.get_present_position([2])[0]
    
    left_motorposition_rad = math.radians(left_motorposition)
    right_motorposition_rad = math.radians(right_motorposition)
    
    left_distance = left_motorposition_rad * wheel_radius
    right_distance = right_motorposition_rad * wheel_radius
    
    delta_distance = right_distance - left_distance
    
    theta_current = delta_distance / wheel_distance

    return theta_current


def convertToRadiansToCoor(currentPosition):
    # Diamètre roue : 5,2 cm
    rayon = 0.026 # 2,6 cm 
    current_position_radians = [math.radians(pos) for pos in currentPosition]

    x1 = rayon * math.cos(current_position_radians[0])
    y1 = rayon * math.sin(current_position_radians[0])

    x2 = rayon * math.cos(current_position_radians[1])
    y2 = rayon * math.sin(current_position_radians[1])

    print(f"Motor 1 - Position en degrés: {currentPosition[0]}, en radians: {current_position_radians[0]}")
    print(f"Coordonnées x, y pour le moteur 1: ({x1}, {y1})")

    print(f"Motor 2 - Position en degrés: {currentPosition[1]}, en radians: {current_position_radians[1]}")
    print(f"Coordonnées x, y pour le moteur 2: ({x2}, {y2})")
    return x1, y1, x2, y2

def set_direction(dxl, motor, speed):
    dxl.set_moving_speed({motor: int(speed)}) # id_moteur : degrés/sec

def turnToLeft(dxl, speed):
    dxl.set_moving_speed({1 : 0, 2: int(speed)})

def turnToRight(dxl, speed):
    dxl.set_moving_speed({1 : - int(speed), 2 : 0}) # Moteur 1 inversé

def set_all_motors(dxl, speed):
    for motor in motors_id:
        speed_cmd = speed
        print(motor)
        if motor == 1 and speed_cmd != 0: # Motor 1 inversé
            speed_cmd = - (int(speed_cmd))
            print(speed_cmd)
        set_direction(dxl, motor, speed_cmd)

def stop_motor(dxl, motor_id):
    dxl.set_moving_speed({motor_id : 0})

def stop_motors(dxl):
    for motor in motors_id:
        print("Arret moteur n° ", motor)
        dxl.set_moving_speed({motor : 0})

def init():
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('No port')
    print(ports)

    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    #dxl_io.enable_torque(motors_id)
    #dxl_io.set_wheel_mode([1])

    # Définir position initiale à 0
#    for motor in motors_id:
#        dxl_io.set_goal_position(motor, 0)
    return dxl_io

def main():
    dxl = init()
    current_position = dxl.get_present_position([1, 2])
    print(f"Position actuelle du moteur 1 (en degrés): {current_position[0]}")
    print(f"Position actuelle du moteur 2 (en degrés): {current_position[1]}")
    #convertToRadiansToCoor(current_position)
    while True :
        getActuAngle(dxl, 0.026, 0.145)


    # while True:
    #     input_cmd = input("Entrer position (x, y, teta): ")
    #     print("Commande reçu : ", input_cmd)
    #     values = input_cmd.split(',')

    #     x = float(values[0].strip())
    #     y = float(values[1].strip())
    #     teta = float(values[2].strip())

    #     # Affichage des valeurs
    #     print(f"x = {x}, y = {y}, teta = {teta}")

    #     if input_cmd == "stop":
    #         stop_motors(dxl)
    #     if input_cmd == "t":
    #         test1(dxl, 10)
    #     else:
    #         speed = input_cmd
    #         set_all_motors(dxl, speed)


main()

