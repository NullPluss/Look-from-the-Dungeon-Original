import pygame
from core.scene_manager import SceneManager
from core.window import Window
from core.audio import AudioManager
from core.event_manager import EventManager
from core.scene import BattleScene, DungeonScene, InventoryScene, MapScene
from entities.party import Party
from entities.player import Player
from ui.ui_manager import UIManager
from core.camera import Camera
from ui.camera_ui import CameraUI


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

        self.player = Player("Hero", (0, 0), None)
        self.party = Party(self.player, {})

        self.scene_manager.register("dungeon", DungeonScene(self))
        self.scene_manager.set_scene("dungeon")

        self.event_manager.subscribe("QUIT", lambda: exit())
        self.event_manager.subscribe("KEYDOWN", self.on_keydown)


    def run(self):
        self.audio.play_music("sounds/background.mp3")
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

    def on_keydown(self, key):
        if key == pygame.K_F11:
            self.window.toggle_fullscreen()