import pygame
import utils.constants as constants

class Window:
    """
    Управляет окном, fullscreen и масштабированием.
    """

    def __init__(self):
        self.fullscreen = True
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.update_scale()

    def update_scale(self):
        self.real_w, self.real_h = self.screen.get_size()
        self.scale_x = self.real_w / constants.BASE_W
        self.scale_y = self.real_h / constants.BASE_H

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (constants.BASE_W, constants.BASE_H)
            )
        self.update_scale()

    def sx(self, x): return int(x * self.scale_x)
    def sy(self, y): return int(y * self.scale_y)