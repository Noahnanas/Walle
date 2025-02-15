import time
import cv2
import numpy as np
from flask import Flask, render_template, Response
from picamera2 import Picamera2

app = Flask(__name__)

# Initialisation de Picamera2
screen_width, screen_height = 640, 640
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (screen_width, screen_height)}
)
picam2.configure(preview_config)
picam2.start()

# Chargement du classificateur Haar pour la détection de visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def gen_frames():
    """Génère un flux d'images JPEG pour le streaming."""
    while True:
        # Capture d'une image depuis la caméra
        frame = picam2.capture_array()
        
        # Conversion de BGR vers RGB (selon la configuration, parfois nécessaire)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Conversion en niveaux de gris pour la détection des visages
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Détection des visages
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            # Dessiner un rectangle vert autour du visage détecté
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
        # Encodage de l'image en JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue  # Si l'encodage échoue, on passe à la frame suivante
        frame_bytes = buffer.tobytes()
        
        # Renvoie le frame dans le format multipart requis pour le streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.03)  # Petite pause pour limiter l'utilisation du CPU

@app.route('/')
def index():
    """Page d'accueil qui affiche le flux vidéo."""
    return render_template('indexwebcam.html')

@app.route('/video_feed')
def video_feed():
    """Route qui fournit le flux vidéo."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Le serveur Flask sera accessible sur toutes les interfaces au port 5000
    app.run(host='0.0.0.0', port=5000)
