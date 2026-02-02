import pygame
from ui.inventory_ui import InventoryUI
from ui.map_ui import MapUI
from core.scene import Scene

class DungeonScene(Scene):
    """
    Основная игровая сцена.
    """

    def __init__(self, game, dungeon, party):
        self.game = game
        self.dungeon = dungeon
        self.party = party
        self.x = 0
        self.y = 0

    def handle_event(self, event):
        """
        Обрабатывает:
        - движение
        - I → инвентарь
        - M → карта
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.y -= 1
            if event.key == pygame.K_s:
                self.y += 1
            if event.key == pygame.K_a:
                self.x -= 1
            if event.key == pygame.K_d:
                self.x += 1
            if event.key == pygame.K_i:
                self.game.ui_manager.set_ui(
                    InventoryUI(self.game, self.party)
                )
            if event.key == pygame.K_m:
                self.game.ui_manager.set_ui(
                    MapUI(self.dungeon)
                )


    def update(self, dt):
        """
        Движение игрока + события клеток.
        """
        pass

    # def render(self, screen):
    #     self.game.ui_manager.render(screen)

    def render(self, screen):
        screen.fill((30, 30, 30))

        for row in self.dungeon.grid:
            for cell in row:
                pygame.draw.rect(
                    screen,
                    (70, 70, 70),
                    (cell.x * 40, cell.y * 40, 38, 38),
                    1
                )

        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (self.x * 40, self.y * 40, 38, 38)
        )