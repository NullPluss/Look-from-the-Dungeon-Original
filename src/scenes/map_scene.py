import pygame
from core.scene import Scene
from ui.map_ui import MapUI
from systems.events import OpenMapEvent


class MapScene(Scene):
    def __init__(self, game, dungeon):
        super().__init__(game)
        self.map_ui = MapUI(dungeon)

    def handle_event(self, event):
        if event.key == pygame.K_m:
            self.game.event_manager.emit(OpenMapEvent())