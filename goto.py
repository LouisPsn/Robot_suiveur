# La position est toujours connue
# teta (θ) est l'angle
# meters and radians

import pypot.dynamixel
from time import sleep
motors_id = [1, 2]


def set_direction(dxl, motor, speed):
    dxl.set_moving_speed({motor: int(speed)}) # id_moteur : degrés/sec

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
    dxl_io.enable_torque(motors_id)
    dxl_io.set_wheel_mode([1])
    return dxl_io

def main():
    #dxl = init()
    while True:
        input_cmd = input("Entrer position (x, y, teta): ")
        print("Commande reçu : ", input_cmd)
        values = input_cmd.split(',')

        x = float(values[0].strip())
        y = float(values[1].strip())
        teta = float(values[2].strip())

        # Affichage des valeurs
        print(f"x = {x}, y = {y}, teta = {teta}")

        if input_cmd == "stop":
            stop_motors(dxl)
        if input_cmd == "t":
            test1(dxl, 10)
        else:
            speed = input_cmd
            set_all_motors(dxl, speed)


main()

