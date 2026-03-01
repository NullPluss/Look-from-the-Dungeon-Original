import pygame
from core.scene_manager import SceneManager
from core.window import Window
from core.audio import AudioManager
from core.event_manager import EventManager
from scenes.dungeon_scene import DungeonScene
from entities.party import Party
from entities.player import Player
from ui.ui_manager import UIManager
from world.tile_registry import TileRegistry
from utils.asset_registry import AssetRegistry

class Game:
    """
    Главный управляющий класс игры.
    Отвечает за:
    - инициализацию pygame
    - окно
    - главный цикл
    - scene manager
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Look from the Dungeon")
        self.clock = pygame.time.Clock()
        self.running = True
        self.window = Window()
        self.audio = AudioManager()
        self.event_manager = EventManager()
        self.scene_manager = SceneManager()
        self.ui_manager = UIManager()
        TileRegistry.init()
        AssetRegistry.init()

        self.player = Player("Hero", (0, 0), None)
        self.party = Party(self.player, {})

        self.scene_manager.register("dungeon", DungeonScene(self))
        self.scene_manager.push_scene("dungeon")

        self.event_manager.subscribe("QUIT", self.quit1)
        self.event_manager.subscribe("KEYDOWN", self.handle_keydown)
        self.event_manager.subscribe("MOUSEWHEEL", self.handle_mousewheel)
        self.event_manager.subscribe("MOUSE_DOWN", self.handle_mouse_down)
        self.event_manager.subscribe("MOUSE_UP", self.handle_mouse_up)
        self.event_manager.subscribe("MOUSE_MOVE", self.handle_mouse_move)

    def handle_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.scene_manager.handle_event(event)
        elif not getattr(self.scene_manager.active_scene, 'paused', False):
            self.scene_manager.handle_event(event)
        else:
            self.ui_manager.handle_event(event)
    
    def handle_mousewheel(self, event):
        if not getattr(self.scene_manager.active_scene, 'paused', False):
            self.scene_manager.handle_event(event)
    
    def handle_mouse_down(self, event):
        if getattr(self.scene_manager.active_scene, 'paused', False):
            self.ui_manager.handle_event(event)
        else:
            self.scene_manager.handle_event(event)
    
    def handle_mouse_up(self, event):
        if not getattr(self.scene_manager.active_scene, 'paused', False):
            self.scene_manager.handle_event(event)
    
    def handle_mouse_move(self, event):
        if getattr(self.scene_manager.active_scene, 'paused', False):
            self.ui_manager.handle_event(event)
        else:
            self.scene_manager.handle_event(event)


    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            self.event_manager.process_pygame_events()
            self.ui_manager.update(dt)
            self.scene_manager.update(dt)
            self.scene_manager.render(self.window.screen)
            self.ui_manager.render(self.window.screen)
            
            pygame.display.flip()
        
        pygame.quit()
        exit()

    def quit1(self):
        self.running = False