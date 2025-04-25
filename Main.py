from Modes import Auto,Follow,Manual,Sequence,Sleep
from Web import server
from Mvt_walle import Walle
from Modes_manager import ModeManager
from Web.log_redirector import init_socketio, redirect_stdout
from Sounds.Test_son import SoundPlayer
import threading
import time

power=True

#server run
flask_thread = threading.Thread(target=server.run_web_server)
flask_thread.daemon = True
flask_thread.start()

robot = Walle("/dev/ttyACM0")
sound = SoundPlayer()
manager = ModeManager(robot,sound,server)

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
    selected = server.get_selected_mode()

    if selected != current_mode_name:
        print(f"[Main] Switching to mode: {selected}")
        current_mode_name = selected
        manager.stop_mode()
        if selected in modes:
            manager.launch_mode(modes[selected])
            
    
    time.sleep(0.03)
    

manager.stop_mode()
robot.neutral()
robot.close()

