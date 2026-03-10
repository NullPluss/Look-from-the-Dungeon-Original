import pygame
from core.scene import Scene

class TradeScene(Scene):
    def __init__(self, game, npc):
        super().__init__(game)
        self.npc = npc
        self.font = pygame.font.SysFont("arial", 20)
        self.title_font = pygame.font.SysFont("arial", 28)
        self.selected_index = 0
        self.items = []
        self.message = ""
        
    def on_enter(self):
        self.items = list(self.game.party.inventory.get_items().items())
        if not self.items:
            self.message = "У вас нет предметов для обмена"
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.scene_manager.pop_scene()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.items:
                    self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.items:
                    self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.items:
                    self._trade_item()
                    
    def _trade_item(self):
        item_name, count = self.items[self.selected_index]
        self.game.party.inventory.remove_item(item_name, 1)
        self.game.party.inventory.add_item("Зелье здоровья", 1)
        self.message = f"Обменяли {item_name} на Зелье здоровья"
        self.items = list(self.game.party.inventory.get_items().items())
        if self.selected_index >= len(self.items):
            self.selected_index = max(0, len(self.items) - 1)
            
    def render(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        w, h = screen.get_size()
        dialog_rect = pygame.Rect(w // 4, h // 4, w // 2, h // 2)
        pygame.draw.rect(screen, (40, 40, 50), dialog_rect)
        pygame.draw.rect(screen, (100, 100, 120), dialog_rect, 3)
        
        title = self.title_font.render(f"Торговля с {self.npc.name}", True, (255, 255, 100))
        screen.blit(title, (dialog_rect.centerx - title.get_width() // 2, dialog_rect.y + 20))
        
        y_offset = dialog_rect.y + 70
        
        if not self.items:
            empty_text = self.font.render("У вас нет предметов", True, (200, 200, 200))
            screen.blit(empty_text, (dialog_rect.x + 20, y_offset))
        else:
            info = self.font.render("Обмен: любой предмет → Зелье здоровья", True, (200, 200, 200))
            screen.blit(info, (dialog_rect.x + 20, y_offset))
            y_offset += 40
            
            for i, (item_name, count) in enumerate(self.items):
                color = (255, 255, 100) if i == self.selected_index else (200, 200, 200)
                text = self.font.render(f"{item_name} ({count}шт)", True, color)
                screen.blit(text, (dialog_rect.x + 20, y_offset))
                y_offset += 30
        
        if self.message:
            msg = self.font.render(self.message, True, (100, 255, 100))
            screen.blit(msg, (dialog_rect.x + 20, dialog_rect.bottom - 60))
        
        hint = self.font.render("Enter - обменять | ESC - выход", True, (150, 150, 150))
        screen.blit(hint, (dialog_rect.x + 20, dialog_rect.bottom - 30))
