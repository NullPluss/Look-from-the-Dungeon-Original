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
        self.small_font = pygame.font.SysFont("arial", 16)
        self.message = ""
        
        # Поле боя 15x15
        self.grid_width = 15
        self.grid_height = 15
        
        w, h = game.window.screen.get_size()
        self.cell_size = min(w // self.grid_width, h // self.grid_height, 60)
        self.start_x = (w - self.cell_size * self.grid_width) // 2
        self.start_y = (h - self.cell_size * self.grid_height) // 2
        
        # Позиции в клетках (x, y)
        self.player_cell = [2, 7]
        self.enemy_cell = [12, 7]
        
        # Система действий
        self.actions_left = 2
        self.max_actions = 2
        
        self.loot_message = ""
        
        # Масштабирование ассетов под размер клетки
        self.player_image = self._scale_to_cell(self.player.image)
        self.enemy_image = self._scale_to_cell(self.enemy.image)
        
        # Генерация случайной сетки пола
        self.floor_grid = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                floor_tile = pygame.transform.scale(TileRegistry.get_random_floor(), (self.cell_size, self.cell_size))
                row.append(floor_tile)
            self.floor_grid.append(row)
        
    def _scale_to_cell(self, image):
        """Масштабирует изображение под размер клетки сохраняя пропорции"""
        img_w, img_h = image.get_size()
        aspect_ratio = img_w / img_h
        
        if aspect_ratio > 1:
            new_w = self.cell_size
            new_h = int(self.cell_size / aspect_ratio)
        else:
            new_h = self.cell_size
            new_w = int(self.cell_size * aspect_ratio)
        
        return pygame.transform.smoothscale(image, (new_w, new_h))
        
    def on_enter(self):
        self._roll_initiative()
        
    def _roll_initiative(self):
        player_roll = random.randint(1, 20) + self.player.initiative_bonus
        enemy_roll = random.randint(1, 20)
        
        self.message = f"Инициатива: Игрок {player_roll}, Враг {enemy_roll}"
        
        if player_roll >= enemy_roll:
            self.state = "player_turn"
            self.actions_left = self.max_actions
        else:
            self.state = "enemy_turn"
            
    def _is_in_melee_range(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1 and pos1 != pos2
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "player_turn" and self.actions_left > 0:
                moved = False
                if event.key == pygame.K_w and self.player_cell[1] > 0:
                    self.player_cell[1] -= 1
                    moved = True
                elif event.key == pygame.K_s and self.player_cell[1] < self.grid_height - 1:
                    self.player_cell[1] += 1
                    moved = True
                elif event.key == pygame.K_a and self.player_cell[0] > 0:
                    self.player_cell[0] -= 1
                    moved = True
                elif event.key == pygame.K_d and self.player_cell[0] < self.grid_width - 1:
                    self.player_cell[0] += 1
                    moved = True
                elif event.key == pygame.K_1:
                    # Атака руками
                    if self._is_in_melee_range(self.player_cell, self.enemy_cell):
                        self._player_attack(20)
                    else:
                        self.message = "Слишком далеко для ближней атаки!"
                elif event.key == pygame.K_2:
                    # Атака мечом
                    if self._has_item("Меч"):
                        if self._is_in_melee_range(self.player_cell, self.enemy_cell):
                            self._player_attack(50)
                        else:
                            self.message = "Слишком далеко для атаки мечом!"
                    else:
                        self.message = "У вас нет меча!"
                elif event.key == pygame.K_3:
                    # Атака арбалетом
                    if self._has_item("Арбалет") and self._has_item("Арбалетные болты"):
                        distance = abs(self.player_cell[0] - self.enemy_cell[0]) + abs(self.player_cell[1] - self.enemy_cell[1])
                        if distance <= 6:
                            self._player_attack(50)
                            self._use_item("Арбалетные болты", 1)
                        else:
                            self.message = "Слишком далеко для выстрела!"
                    else:
                        self.message = "Нужен арбалет и болты!"
                elif event.key == pygame.K_4:
                    # Атака свитком огненного шара
                    if self._has_item("Свиток огненного шара"):
                        if self.player.mp >= 50:
                            distance = abs(self.player_cell[0] - self.enemy_cell[0]) + abs(self.player_cell[1] - self.enemy_cell[1])
                            if distance <= 4:
                                self._player_attack(100)
                                self.player.mp -= 50
                                self._use_item("Свиток огненного шара", 1)
                            else:
                                self.message = "Слишком далеко для огненного шара!"
                        else:
                            self.message = "Недостаточно маны!"
                    else:
                        self.message = "У вас нет свитка!"
                elif event.key == pygame.K_SPACE:
                    self._end_turn()
                    
                if moved:
                    self.actions_left -= 1
                    self.message = f"Движение. Осталось действий: {self.actions_left}"
                    if self.actions_left == 0:
                        self._end_turn()
                        
            elif self.state == "victory":
                if event.key == pygame.K_ESCAPE:
                    self.game.scene_manager.pop_scene()
            elif self.state == "defeat":
                if event.key == pygame.K_r:
                    self._restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False
    
    def _has_item(self, item_name):
        return self.game.party.inventory.items.get(item_name, 0) > 0
    
    def _use_item(self, item_name, count):
        self.game.party.inventory.remove_item(item_name, count)
                    
    def _player_attack(self, damage):
        self.enemy.hp -= damage
        self.actions_left -= 1
        self.message = f"Вы нанесли {damage} урона! Осталось действий: {self.actions_left}"
        
        if self.enemy.hp <= 0:
            self.message = f"{self.enemy.name} повержен!"
            self.state = "victory"
            
            # Добавление лута в инвентарь
            for item in self.enemy.loot:
                count = self.enemy.monster_type.get("loot_counts", {}).get(item, 1)
                self.game.party.inventory.add_item(item, count)
            
            # Сообщение о полученных предметах
            loot_items = []
            for item in self.enemy.loot:
                count = self.enemy.monster_type.get("loot_counts", {}).get(item, 1)
                if count > 1:
                    loot_items.append(f"{item} ({count}шт)")
                else:
                    loot_items.append(item)
            loot_msg = ", ".join(loot_items)
            self.loot_message = f"Получено: {loot_msg}"
            
            for scene in self.game.scene_manager.scene_stack:
                if hasattr(scene, 'dungeon'):
                    scene.dungeon.remove_entity(self.enemy)
                    break
        elif self.actions_left == 0:
            self._end_turn()
            
    def _end_turn(self):
        self.state = "enemy_turn"
        self.actions_left = 0
        
    def _enemy_turn(self):
        # AI монстра в зависимости от типа атаки
        distance = abs(self.player_cell[0] - self.enemy_cell[0]) + abs(self.player_cell[1] - self.enemy_cell[1])
        
        if self.enemy.attack_type == "melee":
            # Ближний бой - приближаться и атаковать
            if self._is_in_melee_range(self.player_cell, self.enemy_cell):
                self._enemy_attack()
            else:
                self._enemy_move_closer()
        else:
            # Дальний бой
            if self._is_in_melee_range(self.player_cell, self.enemy_cell):
                # Слишком близко - отходить
                self._enemy_move_away()
            elif distance <= self.enemy.attack_range:
                # В пределах дальности - атаковать
                if self.enemy.mp >= self.enemy.mp_cost:
                    self._enemy_attack()
                else:
                    # Нет маны - отходить
                    self._enemy_move_away()
            else:
                # Вне дальности - приближаться
                self._enemy_move_closer()
    
    def _enemy_attack(self):
        damage = self.enemy.damage
        self.player.hp -= damage
        
        if self.enemy.mp_cost > 0:
            self.enemy.mp -= self.enemy.mp_cost
            self.message = f"{self.enemy.name} нанес {damage} урона! (MP: {self.enemy.mp}/{self.enemy.max_mp})"
        else:
            self.message = f"{self.enemy.name} нанес {damage} урона!"
        
        if self.player.hp <= 0:
            self.message = "Вы погибли!"
            self.state = "defeat"
        else:
            self.state = "player_turn"
            self.actions_left = self.max_actions
    
    def _enemy_move_closer(self):
        dx = self.player_cell[0] - self.enemy_cell[0]
        dy = self.player_cell[1] - self.enemy_cell[1]
        
        if abs(dx) > abs(dy):
            if dx > 0:
                self.enemy_cell[0] += 1
            else:
                self.enemy_cell[0] -= 1
        else:
            if dy > 0:
                self.enemy_cell[1] += 1
            else:
                self.enemy_cell[1] -= 1
                
        self.message = f"{self.enemy.name} подошел ближе"
        self.state = "player_turn"
        self.actions_left = self.max_actions
    
    def _enemy_move_away(self):
        dx = self.player_cell[0] - self.enemy_cell[0]
        dy = self.player_cell[1] - self.enemy_cell[1]
        
        # Отходить в противоположную сторону
        if abs(dx) > abs(dy):
            if dx > 0 and self.enemy_cell[0] > 0:
                self.enemy_cell[0] -= 1
            elif dx < 0 and self.enemy_cell[0] < self.grid_width - 1:
                self.enemy_cell[0] += 1
        else:
            if dy > 0 and self.enemy_cell[1] > 0:
                self.enemy_cell[1] -= 1
            elif dy < 0 and self.enemy_cell[1] < self.grid_height - 1:
                self.enemy_cell[1] += 1
                
        self.message = f"{self.enemy.name} отошел"
        self.state = "player_turn"
        self.actions_left = self.max_actions
    
    def _restart_game(self):
        from scenes.main_menu_scene import MainMenuScene
        self.game.scene_manager.scenes.clear()
        self.game.scene_manager.scene_stack.clear()
        self.game.scene_manager.register("main_menu", MainMenuScene(self.game))
        self.game.scene_manager.active_scene = self.game.scene_manager.scenes["main_menu"]
            
    def update(self, dt):
        if self.state == "enemy_turn":
            pygame.time.wait(500)
            self._enemy_turn()
            
    def render(self, screen):
        screen.fill((20, 20, 30))
        
        # Отрисовка сетки клеток
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                px = self.start_x + x * self.cell_size
                py = self.start_y + y * self.cell_size
                screen.blit(self.floor_grid[y][x], (px, py))
        
        # Отрисовка игрока
        player_x = self.start_x + self.player_cell[0] * self.cell_size + self.cell_size // 2
        player_y = self.start_y + self.player_cell[1] * self.cell_size + self.cell_size // 2
        player_rect = self.player_image.get_rect(center=(player_x, player_y))
        screen.blit(self.player_image, player_rect)
        
        # Отрисовка врага
        enemy_x = self.start_x + self.enemy_cell[0] * self.cell_size + self.cell_size // 2
        enemy_y = self.start_y + self.enemy_cell[1] * self.cell_size + self.cell_size // 2
        enemy_rect = self.enemy_image.get_rect(center=(enemy_x, enemy_y))
        screen.blit(self.enemy_image, enemy_rect)
        
        # UI
        title = self.font.render("БОЙ", True, (255, 255, 255))
        screen.blit(title, (20, 20))
        
        # Имя и HP врага
        enemy_name = self.small_font.render(self.enemy.name, True, (255, 200, 100))
        screen.blit(enemy_name, (20, 60))
        
        enemy_hp_text = self.small_font.render(f"HP: {self.enemy.hp}/{self.enemy.max_hp}", True, (255, 255, 255))
        screen.blit(enemy_hp_text, (20, 85))
        
        # Шкала здоровья врага
        hp_bar_width = 200
        hp_ratio = self.enemy.hp / self.enemy.max_hp
        pygame.draw.rect(screen, (50, 50, 50), (20, 110, hp_bar_width, 15))
        pygame.draw.rect(screen, (200, 50, 50), (20, 110, int(hp_bar_width * hp_ratio), 15))
        pygame.draw.rect(screen, (255, 255, 255), (20, 110, hp_bar_width, 15), 1)
        
        player_hp = self.small_font.render(f"Игрок HP: {self.player.hp}/{self.player.max_hp}", True, (255, 255, 255))
        screen.blit(player_hp, (20, 135))
        
        if self.state == "player_turn":
            actions_text = self.small_font.render(f"Действий: {self.actions_left}/{self.max_actions}", True, (100, 255, 100))
            screen.blit(actions_text, (20, 160))
        
        msg = self.small_font.render(self.message, True, (255, 255, 100))
        screen.blit(msg, (20, 185))
        
        if self.state == "player_turn":
            hint1 = self.small_font.render("WASD - движение (1 действие)", True, (200, 200, 200))
            screen.blit(hint1, (20, screen.get_height() - 140))
            
            # Доступные атаки
            y_offset = screen.get_height() - 115
            hint2 = self.small_font.render("1 - Руки (20 урона, ближний)", True, (200, 200, 200))
            screen.blit(hint2, (20, y_offset))
            y_offset += 20
            
            if self._has_item("Меч"):
                hint3 = self.small_font.render("2 - Меч (75 урона, ближний)", True, (100, 255, 100))
                screen.blit(hint3, (20, y_offset))
                y_offset += 20
            
            if self._has_item("Арбалет") and self._has_item("Арбалетные болты"):
                bolts = self.game.party.inventory.items.get("Арбалетные болты", 0)
                hint4 = self.small_font.render(f"3 - Арбалет (50 урона, 6 клеток, болтов: {bolts})", True, (100, 255, 100))
                screen.blit(hint4, (20, y_offset))
                y_offset += 20
            
            if self._has_item("Свиток огненного шара"):
                hint5 = self.small_font.render("4 - Огненный шар (100 урона, 4 клетки, 50 MP)", True, (100, 255, 100))
                screen.blit(hint5, (20, y_offset))
                y_offset += 20
            
            hint_space = self.small_font.render("SPACE - Закончить ход", True, (200, 200, 200))
            screen.blit(hint_space, (20, y_offset))
            
            range_text = "В БЛИЖНЕМ БОЮ" if self._is_in_melee_range(self.player_cell, self.enemy_cell) else "ДАЛЕКО"
            range_color = (100, 255, 100) if self._is_in_melee_range(self.player_cell, self.enemy_cell) else (255, 100, 100)
            range_surf = self.small_font.render(range_text, True, range_color)
            screen.blit(range_surf, (20, 210))
        elif self.state == "victory":
            victory_text = self.font.render("Нажмите ESC для выхода", True, (100, 255, 100))
            screen.blit(victory_text, (screen.get_width() // 2 - victory_text.get_width() // 2, screen.get_height() // 2))
            if self.loot_message:
                loot_text = self.small_font.render(self.loot_message, True, (255, 255, 100))
                screen.blit(loot_text, (screen.get_width() // 2 - loot_text.get_width() // 2, screen.get_height() // 2 + 40))
        elif self.state == "defeat":
            defeat_title = self.font.render("ПОРАЖЕНИЕ", True, (255, 50, 50))
            screen.blit(defeat_title, (screen.get_width() // 2 - defeat_title.get_width() // 2, screen.get_height() // 2 - 50))
            
            restart_text = self.small_font.render("R - Начать заново", True, (200, 200, 200))
            screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, screen.get_height() // 2 + 20))
            
            quit_text = self.small_font.render("ESC - Выйти из игры", True, (200, 200, 200))
            screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, screen.get_height() // 2 + 60))
