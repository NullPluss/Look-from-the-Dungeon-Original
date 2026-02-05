import pygame
from core.scene import Scene
from ui.camera_ui import CameraUI
from ui.map_ui import MapUI
from ui.ui_manager import UIManager
from world.dungeon import Dungeon
from world.dungeon_generator_adapter import DungeonGeneratorAdapter
from world.dungeon_generator import DungeonGenerator
from core.camera import Camera
from scenes.map_scene import MapScene



class DungeonScene(Scene):
    """
    Основная игровая сцена.
    """

    def __init__(self, game):
        super().__init__(game)
        self.screen = game.window.screen

        self.dungeon = None
        self.player = None
        self.camera = None

        self.ui_manager = UIManager()

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

        # self.ui_manager.add(InventoryUI((20, h - 240, 320, 220)))

        self.dungeon.add_entity(self.player)

    def on_enter(self):
        self.ui_manager.add(CameraUI(self.camera))

    def on_exit(self):
        self.ui_manager.remove(CameraUI)

    def handle_event(self, event):
        """
        Обрабатывает:
        - I → инвентарь
        - M → карта
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.game.scene_manager.register("map", MapScene(self.game, self.dungeon))
                self.game.scene_manager.push_scene("map")
                return
            if event.key == pygame.K_F11:
                self.game.window.toggle_fullscreen()
                return
        # if key == pygame.K_i:
        #     self.game.scene_manager.register("inventory", InventoryScene(self.game, self.game.party))
        #     self.game.scene_manager.push_scene("inventory")
        #     return
        

        

    def update(self, dt):
        self.player.update(dt)
        self.dungeon.reveal_by_player(self.player)

        for entity in self.dungeon.entities:
            entity.update(dt)

        self.camera.update(dt)
        self.ui_manager.update(dt)

    def render(self, screen):
        screen.fill((10, 10, 15))

        # ===== Отрисовка карты =====
        self.dungeon.render(screen, self.camera)

        # ===== Отрисовка сущностей =====
        for entity in self.dungeon.entities:
            screen.blit(entity.image, self.camera.apply(entity.rect))

        # ===== Отрисовка игрока =====
        screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # ===== UI поверх =====
        self.ui_manager.render(screen)