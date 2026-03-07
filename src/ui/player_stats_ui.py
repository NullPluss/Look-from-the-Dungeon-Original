import pygame
from ui.base_ui import BaseUI

class PlayerStatsUI(BaseUI):
    def __init__(self, player):
        super().__init__((10, 10, 300, 80))
        self.player = player
        self.font = pygame.font.SysFont("arial", 16)

    def render(self, screen):
        pygame.draw.rect(screen, (20, 20, 30), self.rect)
        pygame.draw.rect(screen, (80, 80, 110), self.rect, 2)
        
        # HP bar
        hp_ratio = self.player.hp / self.player.max_hp
        hp_bar_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 10, 280, 25)
        pygame.draw.rect(screen, (50, 50, 50), hp_bar_rect)
        pygame.draw.rect(screen, (200, 50, 50), (hp_bar_rect.x, hp_bar_rect.y, int(hp_bar_rect.width * hp_ratio), hp_bar_rect.height))
        pygame.draw.rect(screen, (255, 255, 255), hp_bar_rect, 1)
        
        hp_text = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (hp_bar_rect.centerx - hp_text.get_width() // 2, hp_bar_rect.centery - hp_text.get_height() // 2))
        
        # MP bar
        mp_ratio = self.player.mp / self.player.max_mp
        mp_bar_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 45, 280, 25)
        pygame.draw.rect(screen, (50, 50, 50), mp_bar_rect)
        pygame.draw.rect(screen, (50, 50, 200), (mp_bar_rect.x, mp_bar_rect.y, int(mp_bar_rect.width * mp_ratio), mp_bar_rect.height))
        pygame.draw.rect(screen, (255, 255, 255), mp_bar_rect, 1)
        
        mp_text = self.font.render(f"MP: {self.player.mp}/{self.player.max_mp}", True, (255, 255, 255))
        screen.blit(mp_text, (mp_bar_rect.centerx - mp_text.get_width() // 2, mp_bar_rect.centery - mp_text.get_height() // 2))
