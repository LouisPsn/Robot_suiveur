import pypot.dynamixel
import matplotlib.pyplot as plt
import math
import time

# définition des constantes
wheelDiameter = 5.2 # in cm
wheelDiameterSI = (wheelDiameter / 100)/2 # in m
wheelDistance = 14.5 # in cm
wheelDistanceSI = (wheelDistance/100)
frequency = 2.5 # in Hz

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

motorId = [1,2]

dxl = init(motorId)
worldX = 0
worldY = 0
worldTeta = 0

Position=[]



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


# Récupèration la vitesse des moteurs et redonne les vitesses linéaires et angulaires robot
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
for i in range(0,25):
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

print(len(Position))

plt.plot(x, y, marker='o', linestyle='-', color='b')

plt.title('Parcours du robot')
plt.xlabel('Axe X')
plt.ylabel('Axe Y')
plt.grid()

plt.savefig('parcours.png')
'''


def main():

    consigne_x, consigne_y, consigne_theta, method = get_coordinate()

    Error_x = consigne_x-worldX

    while( abs(Error_x)<1 ):
        
        v_rot = Kx*Error_x
        if(v_rot>180):
            v_rot=180
        dxl_io.set_moving_speed({2: v_rot}) # Degrees / s
        dxl_io.set_moving_speed({1: -v_rot}) # Degrees / s

        leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
        leftSpeed = -leftSpeed
        v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
        dx,dy,dteta = speedToDelta(v,teta,1/frequency)
        worldX += dx
        worldY += dy
        worldTeta += dteta
        print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))

        time.sleep(1/frequency)

        
def main_1():

    consigne_x, consigne_y, consigne_theta, method = get_coordinate()

    Error_x = consigne_x-worldX
    Error_theta = consigne_theta - worldTeta

    while( abs(Error_theta)<1 ):

        sens=1
        if Error_theta < 0 :
            sens=-1

        v_rot = Kx*Error_x
        if(v_rot>180):
            v_rot=180
        dxl_io.set_moving_speed({2: sens*v_rot}) # Degrees / s
        dxl_io.set_moving_speed({1: sens*v_rot}) # Degrees / s

        leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
        leftSpeed = -leftSpeed
        v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
        dx,dy,dteta = speedToDelta(v,teta,1/frequency)
        worldX += dx
        worldY += dy
        worldTeta += dteta
        print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))

        time.sleep(1/frequency)

    while( abs(Error_x)<1 ):
        
        v_rot = Kx*Error_x
        if(v_rot>180):
            v_rot=180
        dxl_io.set_moving_speed({2: v_rot}) # Degrees / s
        dxl_io.set_moving_speed({1: -v_rot}) # Degrees / s

        leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
        leftSpeed = -leftSpeed
        v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
        dx,dy,dteta = speedToDelta(v,teta,1/frequency)
        worldX += dx
        worldY += dy
        worldTeta += dteta
        print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))

        time.sleep(1/frequency)


main()
