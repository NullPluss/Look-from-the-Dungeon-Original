import pygame
from utils.layout import LayoutCell
from world.tile_registry import TileRegistry
from utils.constants import TILE_SIZE

class MapUI:
    def __init__(self, dungeon, camera):
        self.dungeon = dungeon
        self.camera = camera

        self.zoom = 2.5
        self.tile_size = 6

        self.dragging = False
        self.last_mouse = None

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


    def rebuild_cache(self):
        size = int(self.tile_size * self.zoom)

        w = self.dungeon.width * size
        h = self.dungeon.height * size

        self.cached_surface = pygame.Surface((w, h), pygame.SRCALPHA)

        floor_scaled = pygame.transform.smoothscale(TileRegistry.FLOOR, (size, size))
        void_scaled  = pygame.transform.smoothscale(TileRegistry.VOID,  (size, size))

        for cell in self.dungeon.cells:
            tile = floor_scaled if cell.explored else void_scaled

            gx = cell.rect.x // TILE_SIZE
            gy = cell.rect.y // TILE_SIZE

            self.cached_surface.blit(tile, (gx * size, gy * size))

        self.cached_zoom = self.zoom

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


    def update(self, dt):
        self.camera.update(dt)