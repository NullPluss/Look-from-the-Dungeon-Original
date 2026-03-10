import pygame
from core.scene import Scene
from ui.camera_ui import CameraUI
from ui.player_stats_ui import PlayerStatsUI
from ui.inventory_ui import InventoryUI
from ui.ui_manager import UIManager
from ui.pause_menu import PauseMenu
from world.dungeon import Dungeon
from world.dungeon_generator_adapter import DungeonGeneratorAdapter
from world.dungeon_generator import DungeonGenerator
from core.camera import Camera
from scenes.map_scene import MapScene
from utils.layout import LayoutCell



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
        self.paused = False

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
        self.entity_manager = self.dungeon.entity_manager
        self.inventory_open = False

    def on_enter(self):
        self.ui_manager.add(CameraUI(self.camera))
        self.ui_manager.add(PlayerStatsUI(self.player))
        self.game.audio.play_music("src/assets/sounds/background.mp3")

    def on_exit(self):
        self.ui_manager.remove(CameraUI)

    def handle_event(self, event):
        """
        Обрабатывает:
        - E → взаимодействие с NPC
        - I → инвентарь
        - M → карта
        - Клик мышью → взаимодействие с NPC
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
                return
            
            if self.paused:
                return
            
            if event.key == pygame.K_e:
                self.try_interact()
            elif event.key == pygame.K_i:
                self.toggle_inventory()
            elif event.key == pygame.K_m:
                self.game.scene_manager.register("map", MapScene(self.game, self.dungeon))
                self.game.scene_manager.push_scene("map")
            elif event.key == pygame.K_F11:
                self.game.window.toggle_fullscreen()
        elif event.type == pygame.MOUSEBUTTONDOWN and self.inventory_open:
            # Передача кликов в инвентарь
            for ui in self.ui_manager.stack:
                if isinstance(ui, InventoryUI):
                    ui.handle_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
            # Клик по NPC
            self.try_click_npc(event.pos)
        # if key == pygame.K_i:
        #     self.game.scene_manager.register("inventory", InventoryScene(self.game, self.game.party))
        #     self.game.scene_manager.push_scene("inventory")
        #     return
        
    def update(self, dt):
        if self.paused:
            self.ui_manager.update(dt)
            return
        
        self.player.update(dt)
        self.dungeon.reveal_by_player(self.player)
        
        # Проверка выхода
        cell = self.dungeon.get_cell_at_pixel(self.player.rect.centerx, self.player.rect.centery)
        if cell and cell.tile_type == LayoutCell.EXIT:
            self._go_to_next_level()
            return
        
        # Проверка столкновения с монстрами на той же клетке (автоматический бой)
        player_cell = self.dungeon.get_cell_at_pixel(self.player.rect.centerx, self.player.rect.centery)
        if player_cell:
            enemies_on_cell = []
            for entity in self.dungeon.entities:
                if entity != self.player and hasattr(entity, 'hp') and not hasattr(entity, 'profession'):
                    entity_cell = self.dungeon.get_cell_at_pixel(entity.rect.centerx, entity.rect.centery)
                    if entity_cell and entity_cell == player_cell:
                        enemies_on_cell.append(entity)
            
            if enemies_on_cell:
                # Начать бой со всеми монстрами на клетке
                enemies_on_cell[0].interact(self.player, self.game)
                return

        for entity in self.dungeon.entities:
            entity.update(dt)

        self.camera.update(dt)
        self.ui_manager.update(dt)
    
    def _go_to_next_level(self):
        from scenes.next_level_scene import NextLevelScene
        self.game.scene_manager.register("next_level", NextLevelScene(self.game, "Адские пустоши"))
        self.game.scene_manager.push_scene("next_level")

    def render(self, screen):
        screen.fill((10, 10, 15))

        # ===== Отрисовка карты =====
        self.dungeon.render(screen, self.camera)

        # ===== Отрисовка сущностей (только на той же клетке что и игрок) =====
        player_cell = self.dungeon.get_cell_at_pixel(self.player.rect.centerx, self.player.rect.centery)
        if player_cell:
            for entity in self.dungeon.entities:
                if entity != self.player and hasattr(entity, 'hp'):
                    entity_cell = self.dungeon.get_cell_at_pixel(entity.rect.centerx, entity.rect.centery)
                    if entity_cell and entity_cell == player_cell:
                        screen.blit(entity.image, self.camera.apply(entity.rect))
                # Отрисовка НПС (видны всегда на исследованных клетках)
                elif hasattr(entity, 'profession'):
                    entity_cell = self.dungeon.get_cell_at_pixel(entity.rect.centerx, entity.rect.centery)
                    if entity_cell and entity_cell.explored:
                        screen.blit(entity.image, self.camera.apply(entity.rect))

        # ===== Отрисовка игрока =====
        screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # ===== UI поверх =====
        self.ui_manager.render(screen)

    def try_click_npc(self, mouse_pos):
        for entity in self.dungeon.entities:
            if hasattr(entity, 'profession'):
                entity_cell = self.dungeon.get_cell_at_pixel(entity.rect.centerx, entity.rect.centery)
                if entity_cell and entity_cell.explored:
                    screen_rect = self.camera.apply(entity.rect)
                    if screen_rect.collidepoint(mouse_pos):
                        entity.interact(self.player, self.game)
                        return
    
    def try_interact(self):
        nearby = self.entity_manager.get_near(self.player.rect, 300)

        if not nearby:
            return
        
        # Фильтруем только NPC (не монстров)
        npcs = [e for e in nearby if hasattr(e, 'profession')]
        
        if not npcs:
            return

        ent = min(npcs, key=lambda e: self.player.rect.center.distance_to(e.rect.center))

        ent.interact(self.player, self.game)

    def toggle_pause(self):
        self.paused = not self.paused
        
        if self.paused:
            pause_menu = PauseMenu(self.screen.get_size())
            pause_menu.on_resume = self.resume_game
            pause_menu.on_quit = self.quit_game
            self.game.ui_manager.add(pause_menu)
        else:
            self.game.ui_manager.remove(PauseMenu)

    def resume_game(self):
        self.paused = False
        self.game.ui_manager.remove(PauseMenu)

    def quit_game(self):
        self.game.running = False
    
    def toggle_inventory(self):
        self.inventory_open = not self.inventory_open
        
        if self.inventory_open:
            w, h = self.screen.get_size()
            inventory_ui = InventoryUI((w - 320, 100, 300, 400), self.game.party.inventory, self.player)
            self.ui_manager.add(inventory_ui)
        else:
            self.ui_manager.remove(InventoryUI)
