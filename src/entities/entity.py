import pygame

class Entity:
    def __init__(self, pos):
        self.image = None
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.blit(self.image, self.rect)