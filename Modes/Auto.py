import time
from Vision.cam import frame_process
active = False

def run(robot,server):
    global active
    active = True
    while active:
        head_factor=frame_process()
        if head_factor is not None:
            print(f"[Auto] Head factor: {head_factor}")
        #time.sleep(0.5)

def stop():
    global active
    active = False