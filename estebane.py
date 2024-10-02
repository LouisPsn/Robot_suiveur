import pypot.dynamixel
import time


# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])




# qzlrilibz
dxl_io.set_wheel_mode([1])
dxl_io.set_moving_speed({1: -360}) # Degrees / s
dxl_io.set_moving_speed({2: 360}) # Degrees / s

while True :
    print(dxl_io.get_present_position((1, )))
    print(dxl_io.get_present_position((2, )))
    time.sleep(1)

