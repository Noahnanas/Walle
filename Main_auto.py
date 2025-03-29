import cv2
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Erreur : Impossible d'ouvrir la caméra.")
    exit()

pTime = 0
while True:
    success, img = cap.read()
    if not success:
        print("❌ Erreur : Impossible de lire l'image de la caméra.")
        break  # Sort de la boucle si la capture échoue

    # Affichage FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime - pTime > 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Test", img)

    # Quitter proprement avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
