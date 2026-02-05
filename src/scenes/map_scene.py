import pygame
from core.scene import Scene
from ui.map_ui import MapUI
from core.camera import Camera


class MapScene(Scene):
    def __init__(self, game, dungeon):
        super().__init__(game)
        self.camera = None
        self.map_ui = None
        self.dungeon = dungeon

    def on_enter(self):
        w, h = self.game.window.screen.get_size()

        self.camera = Camera(w, h, smoothing=0.25)

        # if self.game.player:
        #     self.camera.follow(self.game.player)

        self.map_ui = MapUI(self.dungeon, self.camera)

        self.game.ui_manager.add(self.map_ui)

    def on_exit(self):
        if self.map_ui:
            self.game.ui_manager.remove(MapUI)
            self.map_ui = None

        self.camera = None

    def update(self, dt):
        self.map_ui.update(dt)

    def render(self, screen):
        screen.fill((10, 10, 10))
        self.map_ui.render(screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                self.game.scene_manager.remove("map")
                self.game.scene_manager.pop_scene()
                return

        self.map_ui.handle_event(event)