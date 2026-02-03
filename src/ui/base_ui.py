import pygame

class BaseUI:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.visible = True

    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass