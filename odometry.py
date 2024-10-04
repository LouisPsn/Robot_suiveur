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
#x, y = zip(*Position)

x_values = [t[0] for t in Position]  # Première valeur de chaque tuple
y_values = [t[1] for t in Position]

print(len(Position))

plt.plot(x_values, y_values, marker='o')  # 'o' pour marquer les points
plt.title('Graphique des tuples')
plt.xlabel('Axe X')
plt.ylabel('Axe Y')
plt.grid()
plt.show()

plt.savefig('parcours.png')

#plt.plot(x, y, marker='o', linestyle='-', color='b')

#plt.title('Parcours du robot')
#plt.xlabel('Axe X')
#plt.ylabel('Axe Y')
#plt.grid()

p#lt.savefig('parcours.png')