from Modes import Auto,Follow,Manual,Sequence,Sleep
from Web import serveur
from Mvt_walle import Walle
from Modes_manager import ModeManager
import threading
import time

robot = Walle("/dev/ttyACM0")
manager = ModeManager(robot)

manager.launch_mode(Manual)

flask_thread = threading.Thread(target=serveur.run_web_server, args=(manager,))
flask_thread.daemon = True
flask_thread.start()


time.sleep(30)
    

manager.stop_mode()
robot.neutral()
robot.close()

