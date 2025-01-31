import random
import time
from Mvt_walle import Walle

wal = Walle("/dev/ttyACM0")
time.sleep(2)

values = [0, 0.5, 1]  # Valeurs possibles pour les angles

while True:
    action = random.choices(
        ["blink", "head", "sad", "eyebrow", "auto"],
        weights=[0.3, 0.15, 0.2, 0.25, 0.1]
    )[0]

    if action == "blink":
        wal.blink()

    elif action == "head":
        angle = random.choice([-1, -0.5, 0, 0.5, 1])  # Valeurs fixes pour l'inclinaison de la tête
        wal.headAngle(angle)

    elif action == "sad":
        level = random.choice(values)  # Prend une valeur dans [0, 0.5, 1]
        wal.sadness(level)

    elif action == "eyebrow":
        angle = random.choice(values)  # Même logique pour les sourcils
        wal.eyebrow(angle)

    elif action == "auto":
        wal.auto_adjust()

    time.sleep(random.uniform(1, 3))  # Pause entre les actions (aléatoire entre 1 et 3 sec)
