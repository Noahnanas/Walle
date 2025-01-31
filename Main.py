from Mvt_walle import Walle
import time
import keyboard

wal = Walle("/dev/ttyACM0")
time.sleep(2)

print("Contrôle de WALL-E via la console.")
print("Commandes disponibles :")
print("  - blink : fait cligner les yeux")
print("  - head [angle] : incline la tête (valeurs entre -1 et 1)")
print("  - sad [niveau] : ajuste la tristesse (0 à 1)")
print("  - quit : quitter le programme")
print("Appuie sur Échap pour quitter à tout moment.")
wal.auto_adjust()

while True:
    if keyboard.is_pressed("esc"):
        print("\nÉchap détecté. Fermeture du programme...")
        break

    cmd = input("\nCommande : ").strip().lower()
    

    if cmd == "blink":
        wal.blink()

    elif cmd.startswith("head "):
        try:
            angle = float(cmd.split()[1])
            wal.headAngle(angle)
        except (IndexError, ValueError):
            print("Usage : head [angle] (entre -1 et 1)")

    elif cmd.startswith("sad "):
        try:
            level = float(cmd.split()[1])
            wal.sadness(level)
        except (IndexError, ValueError):
            print("Usage : sad [niveau] (entre 0 et 1)")

    elif cmd == "quit":
        print("Fermeture du programme...")
        break

    else:
        print("Commande inconnue.")

wal.close()