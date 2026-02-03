import pygame
from core.scene_manager import SceneManager
from core.window import Window
from core.audio import AudioManager
from core.event_manager import EventManager
from systems.events import StartBattleEvent, OpenInventoryEvent, OpenMapEvent
from core.scene import BattleScene, DungeonScene, InventoryScene, MapScene
from world.dungeon import Dungeon
from world.dungeon_generator_adapter import DungeonGeneratorAdapter
from world.dungeon_generator import DungeonGenerator
from entities.party import Party
from entities.character import Character
from ui.ui_manager import UIManager



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
        self.running = True
        self.window = Window()
        self.audio = AudioManager()
        event_manager = EventManager()
        scene_manager = SceneManager()
        ui_manager = UIManager()
        self.dungeon = Dungeon(DungeonGeneratorAdapter(DungeonGenerator(32, 32)))
        self.dungeon.generate()
        start_x, start_y = self.dungeon.get_starting_position()
        
        rect = pygame.Rect(start_x * 200, start_y * 200, 10, 20)
        self.party = Party(Character("Hero", 100, 100, start_x, start_y, rect), {})
        self.clock = pygame.time.Clock()

        self.scene_manager.push(DungeonScene(self, self.dungeon, self.party))

        # self.event_manager.subscribe(StartBattleEvent, self.on_start_battle)
        # self.event_manager.subscribe(OpenInventoryEvent, self.on_open_inventory)
        # self.event_manager.subscribe(OpenMapEvent, self.on_open_map)
        event_manager.subscribe("QUIT", lambda: exit())
        # event_manager.subscribe("KEYDOWN", on_key)


    def run(self):
        self.audio.play_music("sounds/background.mp3")
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            self.event_manager.process_pygame_events()
            self.ui_manager.update(dt)
            self.scene_manager.update(dt)
            self.scene_manager.render(self.screen)
            self.ui_manager.render(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()
        exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.scene_manager.handle_event(event)