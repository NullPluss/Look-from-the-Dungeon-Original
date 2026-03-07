import pygame
import random
from core.scene import Scene
from world.tile_registry import TileRegistry
from utils.constants import TILE_SIZE

class BattleScene(Scene):
    def __init__(self, game, player, enemy):
        super().__init__(game)
        self.player = player
        self.enemy = enemy
        self.state = "initiative"
        self.font = pygame.font.SysFont("arial", 24)
        self.message = ""
        
        # Позиции для боя (в клетках)
        self.player_cell = 2
        self.enemy_cell = 8
        self.max_cells = 10
        
        w, h = game.window.screen.get_size()
        self.cell_size = min(w // self.max_cells, 100)
        self.start_x = (w - self.cell_size * self.max_cells) // 2
        self.y_pos = h // 2
        
    def on_enter(self):
        self._roll_initiative()
        
    def _roll_initiative(self):
        player_roll = random.randint(1, 20) + self.player.initiative_bonus
        enemy_roll = random.randint(1, 20)
        
        self.message = f"Инициатива: Игрок {player_roll}, Враг {enemy_roll}"
        
        if player_roll >= enemy_roll:
            self.state = "player_turn"
        else:
            self.state = "enemy_turn"
            
    def _is_in_melee_range(self):
        return abs(self.player_cell - self.enemy_cell) <= 1
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "player_turn":
                if event.key == pygame.K_1:
                    if self._is_in_melee_range():
                        self._player_attack(20)
                    else:
                        self.message = "Слишком далеко для ближней атаки!"
                elif event.key == pygame.K_2:
                    self._player_move_closer()
            elif self.state == "victory":
                if event.key == pygame.K_ESCAPE:
                    self.game.scene_manager.pop_scene()
            elif self.state == "defeat":
                if event.key == pygame.K_r:
                    self._restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False
                    
    def _player_attack(self, damage):
        self.enemy.hp -= damage
        self.message = f"Вы нанесли {damage} урона!"
        
        if self.enemy.hp <= 0:
            self.message = "Враг повержен!"
            self.state = "victory"
            for scene in self.game.scene_manager.scene_stack:
                if hasattr(scene, 'dungeon'):
                    scene.dungeon.remove_entity(self.enemy)
                    break
        else:
            self.state = "enemy_turn"
            
    def _player_move_closer(self):
        if self.player_cell < self.enemy_cell:
            self.player_cell += 1
        elif self.player_cell > self.enemy_cell:
            self.player_cell -= 1
        self.message = "Вы подошли ближе"
        self.state = "enemy_turn"
            
    def _enemy_attack(self):
        if self._is_in_melee_range():
            damage = self.enemy.damage
            self.player.hp -= damage
            self.message = f"Враг нанес {damage} урона!"
            
            if self.player.hp <= 0:
                self.message = "Вы погибли!"
                self.state = "defeat"
            else:
                self.state = "player_turn"
        else:
            if self.enemy_cell > self.player_cell:
                self.enemy_cell -= 1
            else:
                self.enemy_cell += 1
            self.message = "Враг подошел ближе"
            self.state = "player_turn"
    
    def _restart_game(self):
        from scenes.main_menu_scene import MainMenuScene
        self.game.scene_manager.scenes.clear()
        self.game.scene_manager.scene_stack.clear()
        self.game.scene_manager.register("main_menu", MainMenuScene(self.game))
        self.game.scene_manager.active_scene = self.game.scene_manager.scenes["main_menu"]
            
    def update(self, dt):
        if self.state == "enemy_turn":
            pygame.time.wait(1000)
            self._enemy_attack()
            
    def render(self, screen):
        screen.fill((20, 20, 30))
        
        # Отрисовка клеток пола
        floor_tile = pygame.transform.scale(TileRegistry.FLOOR, (self.cell_size, self.cell_size))
        for i in range(self.max_cells):
            x = self.start_x + i * self.cell_size
            y = self.y_pos - self.cell_size // 2
            screen.blit(floor_tile, (x, y))
        
        # Отрисовка игрока
        player_x = self.start_x + self.player_cell * self.cell_size + self.cell_size // 2
        player_rect = self.player.image.get_rect(center=(player_x, self.y_pos))
        screen.blit(self.player.image, player_rect)
        
        # Отрисовка врага
        enemy_x = self.start_x + self.enemy_cell * self.cell_size + self.cell_size // 2
        enemy_rect = self.enemy.image.get_rect(center=(enemy_x, self.y_pos))
        screen.blit(self.enemy.image, enemy_rect)
        
        # UI
        title = self.font.render("БОЙ", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))
        
        player_hp = self.font.render(f"Игрок HP: {self.player.hp}/{self.player.max_hp}", True, (255, 255, 255))
        screen.blit(player_hp, (100, 150))
        
        enemy_hp = self.font.render(f"Враг HP: {self.enemy.hp}/{self.enemy.max_hp}", True, (255, 255, 255))
        screen.blit(enemy_hp, (100, 200))
        
        msg = self.font.render(self.message, True, (255, 255, 100))
        screen.blit(msg, (100, 300))
        
        if self.state == "player_turn":
            hint1 = self.font.render("1 - Атака руками (20 урона, ближний бой)", True, (200, 200, 200))
            screen.blit(hint1, (100, 400))
            hint2 = self.font.render("2 - Подойти ближе", True, (200, 200, 200))
            screen.blit(hint2, (100, 430))
            
            range_text = "В БЛИЖНЕМ БОЮ" if self._is_in_melee_range() else "ДАЛЕКО"
            range_color = (100, 255, 100) if self._is_in_melee_range() else (255, 100, 100)
            range_surf = self.font.render(range_text, True, range_color)
            screen.blit(range_surf, (100, 250))
        elif self.state == "victory":
            victory_text = self.font.render("Нажмите ESC для выхода", True, (100, 255, 100))
            screen.blit(victory_text, (100, 450))
        elif self.state == "defeat":
            defeat_title = self.font.render("ПОРАЖЕНИЕ", True, (255, 50, 50))
            screen.blit(defeat_title, (screen.get_width() // 2 - defeat_title.get_width() // 2, screen.get_height() // 2 - 50))
            
            restart_text = self.font.render("R - Начать заново", True, (200, 200, 200))
            screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, screen.get_height() // 2 + 20))
            
            quit_text = self.font.render("ESC - Выйти из игры", True, (200, 200, 200))
            screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, screen.get_height() // 2 + 60))
