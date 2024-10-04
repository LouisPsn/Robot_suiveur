import motor, line_following, robot_constant, opencv_utils, time, odometry, math

def main():
    print("Line followin robot - Group 4")
    print("[Status]: Init...")
    dxl = motor.initMotor()
    cammera = opencv_utils.initVideoCapture(robot_constant.CAMMERA_PORT)
    lineFollowingSavedPos = False
    status:int = 0 # 0 -> ligne noir, 1 -> ligne rouge, 2 -> stop
    odometryStatus = True
    lastSwitch = 0
    lastOdoTickTime = time.time()
    odoTick = 0
    odoTickRate = 5
    positionList = [(0,0)]
    worldX = 0
    worldY = 0
    worldTeta = 0
    bench = True
    t1, t2 = None
    fps_mean = -1

    print("[Status]: Main loop")
    while(True):
        if bench:
            t1 = time.time()

        match status:
            case 0:
                lineFollowingSavedPos = line_following.blackLineFolow(cammera, lineFollowingSavedPos, dxl)
            case 1:
                lineFollowingSavedPos = line_following.redLineFolow(cammera, lineFollowingSavedPos, dxl)
            case 2:
                motor.stop_motor(dxl)
                break

        if bench:
            t2 = time.time()
            img_time = t2-t1
            if(fps_mean == -1):
                fps_mean = img_time
            else:
                fps_mean = (fps_mean + img_time) / 2
        
        #Odometry section
        if (odometryStatus and odoTick > odoTickRate):
            actualTime = time.time()
            dt = actualTime - lastOdoTickTime
            dx, dy, dteta = odometry.odometryTick(positionList, worldX, worldY, worldTeta, dt, dxl)
            worldX += dx
            worldY += dy
            worldTeta += dteta
            print("{}, {}, {}".format(worldX,worldY,worldTeta/(math.pi/180)))
            lastOdoTickTime = actualTime
            odoTick = 0
            if bench:
                print("mean fps on last {} frames: {}".format(odoTickRate, 1/fps_mean))
        else:
            odoTick += 1
        
        #Status update section
        if(lastSwitch > 100 and line_following.yellow_detected(cammera)):
            status += 1
            lastSwitch = 0
            lineFollowingSavedPos = False
            print("[Status]: Status + 1")
            
            # reset odometry
            odometry.saveImage(positionList, "map-{}.png".format(status))
            worldX = 0
            worldY = 0
            worldTeta = 0
            positionList = [(0,0)]
        else:
            lastSwitch += 1
    print("[Status]: Generatin map")
    
    print("[Status]: Deinit")
    cammera.release()
    print("[Status]: Good bye!")

    
main()    


