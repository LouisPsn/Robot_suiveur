import pypot.dynamixel


# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io_L = pypot.dynamixel.DxlIO(ports[0])
# dxl_io_R = pypot.dynamixel.DxlIO(ports[1])


dxl_io_L.set_wheel_mode([1])
# dxl_io_R.set_wheel_mode([1])
dxl_io_L.set_moving_speed({1: 360}) # Degrees / s
# dxl_io_R.set_moving_speed({1: 360}) # Degrees / s

