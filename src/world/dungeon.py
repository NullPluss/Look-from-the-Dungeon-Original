import pygame

from world.dungeon_cell import DungeonCell
from utils.layout import LayoutCell
from utils.constants import TILE_SIZE
from world.tile_registry import TileRegistry


class Dungeon:
    """
    Класс игрового подземелья.
    Отвечает за:
    - хранение карты
    - генерацию
    - хранение сущностей
    - коллизии
    """
    TILE_SIZE = TILE_SIZE

    def __init__(self, generator_adapter):
        self.width = generator_adapter.generator.width
        self.height = generator_adapter.generator.height
        self.generator_adapter = generator_adapter
 
        self.cells = []
        self.entities = []

        self.grid = []

    def reveal_by_player(self, player):
        cell = self.get_cell_at_pixel(
            player.rect.centerx,
            player.rect.centery
        )
        if cell:
            cell.explored = True

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_visible_by_pixel(self, x, y, px, py, radius=1):
        gx = int(px // TILE_SIZE)
        gy = int(py // TILE_SIZE)

        return abs(x - gx) <= radius and abs(y - gy) <= radius

    def render(self, screen, camera):
        for cell in self.cells:
            if cell.explored:
                screen.blit(cell.image, camera.apply(cell.rect))
            elif self.is_visible_by_pixel(
                cell.rect.x // TILE_SIZE,
                cell.rect.y // TILE_SIZE,
                camera.target.rect.centerx,
                camera.target.rect.centery,
                radius=1
            ):
                dark_image = TileRegistry._make_dark(cell.image)
                screen.blit(dark_image, camera.apply(cell.rect))

    def generate(self):
        """
        Генерация карты через адаптер генератора
        """
        if self.generator_adapter:
            self.grid = self.generator_adapter.generate()

        self._build_cells()

    def _build_cells(self):
        """
        Создаёт DungeonCell из grid карты
        """
        self.cells.clear()

        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.grid[y][x]

                cell = DungeonCell(
                    x * self.TILE_SIZE,
                    y * self.TILE_SIZE,
                    self.TILE_SIZE,
                    tile_type
                )
                self.cells.append(cell)

        self.cell_map = {(c.x, c.y): c for c in self.cells}

    def get_cell(self, x, y):
        return self.cell_map.get((x, y))

    def get_cell_at_pixel(self, px, py):
        return self.get_cell(
            px // TILE_SIZE,
            py // TILE_SIZE
        )

    # ================== Entity API ==================

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    # ================== Collisions ==================

    def get_near_walls(self, rect):
        """
        Возвращает список стен вокруг rect
        для оптимальной коллизии
        """
        tiles = []

        left = rect.left // self.TILE_SIZE
        right = rect.right // self.TILE_SIZE
        top = rect.top // self.TILE_SIZE
        bottom = rect.bottom // self.TILE_SIZE

        for y in range(max(0, top - 1), min(self.height, bottom + 2)):
            for x in range(max(0, left - 1), min(self.width, right + 2)):
                if self.grid[y][x] == LayoutCell.VOID:
                    tiles.append(
                        pygame.Rect(
                            x * self.TILE_SIZE,
                            y * self.TILE_SIZE,
                            self.TILE_SIZE,
                            self.TILE_SIZE
                        )
                    )
        return tiles

    def collide_walls(self, rect, dx, dy):
        """
        Обрабатывает коллизии со стенами
        """
        rect.x += dx
        for wall in self.get_near_walls(rect):
            if rect.colliderect(wall):
                if dx > 0:
                    rect.right = wall.left
                if dx < 0:
                    rect.left = wall.right

        rect.y += dy
        for wall in self.get_near_walls(rect):
            if rect.colliderect(wall):
                if dy > 0:
                    rect.bottom = wall.top
                if dy < 0:
                    rect.top = wall.bottom

    # ================== Helpers ==================

    def world_to_grid(self, pos):
        x, y = pos
        return x // self.TILE_SIZE, y // self.TILE_SIZE

    def grid_to_world(self, grid_pos):
        x, y = grid_pos
        return x * self.TILE_SIZE, y * self.TILE_SIZE

    def is_walkable(self, grid_x, grid_y):
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            # return self.grid[grid_y][grid_x] == LayoutCell.FLOOR or self.grid[grid_y][grid_x] == LayoutCell.EXIT or self.grid[grid_y][grid_x] == LayoutCell.START
            return self.grid[grid_y][grid_x] != LayoutCell.VOID
        return False
    
    def get_start_position(self):
        for cell in self.cells:
            if cell.tile_type == LayoutCell.START:
                return cell.rect.topleft
        return None