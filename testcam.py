import time
import pygame
import numpy as np
import cv2
from picamera2 import Picamera2

# Initialisation de Pygame
pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Détection de Visages avec Picamera2")

# Initialisation de Picamera2
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (screen_width, screen_height)})
picam2.configure(preview_config)
picam2.start()

# Charger le classificateur de détection de visages OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

running = True
while running:
    # Capture d'une image depuis la caméra
    frame = picam2.capture_array()

    # Conversion de la couleur BGR (par défaut) en RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Conversion en niveaux de gris pour OpenCV (plus rapide pour la détection)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Détection des visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    # Dessiner des rectangles autour des visages détectés
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Création d'une surface Pygame à partir du tableau NumPy
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame))

    # Affichage de l'image avec les visages encadrés
    screen.blit(frame_surface, (0, 0))
    pygame.display.flip()

    # Gestion des événements Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time.sleep(0.03)  # Pause pour éviter une utilisation CPU excessive

picam2.stop()
pygame.quit()
