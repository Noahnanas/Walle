import time

active = False

def run(robot,sound):
    global active
    active = True
    while active:
        time.sleep(0.05)

def stop():
    global active
    active = False
