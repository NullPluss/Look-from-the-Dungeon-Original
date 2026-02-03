import pygame
from ui.base_ui import BaseUI

class Panel(BaseUI):
    def __init__(self, rect, color=(30,30,30)):
        super().__init__(rect)
        self.color = color

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)