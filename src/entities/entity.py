import pygame

class Entity:
    def __init__(self, pos, size=(32,32)):
        self.rect = pygame.Rect(0,0,*size)
        self.rect.center = pos
        self.alive = True
        self.image = pygame.Surface(size)
        self.image.fill((255, 0, 0))

    def update(self, dt):
        pass

    def render(self, screen, camera):
        pygame.draw.rect(screen, (255,0,0), camera.apply(self.rect), 2)

    def interact(self, player, scene_manager, event_manager):
        pass

    def destroy(self):
        self.alive = False