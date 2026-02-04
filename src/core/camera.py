import pygame

class Camera:
    def __init__(self, width, height, smoothing=0.1):
        self.width = width
        self.height = height
        self.offset = pygame.Vector2(0, 0)
        self.target = None
        self.smoothing = smoothing

    def follow(self, target):
        self.target = target

    def update(self, dt):
        if not self.target:
            return
        desired = pygame.Vector2(
            self.target.rect.centerx - self.width // 2,
            self.target.rect.centery - self.height // 2
        )
        self.offset += (desired - self.offset) * self.smoothing

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)