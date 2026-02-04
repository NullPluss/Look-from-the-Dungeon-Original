import pygame
from ui.map_ui import MapUI
from systems.combat_system import CombatSystem
from entities.chest import Chest
from core.camera import Camera
from ui.camera_ui import CameraUI
from ui.ui_manager import UIManager
from ui.inventory_ui import InventoryUI
from world.dungeon import Dungeon
from world.dungeon_generator_adapter import DungeonGeneratorAdapter
from world.dungeon_generator import DungeonGenerator
from entities.party import Party
from entities.player import Player


class Scene():
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass


class BattleScene(Scene):
    def __init__(self, game, party, enemies):
        super().__init__(game)
        self.combat = CombatSystem(party, enemies)

    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass


class DialogScene(Scene):
    def __init__(self, game, npc):
        super().__init__(game)
        self.npc = npc
    
    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass

class DungeonScene(Scene):
    """
    Основная игровая сцена.
    """

    def __init__(self, game):
        self.game = game
        self.screen = game.window.screen

        self.dungeon = None
        self.player = None
        self.camera = None

        self.ui_manager = UIManager()

    def on_enter(self):
        # ===== Создание мира =====
        self.dungeon = Dungeon(DungeonGeneratorAdapter(DungeonGenerator(64, 64)))
        self.dungeon.generate()

        # ===== Создание игрока =====
        self.player = self.game.party.player
        self.player.dungeon = self.dungeon
        self.player.rect.topleft = self.dungeon.get_start_position()

        # ===== Камера =====
        w, h = self.screen.get_size()
        self.camera = Camera(w, h, smoothing=0.08)
        self.camera.follow(self.player)

        # ===== UI =====
        self.ui_manager.add(CameraUI(self.camera))
        self.ui_manager.add(InventoryUI((20, h - 240, 320, 220)))

        self.dungeon.add_entity(self.player)

    def on_exit(self):
        self.ui_manager.elements.clear()

    def handle_event(self, event):
        """
        Обрабатывает:
        - I → инвентарь
        - M → карта
        """
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:
        #         self.player.move_dir.y = -1
        #     elif event.key == pygame.K_s:
        #         self.player.move_dir.y = 1
        #     elif event.key == pygame.K_a:
        #         self.player.move_dir.x = -1
        #     elif event.key == pygame.K_d:
        #         self.player.move_dir.x = 1

        #     elif event.key == pygame.K_F11:
        #         self.game.window.toggle_fullscreen()

        #     elif event.key == pygame.K_e:
        #         self.try_interact()

        # elif event.type == pygame.KEYUP:
        #     if event.key in (pygame.K_w, pygame.K_s):
        #         self.player.move_dir.y = 0
        #     elif event.key in (pygame.K_a, pygame.K_d):
        #         self.player.move_dir.x = 0

    def update(self, dt):
        self.player.update(dt)

        for entity in self.dungeon.entities:
            entity.update(dt)

        self.camera.update(dt)
        self.ui_manager.update(dt)

    def render(self, screen):
        screen.fill((10, 10, 15))

        # ===== Отрисовка карты =====
        for cell in self.dungeon.cells:
            screen.blit(cell.image, self.camera.apply(cell.rect))

        # ===== Отрисовка сущностей =====
        for entity in self.dungeon.entities:
            screen.blit(entity.image, self.camera.apply(entity.rect))

        # ===== Отрисовка игрока =====
        screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # ===== UI поверх =====
        self.ui_manager.render(screen)



class InventoryScene(Scene):
    def __init__(self, game, party):
        super().__init__(game)
        self.party = party

    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass


class LootScene(Scene):
    def __init__(self, game, party, chest: Chest):
        super().__init__(game)
        self.party = party
        self.chest = chest

    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass

class MapScene(Scene):
    def __init__(self, game, dungeon):
        super().__init__(game)
        self.map_ui = MapUI(dungeon)

    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass