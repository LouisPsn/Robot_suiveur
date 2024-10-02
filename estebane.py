import pypot.dynamixel


# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])

found_ids = dxl_io.scan()
ids = found_ids[:2]



# qzlrilibz
dxl_io.set_wheel_mode([1])
dxl_io.set_moving_speed({1: -360}) # Degrees / s
dxl_io.set_moving_speed({2: 360}) # Degrees / s

while True :
    print(dxl_io.get_present_position(1))
    print(dxl_io_get_present_state(2))
    time.sleep(1)

