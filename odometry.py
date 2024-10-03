import pypot.dynamixel
import math
import time

wheelDiameter = 5.2 # in cm
wheelDiameterSI = (wheelDiameter / 100)/2 # in m
wheelDistance = 14.5 # in cm
wheelDistanceSI = (wheelDistance/100)
frequency = 2.5 # in Hz

def init(motors:list):
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('No port')
    print(ports)

    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    dxl_io.disable_torque(motors)
    dxl_io.set_wheel_mode([1])
    return dxl_io

def wheelSpeedConvertion(leftWheel, RightWheel):
    leftWheelRad = leftWheel * (math.pi/180)
    rightWheelRad = RightWheel * (math.pi/180)
    linearSpeed = (wheelDiameter * (leftWheelRad+rightWheelRad))/4
    angularSpeed = ((wheelDiameter * (leftWheelRad-rightWheelRad))/wheelDistance)/2

    return linearSpeed, angularSpeed

def speedToDelta(linearSpeed, angularSpeed, time):
    if angularSpeed == 0: # TODO ajouter une tolerance
        x = linearSpeed*time*math.cos(worldTeta)
        y = linearSpeed*time*math.sin(worldTeta)
        return (x,y,0)
    else:
        teta = angularSpeed*time
        x = (linearSpeed*time)*(math.cos(worldTeta + angularSpeed*time))
        y = (linearSpeed*time)*(math.sin(worldTeta + angularSpeed*time))
        return(x,y,teta)



motorId = [1,2]

dxl = init(motorId)
worldX = 0
worldY = 0
worldTeta = 0

for i in range(0,1000):
    leftSpeed, rightSpeed = dxl.get_present_speed([1,2])
    leftSpeed = -leftSpeed
    v,teta = wheelSpeedConvertion(rightSpeed, leftSpeed)
    dx,dy,dteta = speedToDelta(v,teta,1/frequency)
    worldX += dx
    worldY += dy
    worldTeta += dteta
    print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))
    time.sleep(1/frequency)
