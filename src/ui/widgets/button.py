import pygame
from ui.base_ui import BaseUI

class Button(BaseUI):
    def __init__(self, rect, text, callback, font=None):
        super().__init__(rect)
        self.text = text
        self.callback = callback
        self.font = font or pygame.font.SysFont("arial", 18)
        self.color = (80,80,80)
        self.hover = False

    def render(self, screen):
        color = (120,120,120) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect)
        label = self.font.render(self.text, True, (255,255,255))
        screen.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.callback()