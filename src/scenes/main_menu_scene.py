import pygame
from core.scene import Scene

class MainMenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("arial", 32)
        self.small_font = pygame.font.SysFont("arial", 24)
        self.selected = 0
        self.levels = ["Горные глубины", "Адские пустоши"]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected = (self.selected - 1) % len(self.levels)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected = (self.selected + 1) % len(self.levels)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._start_game()
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False
                
    def _start_game(self):
        from scenes.dungeon_scene import DungeonScene
        from entities.player import Player
        from entities.party import Party
        from systems.inventory_system import Inventory
        
        self.game.player = Player("Hero", (0, 0), None)
        self.game.party = Party(self.game.player, Inventory())
        
        self.game.scene_manager.register("dungeon", DungeonScene(self.game))
        self.game.scene_manager.push_scene("dungeon")
        
    def render(self, screen):
        screen.fill((20, 20, 30))
        
        title = self.font.render("Look from the Dungeon", True, (255, 255, 100))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))
        
        subtitle = self.small_font.render("Выберите уровень:", True, (200, 200, 200))
        screen.blit(subtitle, (screen.get_width() // 2 - subtitle.get_width() // 2, 200))
        
        for i, level in enumerate(self.levels):
            color = (255, 255, 100) if i == self.selected else (150, 150, 150)
            text = self.small_font.render(level, True, color)
            y = 280 + i * 50
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
        
        hint = self.small_font.render("Enter - начать игру | ESC - выход", True, (100, 100, 100))
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, screen.get_height() - 100))
