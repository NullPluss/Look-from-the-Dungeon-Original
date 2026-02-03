import pygame
from ui.base_ui import BaseUI

class Slot(BaseUI):
    def __init__(self, rect):
        super().__init__(rect)
        self.item = None

    def set_item(self, item):
        self.item = item

    def render(self, screen):
        pygame.draw.rect(screen, (100,100,100), self.rect, 2)
        if self.item and hasattr(self.item, 'icon'):
            screen.blit(self.item.icon, self.rect.topleft)