import cv2

# Charger le classificateur Haar pour la détection des visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialiser la webcam (0 pour la webcam par défaut)
cap = cv2.VideoCapture(0)

# Vérifier si la webcam s'ouvre correctement
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la webcam.")
    exit()

# Boucle de capture vidéo
while True:
    # Capture image par image
    ret, frame = cap.read()
    
    # Vérifier si l'image a été capturée correctement
    if not ret:
        print("Erreur : Impossible de capturer l'image.")
        break
    
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détection des visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Dessiner un rectangle autour de chaque visage détecté
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Rectangle bleu autour du visage
    
    # Afficher l'image avec les visages détectés
    cv2.imshow('Détection de visages', frame)
    
    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
