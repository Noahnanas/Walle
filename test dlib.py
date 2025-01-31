import cv2
import dlib
import numpy as np
from imutils import face_utils

# Charger le détecteur de visage dlib et le prédicteur de points de repère faciaux
detector = dlib.get_frontal_face_detector()
predictor_path = r"G:/.shortcut-targets-by-id/1kIymp6LMtwX3kk3tlaloCrtWfamhfD6l/Projet WALL-E/Walle/shape_predictor_68_face_landmarks.dat"  # Remplace par le chemin réel
predictor = dlib.shape_predictor(predictor_path)

# Ouvrir la webcam
video_path = r"C:/Users/joker/Pictures/Camera Roll/testRec.mp4"  # Chemin de la vidéo
#cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détecter les visages
    faces = detector(gray)
    
    for face in faces:
        # Obtenir les landmarks du visage
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)  # Convertir en tableau numpy
        
        # Dessiner tous les points de repère
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 2, (255, 0, 255), -1)  # Cercle magenta pour tous les points

        # Calcul de la hauteur des sourcils
        # Points de sourcil gauche (17 à 21)
        brow_left = shape[17:22]  # Points du sourcil gauche
        # Points de sourcil droit (22 à 26)
        brow_right = shape[22:27]  # Points du sourcil droit
        
        # Trouver les points les plus hauts des sourcils
        brow_left_top = min(brow_left, key=lambda p: p[1])  # Point le plus haut du sourcil gauche
        brow_right_top = min(brow_right, key=lambda p: p[1])  # Point le plus haut du sourcil droit
        
        # Calculer la hauteur des sourcils (différence de la coordonnée Y)
        brow_height = abs(brow_left_top[1] - brow_right_top[1])

        # Afficher la hauteur des sourcils
        cv2.putText(frame, f"Hauteur des sourcils: {brow_height}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Afficher le résultat
    cv2.imshow("Points du visage et hauteur des sourcils", frame)
    
    # Sortir de la boucle avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
