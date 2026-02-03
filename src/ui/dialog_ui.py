import pygame
from ui.base_ui import BaseUI

class DialogUI(BaseUI):
    def __init__(self, rect, font=None):
        super().__init__(rect)
        self.text = ""
        self.font = font or pygame.font.SysFont("arial", 18)

    def set_text(self, text):
        self.text = text

    def render(self, screen):
        pygame.draw.rect(screen, (20,20,20), self.rect)
        lines = self.text.split("\n")
        y = self.rect.y + 10
        for line in lines:
            surf = self.font.render(line, True, (255,255,255))
            screen.blit(surf, (self.rect.x+10, y))
            y += surf.get_height()+5