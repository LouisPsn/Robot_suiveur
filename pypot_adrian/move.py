import pypot.dynamixel
from time import sleep

# found_ids = dxl_io.scan()
# print('Found ids:', found_ids)

# ids = found_ids[:2]
# print(ids)

#set_moving_speed({idmoteur : angle de rotation})
motors_id = [1, 2]


def set_direction(dxl, motor, speed):
    dxl.set_moving_speed({motor: int(speed)}) # id_moteur : degrés/sec

def set_all_motors(dxl, speed):
    for motor in motors_id:
        speed_cmd = speed
        print(motor)
        if motor == 1 and speed_cmd != 0: # Motor 1 inversé
            speed_cmd = - (speed_cmd)
            print(speed_cmd)
        dxl.set_moving_speed({motor : speed_cmd})

def test1(dxl, speed):
    set_all_motors(dxl, speed)
    sleep(2)
    set_all_motors(dxl, 0)
    sleep(2)
    set_all_motors(dxl, -(speed))


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
    dxl = init()
    # dxl.set_moving_speed({1 : - 100})
    # dxl.set_moving_speed({2 : 100})
    # sleep(5)
    # dxl.set_moving_speed({1 : 0})
    # dxl.set_moving_speed({2 : 0})
    while True:
        input_cmd = input("Définir vitesse (Unité : degrés/seconde): ")
        print("Commande reçu : ", input_cmd)

        if input_cmd == "stop":
            stop_motors(dxl)
        if input_cmd == "t":
            test1(dxl, 10)
        else:
            speed = int(input_cmd)
            set_all_motors(dxl, speed)


main()

