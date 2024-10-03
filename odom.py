import pypot.dynamixel
import time
import numpy as np

# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])

dxl_io.set_wheel_mode([2])

############################################
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

angle_robot=0

angletotal_roue_1 = 0
angletotal_roue_2 = 0

############################################

def direct_kinematics(vgauche, vdroite):

    linear_speed = (vgauche+vdroite)/2
    angular_speed = 

    return linear_speed, angular_speed 
