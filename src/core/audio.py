import pygame
import os

class AudioManager:
    """
    Управляет всей музыкой и звуками.
    """

    def play_music(self, path):
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)