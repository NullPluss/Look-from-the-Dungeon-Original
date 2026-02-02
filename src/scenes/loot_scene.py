import pygame
from core.scene import Scene
from entities.chest import Chest
from scenes.inventory_scene import InventoryScene

class LootScene(Scene):
    def __init__(self, game, party, chest: Chest):
        super().__init__(game)
        self.party = party
        self.chest = chest

    def handle_event(self, event):
        if event.key == pygame.K_i:
            self.game.scene_manager.change_scene(
                InventoryScene(self.game, self.party)
            )
        elif event.key == pygame.K_ESCAPE:
            self.game.scene_manager.change_scene(
                self.game.last_scene
            )
        # Обработка взаимодействия с сундуком здесь
        pass