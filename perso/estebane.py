import pypot.dynamixel
import matplotlib.pyplot as plt
import math
import time
import cv2 
import numpy as np 

# définition des constantes
wheelDiameter = 5.2 # in cm
wheelDiameterSI = (wheelDiameter / 100)/2 # in m
wheelDistance = 14.5 # in cm
wheelDistanceSI = (wheelDistance/100)
frequency = 2.5 # in Hz

motorId = [1,2]

# Initilisation des moteurs
def init(motors:list):
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('No port')
    print(ports)

    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    dxl_io.disable_torque(motors)
    dxl_io.set_wheel_mode([1])
    return dxl_io


dxl = init(motorId)
worldX = 0
worldY = 0
worldTeta = 0



Position=[]


# récupère la vitesse des moteurs et redonne les vitesses linéaires et angulaires robot
def wheelSpeedConvertion(leftWheel, RightWheel):
    leftWheelRad = leftWheel * (math.pi/180)        
    rightWheelRad = RightWheel * (math.pi/180)
    linearSpeed = (wheelDiameter * (leftWheelRad+rightWheelRad))/4
    angularSpeed = ((wheelDiameter * (leftWheelRad-rightWheelRad))/wheelDistance)/2

    return linearSpeed, angularSpeed

# calcul x, y et theta actuel
def speedToDelta(linearSpeed, angularSpeed, dt):
    '''
        if angularSpeed == 0: # TODO ajouter une tolerance
        x = linearSpeed*dt*math.cos(worldTeta)
        y = linearSpeed*dt*math.sin(worldTeta)
        return (x,y,0)
    else:

    '''
    teta = angularSpeed*dt
    x = (linearSpeed*dt)*(math.cos(worldTeta + angularSpeed*dt))
    y = (linearSpeed*dt)*(math.sin(worldTeta + angularSpeed*dt))
    return(x,y,teta)


'''
# Récupération des données et stockage dans Position
for i in range(0,100):
    leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
    leftSpeed = -leftSpeed
    v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
    dx,dy,dteta = speedToDelta(v,teta,1/frequency)
    worldX += dx
    worldY += dy
    worldTeta += dteta
    Position.append( (worldX, worldY) )
    print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))
    time.sleep(1/frequency)

# Création et sauvegarde du parcours
x, y = zip(*Position)

plt.plot(x, y, marker='o', linestyle='-', color='b')

plt.title('Parcours du robot')
plt.xlabel('Axe X')
plt.ylabel('Axe Y')
plt.grid()

plt.savefig('parcours.png')

leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
leftSpeed = -leftSpeed
v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
dx,dy,dteta = speedToDelta(v,teta,1/frequency)
worldX += dx
worldY += dy
worldTeta += dteta
print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))
'''

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
    wheel_perimeter = 162
    robot_width = 145
    
    # Retourne le robot si la coordonnée en ordonnée est négative
    if (y < 0):
        # dxl_io.set_wheel_mode([1])
        # dxl_io.set_moving_speed({2: 180}) # Degrees / s
        # dxl_io.set_moving_speed({1: 180}) # Degrees / s
        time.sleep(1)
        y = -y
        x = -x
        theta_util -= 180
    
    
    # Calcule des coordonnées du cercle suivi par le robot
    theta_i = math.atan(x/y)
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
        print("ici")
        rL = -r - robot_width/2
        rR = -r + robot_width/2
        
        DL = rL * -theta
        DR = rR * -theta
        
        vR = 720
        vL = 720*(DL/DR)
        wait_time = (DR/wheel_perimeter)/(vR/360)
    
    # Calcul de la rotation final en fonction de la position du robot après translation et en fonction de la rotation utilisateur
    rotation = theta_util*(math.pi/180) - theta
    
    print("theta_i : ", theta_i*180/math.pi)
    print("theta : ", theta*180/math.pi)
    print("rotation : ", rotation*180/math.pi)
    print("r : ", r)
    print("DL : ", DL)
    print("DR : ", DR)
    print("vL : ", vL)
    print("vR : ", vR)
    
    return vL, vR, wait_time, rotation
    
    
