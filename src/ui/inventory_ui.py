import pygame
from ui.base_ui import BaseUI

class InventoryUI(BaseUI):
    def __init__(self, rect, inventory, player=None):
        super().__init__(rect)
        self.inventory = inventory
        self.player = player
        self.font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 14)
        self.selected_item = None
        self.confirm_use = False
        self.message = ""
        self.message_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.confirm_use:
                # Обработка подтверждения
                yes_rect = pygame.Rect(self.rect.centerx - 60, self.rect.centery + 20, 50, 30)
                no_rect = pygame.Rect(self.rect.centerx + 10, self.rect.centery + 20, 50, 30)
                
                if yes_rect.collidepoint(event.pos):
                    self._use_item()
                    self.confirm_use = False
                    self.selected_item = None
                elif no_rect.collidepoint(event.pos):
                    self.confirm_use = False
                    self.selected_item = None
            else:
                # Клик по предмету
                y_offset = 50
                items = self.inventory.get_items()
                for item_name, count in items.items():
                    item_rect = pygame.Rect(self.rect.x + 10, self.rect.y + y_offset, self.rect.width - 20, 25)
                    if item_rect.collidepoint(event.pos):
                        if self._is_potion(item_name):
                            self.selected_item = item_name
                            self.confirm_use = True
                        break
                    y_offset += 30
    
    def _is_potion(self, item_name):
        return item_name in ["Зелье здоровья", "Зелье маны"]
    
    def _use_item(self):
        if not self.player or not self.selected_item:
            return
        
        if self.selected_item == "Зелье здоровья":
            if self.player.hp >= self.player.max_hp:
                self.message = "Здоровье уже максимальное!"
                self.message_timer = 2.0
                return
            self.player.hp = min(self.player.max_hp, self.player.hp + 50)
            self.inventory.remove_item(self.selected_item, 1)
            self.message = "Использовано зелье здоровья (+50 HP)"
            self.message_timer = 2.0
        elif self.selected_item == "Зелье маны":
            if self.player.mp >= self.player.max_mp:
                self.message = "Мана уже максимальная!"
                self.message_timer = 2.0
                return
            self.player.mp = min(self.player.max_mp, self.player.mp + 50)
            self.inventory.remove_item(self.selected_item, 1)
            self.message = "Использовано зелье маны (+50 MP)"
            self.message_timer = 2.0
    
    def update(self, dt):
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""

    def render(self, screen):
        # Фон
        pygame.draw.rect(screen, (30, 30, 40), self.rect)
        pygame.draw.rect(screen, (80, 80, 110), self.rect, 2)
        
        # Заголовок
        title = self.title_font.render("Инвентарь", True, (255, 255, 255))
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Сообщение
        if self.message:
            msg = self.small_font.render(self.message, True, (255, 255, 100))
            screen.blit(msg, (self.rect.x + 10, self.rect.y + 40))
        
        # Список предметов
        y_offset = 50
        items = self.inventory.get_items()
        
        if not items:
            empty_text = self.font.render("Пусто", True, (150, 150, 150))
            screen.blit(empty_text, (self.rect.x + 10, self.rect.y + y_offset))
        else:
            for item_name, count in items.items():
                # Подсветка зелий
                color = (100, 255, 100) if self._is_potion(item_name) else (200, 200, 200)
                text = self.font.render(f"{item_name} ({count}шт)", True, color)
                screen.blit(text, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 30
        
        # Окно подтверждения
        if self.confirm_use:
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, self.rect.topleft)
            
            confirm_text = self.font.render(f"Использовать {self.selected_item}?", True, (255, 255, 255))
            screen.blit(confirm_text, (self.rect.centerx - confirm_text.get_width() // 2, self.rect.centery - 20))
            
            yes_text = self.font.render("Да", True, (100, 255, 100))
            no_text = self.font.render("Нет", True, (255, 100, 100))
            screen.blit(yes_text, (self.rect.centerx - 50, self.rect.centery + 20))
            screen.blit(no_text, (self.rect.centerx + 20, self.rect.centery + 20))