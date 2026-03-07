import pygame
from core.scene import Scene

class NextLevelScene(Scene):
    def __init__(self, game, level_name):
        super().__init__(game)
        self.level_name = level_name
        self.font = pygame.font.SysFont("arial", 32)
        self.small_font = pygame.font.SysFont("arial", 24)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self._return_to_menu()
                
    def _return_to_menu(self):
        from scenes.main_menu_scene import MainMenuScene
        self.game.scene_manager.scenes.clear()
        self.game.scene_manager.scene_stack.clear()
        self.game.scene_manager.register("main_menu", MainMenuScene(self.game))
        self.game.scene_manager.active_scene = self.game.scene_manager.scenes["main_menu"]
        
    def render(self, screen):
        screen.fill((20, 20, 30))
        
        title = self.font.render(f"Следующий этаж: {self.level_name}", True, (255, 255, 100))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, screen.get_height() // 2 - 50))
        
        hint = self.small_font.render("Enter/ESC - Выйти в главное меню", True, (200, 200, 200))
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, screen.get_height() // 2 + 50))
