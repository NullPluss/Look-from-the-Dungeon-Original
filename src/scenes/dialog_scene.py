import pygame
import random
from core.scene import Scene

class DialogScene(Scene):
    def __init__(self, game, npc):
        super().__init__(game)
        self.npc = npc
        self.font = pygame.font.SysFont("arial", 20)
        self.title_font = pygame.font.SysFont("arial", 28)
        self.state = "greeting"  # greeting, quest_check, diplomacy, trade, joined
        self.message = ""
        
    def on_enter(self):
        if self.npc.in_party:
            self.state = "already_in_party"
            self.message = f"{self.npc.name} уже в вашей команде."
        elif self.npc.quest_completed:
            if self.npc.can_recruit:
                self.state = "diplomacy_offer"
                self.message = "Спасибо! Теперь я могу присоединиться к вам или торговать."
            else:
                self.state = "trade"
        else:
            self.state = "greeting"
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.scene_manager.pop_scene()
            elif event.key == pygame.K_1:
                if self.state == "greeting":
                    self._check_quest()
                elif self.state == "diplomacy_offer":
                    self._try_diplomacy()
                elif self.state == "trade":
                    self._open_trade()
            elif event.key == pygame.K_2:
                if self.state == "greeting":
                    self._open_trade()
                elif self.state == "diplomacy_offer":
                    self._open_trade()
                elif self.state == "trade":
                    self.game.scene_manager.pop_scene()
            elif event.key == pygame.K_3:
                if self.state == "greeting" or self.state == "diplomacy_offer":
                    self.game.scene_manager.pop_scene()
                    
    def _check_quest(self):
        has_item = self.game.party.inventory.items.get(self.npc.quest_item, 0) > 0
        
        if has_item:
            self.game.party.inventory.remove_item(self.npc.quest_item, 1)
            self.npc.quest_completed = True
            self.state = "diplomacy_offer"
            self.message = f"Спасибо! Теперь я могу присоединиться к вам или торговать."
        else:
            self.state = "quest_active"
            self.message = f"Принесите мне {self.npc.quest_item}, и я помогу вам."
            
    def _try_diplomacy(self):
        party_size = len(self.game.party.members)
        roll = random.randint(1, 20) + party_size
        
        if roll > 11:
            if len(self.game.party.members) < 4:
                self.game.party.add_member(self.npc)
                self.npc.in_party = True
                self.state = "joined"
                self.message = f"{self.npc.name} присоединился к вашей команде! (Бросок: {roll})"
            else:
                self.state = "party_full"
                self.message = "Ваша команда уже полна (максимум 4 человека)."
        else:
            self.npc.can_recruit = False
            self.state = "diplomacy_failed"
            self.message = f"Не удалось уговорить. Теперь доступна только торговля. (Бросок: {roll})"
    
    def _open_trade(self):
        from scenes.trade_scene import TradeScene
        trade = TradeScene(self.game, self.npc)
        self.game.scene_manager.register("trade", trade)
        self.game.scene_manager.push_scene("trade")
            
    def render(self, screen):
        # Затемнение фона
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Диалоговое окно
        w, h = screen.get_size()
        dialog_rect = pygame.Rect(w // 4, h // 4, w // 2, h // 2)
        pygame.draw.rect(screen, (40, 40, 50), dialog_rect)
        pygame.draw.rect(screen, (100, 100, 120), dialog_rect, 3)
        
        # Имя НПС
        name_text = self.title_font.render(self.npc.name, True, (255, 255, 100))
        screen.blit(name_text, (dialog_rect.centerx - name_text.get_width() // 2, dialog_rect.y + 20))
        
        # Диалог
        y_offset = dialog_rect.y + 70
        
        if self.state == "greeting":
            dialogue = self.font.render(self.npc.dialogue, True, (255, 255, 255))
            screen.blit(dialogue, (dialog_rect.x + 20, y_offset))
            
            option1 = self.font.render("1 - Отдать предмет", True, (200, 200, 200))
            screen.blit(option1, (dialog_rect.x + 20, y_offset + 60))
            
            option2 = self.font.render("2 - Торговать", True, (200, 200, 200))
            screen.blit(option2, (dialog_rect.x + 20, y_offset + 90))
            
            option3 = self.font.render("3 - Уйти", True, (200, 200, 200))
            screen.blit(option3, (dialog_rect.x + 20, y_offset + 120))
            
        elif self.state == "quest_active":
            msg = self.font.render(self.message, True, (255, 200, 100))
            screen.blit(msg, (dialog_rect.x + 20, y_offset))
            
            hint = self.font.render("ESC - Закрыть", True, (150, 150, 150))
            screen.blit(hint, (dialog_rect.x + 20, y_offset + 60))
            
        elif self.state == "diplomacy_offer":
            msg = self.font.render(self.message, True, (100, 255, 100))
            screen.blit(msg, (dialog_rect.x + 20, y_offset))
            
            option1 = self.font.render("1 - Пригласить в команду", True, (200, 200, 200))
            screen.blit(option1, (dialog_rect.x + 20, y_offset + 60))
            
            option2 = self.font.render("2 - Торговать", True, (200, 200, 200))
            screen.blit(option2, (dialog_rect.x + 20, y_offset + 90))
            
            option3 = self.font.render("3 - Уйти", True, (200, 200, 200))
            screen.blit(option3, (dialog_rect.x + 20, y_offset + 120))
            
        elif self.state == "joined":
            msg = self.font.render(self.message, True, (100, 255, 100))
            screen.blit(msg, (dialog_rect.x + 20, y_offset))
            
            hint = self.font.render("ESC - Закрыть", True, (150, 150, 150))
            screen.blit(hint, (dialog_rect.x + 20, y_offset + 60))
            
        elif self.state == "diplomacy_failed":
            msg = self.font.render(self.message, True, (255, 100, 100))
            screen.blit(msg, (dialog_rect.x + 20, y_offset))
            
            hint = self.font.render("ESC - Закрыть", True, (150, 150, 150))
            screen.blit(hint, (dialog_rect.x + 20, y_offset + 60))
            
        elif self.state == "trade":
            msg = self.font.render("Торговля доступна.", True, (200, 200, 200))
            screen.blit(msg, (dialog_rect.x + 20, y_offset))
            
            option1 = self.font.render("1 - Открыть торговлю", True, (200, 200, 200))
            screen.blit(option1, (dialog_rect.x + 20, y_offset + 40))
            
            option2 = self.font.render("2 - Уйти", True, (200, 200, 200))
            screen.blit(option2, (dialog_rect.x + 20, y_offset + 70))
            
        elif self.state == "already_in_party":
            msg = self.font.render(self.message, True, (200, 200, 200))
            screen.blit(msg, (dialog_rect.x + 20, y_offset))
            
            hint = self.font.render("ESC - Закрыть", True, (150, 150, 150))
            screen.blit(hint, (dialog_rect.x + 20, y_offset + 60))
            
        elif self.state == "party_full":
            msg = self.font.render(self.message, True, (255, 200, 100))
            screen.blit(msg, (dialog_rect.x + 20, y_offset))
            
            hint = self.font.render("ESC - Закрыть", True, (150, 150, 150))
            screen.blit(hint, (dialog_rect.x + 20, y_offset + 60))
