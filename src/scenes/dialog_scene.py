import pygame
from core.scene import Scene

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