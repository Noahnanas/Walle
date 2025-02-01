import pygame

# Initialisation de pygame
pygame.mixer.init()

# Charger le fichier MP3
pygame.mixer.music.load("sound/voice_walle.mp3")

# Jouer le son  
pygame.mixer.music.play()

# Attendre la fin du son
while pygame.mixer.music.get_busy():
    continue
