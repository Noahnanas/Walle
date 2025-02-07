#emotion_detection.py
import cv2
from deepface import DeepFace
import numpy as np  #this will be used later in the process

imgpath = "C:/Users/mouss/Pictures/Camera Roll/walle/emie_2.jpg"  #put the image where this file is located and put its name here
#image = cv2.imread(imgpath)

objs = DeepFace.analyze(
  imgpath,
  actions = ['age', 'gender', 'race', 'emotion'],
)
print(objs)

#DeepFace.stream(db_path = "C:/Users/mouss/Pictures/Camera Roll/walle")

"""
# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Analyse du visage avec DeepFace
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Récupérer l'émotion prédite
        dominant_emotion = analysis[0]['dominant_emotion']

        # Ajouter le texte sur l'image
        cv2.putText(frame, f"Émotion: {dominant_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        print("Erreur DeepFace :", e)

    # Affichage du flux vidéo
    cv2.imshow("DeepFace Emotion Recognition", frame)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la webcam et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
"""