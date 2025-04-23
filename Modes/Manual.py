import time

_active = False

def run(robot):
    global _active
    _active = True
    while _active:
        time.sleep(0.05)

def stop():
    global _active
    _active = False
