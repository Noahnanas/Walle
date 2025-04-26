import time

active = False

def run(robot,sound,server):
    global active
    active = True
    while active:
        command = server.get_last_command()
        if command!= None:
            command = server.get_last_command()
            if command == "left":
                robot.turn(-0.5)
            elif command == "right":
                robot.turn(0.5)
            elif command == "forward":
                robot.forward()
            elif command == "backward":
                robot.backward()
            elif command == "stop":
                pass
            elif command == "blink":
                robot.blink()
                
        emote = server.get_selected_emote()
            
        time.sleep(0.05)

def stop():
    global active
    active = False
