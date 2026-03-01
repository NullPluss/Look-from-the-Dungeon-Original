import pygame
from ui.base_ui import BaseUI

class PauseMenu(BaseUI):
    def __init__(self, screen_size):
        w, h = screen_size
        super().__init__((0, 0, w, h))
        self.font = pygame.font.SysFont("arial", 32)
        self.small_font = pygame.font.SysFont("arial", 24)
        self.selected = 0
        self.options = ["Продолжить", "Выйти"]
        self.confirm_exit = False
        self.on_resume = None
        self.on_quit = None
        
        # Создаем прямоугольники для кликабельных областей
        self.option_rects = []
        for i in range(len(self.options)):
            y = h // 2 + i * 60
            text_surf = self.font.render(self.options[i], True, (255, 255, 255))
            rect = pygame.Rect(w // 2 - text_surf.get_width() // 2, y, text_surf.get_width(), text_surf.get_height())
            self.option_rects.append(rect)
        
        # Прямоугольники для подтверждения
        self.yes_rect = pygame.Rect(w // 2 - 50, h // 2 + 20, 100, 30)
        self.no_rect = pygame.Rect(w // 2 - 50, h // 2 + 60, 100, 30)

    def handle_event(self, event):
        pos = event.pos if hasattr(event, 'pos') else pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEMOTION:
            if not self.confirm_exit:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        self.selected = i
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.confirm_exit:
                if self.yes_rect.collidepoint(pos):
                    if self.on_quit:
                        self.on_quit()
                elif self.no_rect.collidepoint(pos):
                    self.confirm_exit = False
            else:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        if i == 0:
                            if self.on_resume:
                                self.on_resume()
                        elif i == 1:
                            self.confirm_exit = True
        
        elif event.type == pygame.KEYDOWN:
            if self.confirm_exit:
                if event.key == pygame.K_y:
                    if self.on_quit:
                        self.on_quit()
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    self.confirm_exit = False
            else:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected == 0:
                        if self.on_resume:
                            self.on_resume()
                    elif self.selected == 1:
                        self.confirm_exit = True
                elif event.key == pygame.K_ESCAPE:
                    if self.on_resume:
                        self.on_resume()

    def render(self, screen):
        overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        if self.confirm_exit:
            text = self.font.render("Выйти из игры?", True, (255, 255, 255))
            screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - 60))
            
            yes_text = self.small_font.render("Y - Да", True, (255, 255, 255))
            no_text = self.small_font.render("N - Нет", True, (255, 255, 255))
            screen.blit(yes_text, (self.rect.centerx - yes_text.get_width() // 2, self.rect.centery + 20))
            screen.blit(no_text, (self.rect.centerx - no_text.get_width() // 2, self.rect.centery + 60))
        else:
            title = self.font.render("ПАУЗА", True, (255, 255, 255))
            screen.blit(title, (self.rect.centerx - title.get_width() // 2, self.rect.centery - 100))

            for i, option in enumerate(self.options):
                color = (255, 255, 100) if i == self.selected else (200, 200, 200)
                text = self.font.render(option, True, color)
                y = self.rect.centery + i * 60
                screen.blit(text, (self.rect.centerx - text.get_width() // 2, y))
