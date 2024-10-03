import pypot.dynamixel

def initMotor() -> pypot.dynamixel.DxlIO: 
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('No port')
    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    return dxl_io

def setup_motors(dxl_io:pypot.dynamixel.DxlIO) -> None:
    dxl_io.set_wheel_mode([1, 2])

def command_motors(vL:int, vR:int, dxl_io:pypot.dynamixel.DxlIO) -> None:
    dxl_io.set_moving_speed({1: -vL, 2: vR})

def stop_motor(dxl_io:pypot.dynamixel.DxlIO):
    command_motors(0,0,dxl_io)
