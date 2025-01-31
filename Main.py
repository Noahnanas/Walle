import time
import threading
import sys
from Mvt_walle import Walle

stop_flag = False  # Variable globale pour stopper le programme

def watch_escape():
    """Thread qui surveille si l'utilisateur appuie sur Échap."""
    global stop_flag
    try:
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)  # Mode non bloquant pour stdin
        while not stop_flag:
            key = sys.stdin.read(1)  # Lecture d'un seul caractère
            if key == '\x1b':  # Code ASCII de Échap
                print("\nÉchap détecté. Fermeture du programme...")
                stop_flag = True
                break
    except Exception as e:
        print(f"Erreur dans la détection de la touche : {e}")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Lancer le thread de détection de la touche Échap
threading.Thread(target=watch_escape, daemon=True).start()

# Initialisation de WALL-E
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

while not stop_flag:
    try:
        cmd = input("\nCommande : ").strip().lower()
    except EOFError:  # Gestion du Ctrl+D pour quitter proprement
        break

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

stop_flag = True  # Assure l'arrêt du thread
wal.close()
