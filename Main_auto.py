from Mvt_walle import Walle
import time
import random

wal = Walle("/dev/ttyACM0")
time.sleep(2)

print("Contrôle de WALL-E via la console.")
print("Mouvements aléatoires en cours...")
print("Appuie sur Ctrl+C pour arrêter le programme.")

wal.auto_adjust()

actions = ["blink", "head", "sad", "eyebrow", "auto"]

try:
    while True:
        action = random.choice(actions)
        if action == "blink":
            wal.blink()
        elif action == "head":
            angle = random.choice([-1.0,-0.5,0.0, 0.5, 1.0])
            wal.headAngle(angle)
        elif action == "sad":
            level = random.choice([0.0, 0.5, 1.0])
            wal.sadness(level)
        elif action == "eyebrow":
            angle = random.choice([0.0, 0.5, 1.0])
            wal.eyebrow(angle)
        elif action == "auto":
            wal.auto_adjust()

        time.sleep(random.uniform(1, 3))
except KeyboardInterrupt:
    print("\nProgramme arrêté par l'utilisateur avec Ctrl+C.")
    wal.neutral()
    wal.close()
