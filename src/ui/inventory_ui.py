import pygame
from ui.base_ui import BaseUI

class InventoryUI(BaseUI):
    def __init__(self, rect, inventory):
        super().__init__(rect)
        self.inventory = inventory
        self.font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 24)

    def render(self, screen):
        # Фон
        pygame.draw.rect(screen, (30, 30, 40), self.rect)
        pygame.draw.rect(screen, (80, 80, 110), self.rect, 2)
        
        # Заголовок
        title = self.title_font.render("Инвентарь", True, (255, 255, 255))
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Список предметов
        y_offset = 50
        items = self.inventory.get_items()
        
        if not items:
            empty_text = self.font.render("Пусто", True, (150, 150, 150))
            screen.blit(empty_text, (self.rect.x + 10, self.rect.y + y_offset))
        else:
            for item_name, count in items.items():
                text = self.font.render(f"{item_name} ({count}шт)", True, (200, 200, 200))
                screen.blit(text, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 30