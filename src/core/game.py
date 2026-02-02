import pygame
from core.scene_manager import SceneManager
from core.window import Window
from core.audio import AudioManager
from core.event_manager import EventManager
from systems.events import StartBattleEvent, OpenInventoryEvent, OpenMapEvent
from scenes.battle_scene import BattleScene
from scenes.dungeon_scene import DungeonScene
from scenes.inventory_scene import InventoryScene
from scenes.map_scene import MapScene
from world.dungeon import Dungeon
from world.dungeon_generator_adapter import DungeonGeneratorAdapter
from world.dungeon_generator import DungeonGenerator
from entities.party import Party



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

        self.party = Party()
        self.window = Window()
        self.audio = AudioManager()
        self.scene_manager = SceneManager()
        self.event_manager = EventManager()
        self.dungeon = DungeonGeneratorAdapter(DungeonGenerator())
        self.dungeon.build()
        self.clock = pygame.time.Clock()

        self.scene_manager.change_scene(DungeonScene(self, self.dungeon), self.party)

        # self.event_manager.subscribe(StartBattleEvent, self.on_start_battle)
        # self.event_manager.subscribe(OpenInventoryEvent, self.on_open_inventory)
        # self.event_manager.subscribe(OpenMapEvent, self.on_open_map)


    def run(self):
        self.audio.play_music("sounds/background.mp3")

        while True:
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.scene_manager.update(dt)
            self.scene_manager.render(self.window.screen)
            
            pygame.display.flip()
            
            if pygame.event.peek(pygame.QUIT):
                break
        pygame.quit()
        exit()

    def handle_events(self):
        for event in pygame.event.get():
            self.scene_manager.handle_event(event)

    def update(self, dt):
        self.scene_manager.update(dt)
        
    def render(self):
        self.scene_manager.render(self.window.screen)

    def on_start_battle(self, event):
        self.scene_manager.change_scene(
            BattleScene(self, self.party, event.enemies)
        )

    def on_open_inventory(self, event):
        self.scene_manager.change_scene(
            InventoryScene(self, self.party)
        )

    def on_open_map(self, event):
        self.scene_manager.change_scene(
            MapScene(self, self.dungeon)
        )

    def on_end_battle(self, event):
        self.scene_manager.change_scene(self.last_scene)

    def on_event(self, event):
        if isinstance(event, StartBattleEvent):
            self.scene_manager.change_scene(
                BattleScene(event.monsters, self.party)
            )