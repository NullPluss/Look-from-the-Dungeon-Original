import pygame
from ui.inventory_ui import InventoryUI
from ui.map_ui import MapUI
from systems.combat_system import CombatSystem
from entities.chest import Chest
from systems.events import OpenInventoryEvent, OpenMapEvent
from ui.camera_ui import Camera

from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, screen):
        pass


class BattleScene(Scene):
    def __init__(self, game, party, enemies):
        super().__init__(game)
        self.combat = CombatSystem(party, enemies)

    def update(self, dt):
        if self.combat.is_finished():
            self.game.scene_manager.change_scene(
                DungeonScene(...)
            )


class DialogScene(Scene):
    def __init__(self, game, npc):
        super().__init__(game)
        self.npc = npc

    def handle_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.scene_manager.change_scene(
                self.game.last_scene
            )
        # Обработка диалога с NPC здесь
        pass


class DungeonScene(Scene):
    """
    Основная игровая сцена.
    """

    def __init__(self, game, dungeon, party):
        self.game = game
        self.dungeon = dungeon
        self.party = party
        self.player = party.get_player()
        self.camera = Camera(
            screen_size=(game.window.screen.get_size()),
            world_size=(6400, 6400)
        )

    def handle_event(self, event):
        """
        Обрабатывает:
        - I → инвентарь
        - M → карта
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.move_dir.y = -1
            elif event.key == pygame.K_s:
                self.player.move_dir.y = 1
            elif event.key == pygame.K_a:
                self.player.move_dir.x = -1
            elif event.key == pygame.K_d:
                self.player.move_dir.x = 1

            elif event.key == pygame.K_F11:
                self.game.window.toggle_fullscreen()

            elif event.key == pygame.K_e:
                self.try_interact()

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                self.player.move_dir.y = 0
            elif event.key in (pygame.K_a, pygame.K_d):
                self.player.move_dir.x = 0

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    def update(self, dt):
        self.player.update(dt)
        # self.map.update(dt)
        self.camera.update(self.player.rect.center, dt)

    def on_enter(self):
        """
        Инициализация сцены.
        """
        return 

    def render(self, screen):
        self.game.ui_manager.render(screen)



class InventoryScene(Scene):
    def __init__(self, game, party):
        super().__init__(game)
        self.party = party

    def handle_event(self, event):
        if event.key == pygame.K_i:
            self.game.scene_manager.change_scene(
                self.game.last_scene
            )
        
        if event.key == pygame.K_i:
            self.game.event_manager.emit(OpenInventoryEvent())


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


class MapScene(Scene):
    def __init__(self, game, dungeon):
        super().__init__(game)
        self.map_ui = MapUI(dungeon)

    def handle_event(self, event):
        if event.key == pygame.K_m:
            self.game.event_manager.emit(OpenMapEvent())