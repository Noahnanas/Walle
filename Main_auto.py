import time
import random
from Mvt_walle import Walle

# Initialisation de WALL-E
wal = Walle("/dev/ttyACM0")
time.sleep(2)

print("WALL-E commence ses mouvements aléatoires...")

# Boucle infinie avec mouvements aléatoires
try:
    while True:
        action = random.choice(["blink", "head", "sad", "eyebrow", "auto"])

        if action == "blink":
            wal.blink()
            print("WALL-E cligne des yeux.")

        elif action == "head":
            angle = random.uniform(-1, 1)
            wal.headAngle(angle)
            print(f"WALL-E incline la tête à {angle:.2f}.")

        elif action == "sad":
            level = random.uniform(0, 1)
            wal.sadness(level)
            print(f"WALL-E ajuste sa tristesse à {level:.2f}.")

        elif action == "eyebrow":
            angle = random.uniform(0, 1)
            wal.eyebrow(angle)
            print(f"WALL-E bouge ses sourcils à {angle:.2f}.")

        elif action == "auto":
            wal.auto_adjust()
            print("WALL-E exécute une suite de mouvements prédéfinie.")
            time.sleep(10)

        time.sleep(random.uniform(1, 3))  # Pause aléatoire entre les mouvements

except KeyboardInterrupt:
    print("\nArrêt du programme.")
    wal.close()