import math
from robot_constant import *
import matplotlib.pyplot as plt


# récupère la vitesse des moteurs et redonne les vitesses linéaires et angulaires robot
def wheelSpeedConvertion(leftWheel, RightWheel):
    leftWheelRad = leftWheel * (math.pi/180)        
    rightWheelRad = RightWheel * (math.pi/180)
    linearSpeed = (wheelDiameter * (leftWheelRad+rightWheelRad))/4
    angularSpeed = ((wheelDiameter * (leftWheelRad-rightWheelRad))/wheelDistance)/2

    return linearSpeed, angularSpeed

# calcul x, y et theta actuel
def speedToDelta(linearSpeed, angularSpeed, dt, worldTeta):
    teta = angularSpeed*dt
    x = (linearSpeed*dt)*(math.cos(worldTeta + angularSpeed*dt))
    y = (linearSpeed*dt)*(math.sin(worldTeta + angularSpeed*dt))
    return(x,y,teta)

def odometryTick(Position, worldX, worldY, worldTeta, deltaT, dxl):

    leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
    leftSpeed = -leftSpeed
    v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
    dx,dy,dteta = speedToDelta(v,teta,deltaT)
    
    worldX += dx
    worldY += dy
    worldTeta += dteta

    Position.append((worldX, worldY))
    print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))

def saveImage(Position, filename):
    x, y = zip(*Position)

    print(len(Position))

    plt.plot(x, y, marker='o', linestyle='-', color='b')

    plt.title('Parcours du robot')
    plt.xlabel('Axe X')
    plt.ylabel('Axe Y')
    plt.grid()

    plt.savefig(filename)