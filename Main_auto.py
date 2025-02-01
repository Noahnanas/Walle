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
        action = random.choices(["blink", "head", "sad", "eyebrow", "auto"],weights=[0.5, 0.1, 0.1, 0.15, 0.1])[0]

        if action == "blink":
            wal.blink()
            print("WALL-E cligne des yeux.")

        elif action == "head":
            angle = random.choice([-1.0,-0.5,0.0, 0.5, 1.0])
            wal.headAngle(angle)
            print(f"WALL-E incline la tête à {angle:.2f}.")

        elif action == "sad":
            level = random.choice([0.0, 0.5, 1.0])
            wal.sadness(level)
            print(f"WALL-E ajuste sa tristesse à {level:.2f}.")

        elif action == "eyebrow":
            angle = random.choice([0.0, 0.5, 1.0])
            wal.eyebrow(angle)
            print(f"WALL-E bouge ses sourcils à {angle:.2f}.")

        elif action == "auto":
            wal.auto_adjust()
            print("WALL-E exécute une suite de mouvements prédéfinie.")

        time.sleep(random.uniform(4, 15))  # Pause aléatoire entre les mouvements

except KeyboardInterrupt:
    print("\nArrêt du programme.")
    wal.neutral()
    wal.close()