import pypot.dynamixel
import time
import numpy as np



# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])

current_position_1=(0,0)
current_position_2=(0,0)

past_position_1=0
past_position_2=0

# distance en centimetre
empatement = 14.5
perimetre_empatement = (empatement/2)*2*3.1415

diametre_roue = 5.2
rayon_roue = diametre_roue/2
perimetre_roue = rayon_roue*2*3.1415



# qzlrilibz
dxl_io.set_wheel_mode([2])
#dxl_io.set_moving_speed({1: -360}) # Degrees / s
#dxl_io.set_moving_speed({2: 360}) # Degrees / s

while True :
    past_position_1 = current_position_1
    past_position_2 = current_position_2

    # en degree
    current_position_1=dxl_io.get_present_position((1, ))
    current_position_2 =dxl_io.get_present_position((2, ))

    print(current_position_1)
    print(current_position_2)

    #posera probleme par la suite
    delta_angle_1 = current_position_1[0] - past_position_1[0]
    delta_angle_2 = current_position_2[0] - past_position_2[0]

    delta_position_1 = perimetre_roue*(delta_angle_1/360)
    delta_position_2 = perimetre_roue*(delta_angle_2/360)

    angle = np.degrees(np.arcsin( ( delta_position_1 - delta_position_2)/rayon_roue ))
    #PositionX = (delta_1 + delta_2)*np.cos(angle)
    #PositionY = (delta_1 + delta_2)*np.sin(angle)

    print(angle)
    #print(PositionX)
    #print(PositionY)

    time.sleep(1)

