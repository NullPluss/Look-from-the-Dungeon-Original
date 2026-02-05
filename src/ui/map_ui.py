import pygame
from world.tile_registry import TileRegistry
from utils.asset_registry import AssetRegistry
from utils.constants import TILE_SIZE

class MapUI:
    def __init__(self, dungeon, camera, player):
        self.dungeon = dungeon
        self.camera = camera

        self.zoom = 5
        self.tile_size = 6

        self.dragging = False
        self.last_mouse = None

        self.player = player
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            old_zoom = self.zoom
            self.zoom = max(0.6, min(8.0, self.zoom + event.y * 0.15))

            # корректируем offset, чтобы зум был относительно курсора
            if self.zoom != old_zoom:
                mouse = pygame.Vector2(pygame.mouse.get_pos())
                world_before = (mouse + self.camera.offset) / old_zoom
                self.camera.offset = world_before * self.zoom - mouse

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.dragging = True
            self.last_mouse = pygame.Vector2(pygame.mouse.get_pos())

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            cur = pygame.Vector2(pygame.mouse.get_pos())
            self.camera.offset -= (cur - self.last_mouse)
            self.last_mouse = cur

    def render(self, screen):
        size = int(self.tile_size * self.zoom)

        cam_x = int(self.camera.offset.x)
        cam_y = int(self.camera.offset.y)

        screen_w, screen_h = screen.get_size()

        start_x = max(0, cam_x // size)
        start_y = max(0, cam_y // size)

        end_x = min(self.dungeon.width,  (cam_x + screen_w) // size + 2)
        end_y = min(self.dungeon.height, (cam_y + screen_h) // size + 2)

        floor = pygame.transform.smoothscale(TileRegistry.FLOOR, (size, size))
        void  = pygame.transform.smoothscale(TileRegistry.VOID,  (size, size))

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                cell = self.dungeon.get_cell(x, y)
                if not cell:
                    continue

                tile = floor if cell.explored else void

                px = x * size - cam_x
                py = y * size - cam_y

                screen.blit(tile, (px, py))
        
        # Рендер игрока там где он стоит
        icon = pygame.transform.smoothscale(AssetRegistry.PLAYER, (10, 20))
        screen.blit(icon, (self.player.rect.centerx // TILE_SIZE * size - cam_x - 5,
                                   self.player.rect.centery // TILE_SIZE * size - cam_y - 10))


    def update(self, dt):
        self.camera.update(dt)