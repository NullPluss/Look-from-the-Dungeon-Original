import pygame
from entities.entity import Entity
from world.tile_registry import TileRegistry

class Player(Entity):
    def __init__(self, name, pos, dungeon, speed=250):
        super().__init__(pos)

        self.name = name
        self.dungeon = dungeon
        self.speed = speed

        self.velocity = pygame.Vector2(0, 0)

        # self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        # pygame.draw.rect(self.image, (60, 200, 80), (0, 0, 28, 28), border_radius=6)
        self.image = TileRegistry.PLAYER

        self.rect = self.image.get_rect(topleft=pos)

    # ================== Input ==================

    def handle_input(self):
        keys = pygame.key.get_pressed()

        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pygame.K_w]:
            self.velocity.y = -1
        if keys[pygame.K_s]:
            self.velocity.y = 1
        if keys[pygame.K_a]:
            self.velocity.x = -1
        if keys[pygame.K_d]:
            self.velocity.x = 1

        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize()

    # ================== Update ==================

    def update(self, dt):
        self.handle_input()

        dx = self.velocity.x * self.speed * dt
        dy = self.velocity.y * self.speed * dt

        self.dungeon.collide_walls(self.rect, dx, dy)

    # ================== Debug ==================

    def draw_debug(self, screen, camera):
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.rect), 1)
