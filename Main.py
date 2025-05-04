from Modes import Auto,Follow,Manual,Sequence,Sleep
from Web import server
from Services.Mvt_walle import Walle
from Services.Modes_manager import ModeManager
from Web.log_redirector import init_socketio, redirect_stdout
import RPi.GPIO as GPIO

import threading
import time
import os

power=True

# Definition des pins
GPIO.setmode(GPIO.BCM)

pinBtn_R = 2
pinBtn_C = 3
pinBtn_T = 4
pinBtn_S = 17

GPIO.setup(pinBtn_R, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(pinBtn_C, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(pinBtn_T, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(pinBtn_S, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


#server run
flask_thread = threading.Thread(target=server.run_web_server)
flask_thread.daemon = True
flask_thread.start()

robot = Walle("/dev/ttyACM0")
manager = ModeManager(robot,server)

#log redirection
init_socketio(server.socketio)
redirect_stdout()

# modes
modes = {
    "Auto": Auto,
    "Follow": Follow,
    "Manual": Manual,
    "Sequence": Sequence,
    "Sleep": Sleep
}

current_mode_name = None

while power:
    etat_R = GPIO.input(pinBtn_R)
    etat_C = GPIO.input(pinBtn_C)
    etat_T = GPIO.input(pinBtn_T)
    etat_S = GPIO.input(pinBtn_S)
    selected = server.get_selected_mode()

    if selected != current_mode_name:
        print(f"[Main] Switching to mode: {selected}")
        current_mode_name = selected
        manager.stop_mode()
        if selected in modes:
            manager.launch_mode(modes[selected])
            
    if server.get_shudown():
        print("[Main] Shutdown command received.")
        power = False
            
    
    time.sleep(0.03)
    

manager.stop_mode()
#robot.sleep()
robot.close()

#os.system("sudo shutdown -h now")
