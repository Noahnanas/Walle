from Modes import Auto,Follow,Manual,Sequence,Sleep
from Web import server
from Mvt_walle import Walle
from Modes_manager import ModeManager
import threading
import time

robot = Walle("/dev/ttyACM0")
manager = ModeManager(robot)

manager.launch_mode(Manual)

flask_thread = threading.Thread(target=server.run_web_server)
flask_thread.daemon = True
flask_thread.start()

# Dictionnaire des modes disponibles
modes = {
    "Auto": Auto,
    "Follow": Follow,
    "Manual": Manual,
    "Sequence": Sequence,
    "Sleep": Sleep
}
current_mode_name = None

for i in range(0,60):
    selected = server.get_selected_mode()

    if selected != current_mode_name:
        print(f"Switching to mode: {selected}")
        current_mode_name = selected
        manager.stop_mode()
        if selected in modes:
            manager.launch_mode(modes[selected])
    time.sleep(1)
    

manager.stop_mode()
robot.neutral()
robot.close()

