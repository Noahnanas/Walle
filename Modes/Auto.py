import time
from Vision.cam import get_head_factor

active = False

deadzone = 0.06
y_step = 0.05
x_factor = 0.5

def run(robot,server):
    global active
    active = True
    while active:
        head_factor=get_head_factor()
        if head_factor is not None:
            print(f"[Auto] Head factor: {head_factor}")
            
            """neck_angle = robot.get_coef("neck_angle")
            if (head_factor[1] < (0.5 - deadzone)) and (neck_angle!=0) :
                robot.neckAngle(round(neck_angle - y_step,2))
            elif (head_factor[1] > (0.5 + deadzone)) and (neck_angle!=1) :
                robot.neckAngle(round(neck_angle + y_step,2))
            """
            #neck_LR = robot.get_coef("neck_LR")
            robot.manual("neck_LR",round((head_factor[0] - 0.5) * x_factor + 0.5,2))
            print(f"[Auto] round {round((head_factor[0] - 0.5) * x_factor + 0.5,2)}")
                
            
            time.sleep(0.1) 

def stop():
    global active
    active = False