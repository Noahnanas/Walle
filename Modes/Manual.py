import time

active = False

def run(robot,sound,server):
    global active
    active = True
    while active:
        command = server.get_last_command()
        if command!= None:
            print(f"[Manual] Command received:{command}")
            match command:
                case "left":
                    robot.turn(-0.5)
                case "right":
                    robot.turn(0.5)
                case "forward":
                    print("[Manual] Moving forward")
                    robot.forward()
                case "backward":
                    robot.backward()
                case "stop":
                    pass
                case "blink":
                    robot.blink()
                
        emote = server.get_selected_emote()
            
        time.sleep(0.05)

def stop():
    global active
    active = False