def compute_motor_command_2(x, y, theta_util):
    wheel_perimeter = 162
    theta = math.atan(x/y)
    
    # Retournement initial du robot si la coordonnées en ordonnée est négative
    if (y < 0):
            # dxl_io.set_wheel_mode([1])
            # dxl_io.set_moving_speed({2: 180}) # Degrees / s
            # dxl_io.set_moving_speed({1: 180}) # Degrees / s
            time.sleep(1)
            y = -y
            x = -x
            theta_util -= 180    
    
    
    # Calcul de la rotation initial du robot
    v_rot = 180
    rotation = theta*180/math.pi
    wait_rot = abs(rotation/v_rot)
    print("rotation : ", rotation)
    
    if rotation < 0:
        sens = -1
    else:
        sens = 1
    
    # Rotation du robot
    # dxl_io.set_moving_speed({2: v_rot*sens}) # Degrees / s180
    # dxl_io.set_moving_speed({1: v_rot*sens}) # Degrees / s
    # time.sleep(wait_rot)
    
    # Calcul de la translation du robot
    distance = math.sqrt(x**2 + y**2)
    v_moteur = 1080
    wait_time = distance/((wheel_perimeter/360)*v_moteur)
    
    print("distance : ", distance)
    
    # Translation du robot
    # dxl_io.set_moving_speed({2: v_moteur}) # Degrees / s
    # dxl_io.set_moving_speed({1: -v_moteur}) # Degrees / s
    # time.sleep(wait_time)
    
    # Calcul de la rotation du robot
    rotation = theta_util*(math.pi/180) - theta
    rotation = rotation*180/math.pi
    wait_rot = abs(rotation/v_rot)
    
    print("rotation : ", rotation)
    
    if rotation < 0:
        sens = -1
    else:
        sens = 1
    
    # Rotation finale du robot
    # dxl_io.set_moving_speed({2: v_rot*sens}) # Degrees / s180
    # dxl_io.set_moving_speed({1: v_rot*sens}) # Degrees / s
    # time.sleep(wait_rot)
    
    # dxl_io.set_moving_speed({2: 0}) # Degrees / s
    # dxl_io.set_moving_speed({1: 0}) # Degrees / s

def Print_position(debut, final):
    leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
    leftSpeed = -leftSpeed
    v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
    dx,dy,dteta = speedToDelta(v,teta,1/(final - debut))
    worldX += dx
    worldY += dy
    worldTeta += dteta
    print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))

    

def send_command_to_motors(vL, vR, wait_time, rotation):
    ########################################################
    debut_time = time.time()

    dxl_io.set_moving_speed({2: vL}) # Degrees / s
    dxl_io.set_moving_speed({1: -vR}) # Degrees / s
    time.sleep(wait_time)

    debut_time = time.time()

    Print_position()



    dxl_io.set_moving_speed({2: 0}) # Degrees / s
    dxl_io.set_moving_speed({1: 0}) # Degrees / s
    
    ########################################################
    v_rot = 180
    rotation = rotation*180/math.pi
    wait_rot = abs(rotation/v_rot)
    print("wait_rot : ", wait_rot)
    
    if rotation < 0:
        sens = -1
    else:
        sens = 1
    
    # dxl_io.set_moving_speed({2: v_rot*sens}) # Degrees / s180
    # dxl_io.set_moving_speed({1: v_rot*sens}) # Degrees / s
    # time.sleep(wait_rot)
    
    # dxl_io.set_moving_speed({2: 0}) # Degrees / s
    # dxl_io.set_moving_speed({1: 0}) # Degrees / s
    
def main():
    while(1):
        x, y, theta, method = get_coordinate()
        
        if method == 1:
            vL, vR, wait_time, rotation = compute_motor_command_1(x, y, theta)
            send_command_to_motors(vL, vR, wait_time, rotation)
        elif method == 2:
            compute_motor_command_2(x, y, theta)


main()