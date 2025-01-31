import cv2

# Charger les classificateurs Haar pour la détection des visages et des sourires
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

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
    
    if not ret:
        print("Erreur : Impossible de capturer l'image.")
        break
    
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détection des visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    
    for (x, y, w, h) in faces:
        # Dessiner un rectangle autour du visage
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Sélectionner la région du visage pour la détection des sourires
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Détection des sourires dans la région du visage
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=25, minSize=(30, 30))
        
        for (sx, sy, sw, sh) in smiles:
            # Dessiner un rectangle autour du sourire
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)  # Rectangle vert autour du sourire
    
    # Afficher l'image avec les visages et sourires détectés
    cv2.imshow('Détection de sourires', frame)
    
    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
