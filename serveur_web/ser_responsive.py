from flask import Flask, render_template, request
import os
from Mvt_walle import Walle  # On garde l'importation comme elle est

# Chemin absolu du dossier 'templates'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Chemin absolu du script
TEMPLATE_DIR = os.path.join(BASE_DIR, "serveur_web/templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

wal = Walle("/dev/ttyACM0")  # Connexion au port série de WALL-E

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servo', methods=['POST'])
def servo():
    servo_id = request.form['servo']  # Récupère le servomoteur sélectionné
    angle = request.form['angle']  # Récupère l'angle envoyé par le client

    print(f"Servo sélectionné : {servo_id}, Angle : {angle}°")  # Affichage côté serveur

    # Utilisation de Mvt_walle pour bouger le servomoteur
    wal.manual(servo_id, float(angle))  # Déplace le servomoteur en fonction de l'angle

    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
