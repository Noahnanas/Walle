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
wal = Walle("COM6")
time.sleep(2)

print("\n🚀 Contrôle de WALL-E via la console.")
print("Commandes disponibles :")
print("  - blink               → Cligne des yeux")
print("  - head [angle]        → Incline la tête (-1 à 1)")
print("  - sad [niveau]        → Ajuste la tristesse (0 à 1)")
print("  - eyebrow [angle]     → Bouge les sourcils (0 à 1)")
print("  - manual [nom] [val]  → Modifie un paramètre spécifique")
print("  - auto                → Exécute une séquence animée")
print("  - neutral             → Remet WALL-E en position neutre")
print("  - quit                → Quitte le programme")
print("  - neckA [angle]       → Incline le cou (0 à 1)")
print("  - neckL [level]       → (0 à 1)")
print("  - neckLR [level]       → (0 à 1)")
print("\nAppuie sur 'q' ou 'quit' pour quitter.")

#wal.auto_adjust()  # Démarrage avec une animation automatique

while True:
    try:
        cmd = input("\nCommande : ").strip().lower()
    except EOFError:  
        break  # Gestion du Ctrl+D

    if cmd == "blink":
        wal.blink()

    elif cmd.startswith("head "):
        try:
            angle = float(cmd.split()[1])
            wal.headAngle(angle)
        except (IndexError, ValueError):
            print("❌ Usage : head [angle] (valeurs entre -1 et 1)")
            
    elif cmd.startswith("neckl "):
        try:
            angle = float(cmd.split()[1])
            wal.neckLevel(angle)
        except (IndexError, ValueError):
            print("❌ Usage : head [angle] (valeurs entre -1 et 1)")
            
    elif cmd.startswith("necka "):
        try:
            angle = float(cmd.split()[1])
            wal.neckAngle(angle)
        except (IndexError, ValueError):
            print("❌ Usage : head [angle] (valeurs entre -1 et 1)")
            
    elif cmd.startswith("necklr "):
        try:
            angle = float(cmd.split()[1])
            wal.neckLR(angle)
        except (IndexError, ValueError):
            print("❌ Usage : head [angle] (valeurs entre -1 et 1)")
            

    elif cmd.startswith("sad "):
        try:
            level = float(cmd.split()[1])
            wal.sadness(level)
        except (IndexError, ValueError):
            print("❌ Usage : sad [niveau] (valeurs entre 0 et 1)")

    elif cmd.startswith("eyebrow "):
        try:
            angle = float(cmd.split()[1])
            wal.eyebrow(angle)
        except (IndexError, ValueError):
            print("❌ Usage : eyebrow [angle] (valeurs entre 0 et 1)")

    elif cmd.startswith("manual "):
        try:
            parts = cmd.split()
            name = parts[1]
            value = float(parts[2])
            print(name[:-1]+name[-1].upper())
            wal.manual(name[:-1]+name[-1].upper(), value)
        except (IndexError, ValueError):
            print("❌ Usage : manual [nom] [valeur]")

    elif cmd == "auto":
        wal.auto_adjust()

    elif cmd == "neutral":
        wal.neutral()

    elif cmd in ["quit", "q"]:
        print("🔴 Fermeture du programme...")
        break

    else:
        print("❌ Commande inconnue.")