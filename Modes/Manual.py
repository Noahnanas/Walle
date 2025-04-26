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
                    robot.forward()
                case "backward":
                    robot.backward()
                case "stop":
                    pass
                case "blink":
                    robot.blink()
                
        emote = server.get_selected_emote()
        if emote != None:
            print(f"[Manual] Emote received: {emote}")
            robot.emote(emote)
            
        servo, position = server.get_servo_data()
        if servo != None:
            print(f"[Manual] Servo {servo} to position {position}")
            robot.manual(servo,position/180)
            
        time.sleep(0.05)

def stop():
    global active
    active = False
