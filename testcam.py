import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if ret:
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
else:
    print("Erreur : Impossible de capturer l'image.")
