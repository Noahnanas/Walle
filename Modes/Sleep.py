import time

active = False

def run(robot,server):
    global active
    active = True
    
    while active:
        robot.sleep()
        time.sleep(0.05)

def stop():
    global active
    active = False