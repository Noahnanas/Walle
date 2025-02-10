import cv2

# Ouvre la webcam (0 pour la webcam par défaut)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Capture une image
    if not ret:
        break

    cv2.imshow("Flux Webcam", frame)  # Affiche l'image dans une fenêtre

    # Quitte avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libère la webcam et ferme les fenêtres
cap.release()
cv2.destroyAllWindows()
