import pygame
import threading
import os

class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.lock = threading.Lock()

    def play(self, sound_name):
        file_path = os.path.join("Sounds/"+ sound_name + ".mp3")
        print(f"[SoundPlayer] Playing sound: {sound_name}")
        with self.lock:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

    def is_playing(self):
        return pygame.mixer.music.get_busy()
