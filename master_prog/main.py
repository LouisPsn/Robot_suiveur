import motor, line_following, robot_constant, opencv_utils

def main():
    print("Line followin robot - Group 4")
    print("[Status]: Init...")
    dxl = motor.initMotor()
    cammera = opencv_utils.initVideoCapture(robot_constant.CAMMERA_PORT)
    lineFollowingSavedPos = False
    status:int = 0 # 0 -> ligne noir, 1 -> ligne rouge, 2 -> stop
    odometry = False
    lastSwitch = 0

    print("[Status]: Main loop")
    while(True):
        match status:
            case 0:
                line_following.blackLineFolow(cammera, dxl)
            case 1:
                line_following.redLineFolow(cammera, lineFollowingSavedPos, dxl)
            case 2:
                motor.stop_motor(dxl)
                break
        
        #Odometry section
        if (odometry):
            # odotick
            pass
        
        #Status update section
        if(lastSwitch > 100 and line_following.yellow_detected(cammera)):
            status += 1
            lastSwitch = 0
            print("[Status]: Status + 1")
        else:
            lastSwitch += 1
    
    print("[Status]: Deinit")
    cammera.release()
    print("[Status]: Good bye!")

    
main()    


