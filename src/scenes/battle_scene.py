import pygame
import random
from core.scene import Scene
from world.tile_registry import TileRegistry
from utils.constants import TILE_SIZE

class BattleScene(Scene):
    def __init__(self, game, player, enemy):
        super().__init__(game)
        self.player = player
        self.party = game.party.members
        self.enemies = [enemy]
        self.state = "party_turn"
        self.font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 16)
        self.message = ""
        
        self.grid_width = 15
        self.grid_height = 15
        
        w, h = game.window.screen.get_size()
        self.cell_size = min(w // self.grid_width, h // self.grid_height, 60)
        self.start_x = (w - self.cell_size * self.grid_width) // 2
        self.start_y = (h - self.cell_size * self.grid_height) // 2
        
        self.positions = {}
        self._setup_positions()
        
        self.current_character_index = 0
        self.current_character = self.party[0]
        self.actions_left = 2
        self.max_actions = 2
        
        self.loot_message = ""
        
        self.scaled_images = {}
        for member in self.party:
            self.scaled_images[member] = self._scale_to_cell(member.image)
        for enemy in self.enemies:
            self.scaled_images[enemy] = self._scale_to_cell(enemy.image)
        
        self.floor_grid = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                floor_tile = pygame.transform.scale(TileRegistry.get_random_floor(), (self.cell_size, self.cell_size))
                row.append(floor_tile)
            self.floor_grid.append(row)
    
    def _setup_positions(self):
        for i, member in enumerate(self.party):
            self.positions[member] = [2, 5 + i * 2]
        for i, enemy in enumerate(self.enemies):
            self.positions[enemy] = [12, 7]
        
    def _scale_to_cell(self, image):
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
        self.message = f"Ход: {self.current_character.name}"
        
    def _is_in_melee_range(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1 and pos1 != pos2
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "party_turn" and self.actions_left > 0:
                moved = False
                char_pos = self.positions[self.current_character]
                
                if event.key == pygame.K_w and char_pos[1] > 0:
                    char_pos[1] -= 1
                    moved = True
                elif event.key == pygame.K_s and char_pos[1] < self.grid_height - 1:
                    char_pos[1] += 1
                    moved = True
                elif event.key == pygame.K_a and char_pos[0] > 0:
                    char_pos[0] -= 1
                    moved = True
                elif event.key == pygame.K_d and char_pos[0] < self.grid_width - 1:
                    char_pos[0] += 1
                    moved = True
                elif event.key == pygame.K_1:
                    self._try_attack(20, "melee", 0, 0, "Руки")
                elif event.key == pygame.K_2:
                    if self._has_item("Меч"):
                        self._try_attack(75, "melee", 0, 0, "Меч")
                    else:
                        self.message = "У вас нет меча!"
                elif event.key == pygame.K_3:
                    if self._has_item("Арбалет") and self._has_item("Арбалетные болты"):
                        if self._try_attack(50, "ranged", 6, 0, "Арбалет"):
                            self._use_item("Арбалетные болты", 1)
                    else:
                        self.message = "Нужен арбалет и болты!"
                elif event.key == pygame.K_4:
                    if self._has_item("Свиток огненного шара"):
                        if self.current_character.mp >= 50:
                            if self._try_attack(100, "ranged", 4, 50, "Огненный шар"):
                                self._use_item("Свиток огненного шара", 1)
                        else:
                            self.message = "Недостаточно маны!"
                    else:
                        self.message = "У вас нет свитка!"
                elif event.key == pygame.K_SPACE:
                    self._next_character()
                    
                if moved:
                    self.actions_left -= 1
                    self.message = f"{self.current_character.name}: Движение. Осталось: {self.actions_left}"
                    if self.actions_left == 0:
                        self._next_character()
                        
            elif self.state == "victory":
                if event.key == pygame.K_ESCAPE:
                    self.game.scene_manager.pop_scene()
            elif self.state == "defeat":
                if event.key == pygame.K_r:
                    self._restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False
    
    def _try_attack(self, damage, attack_type, max_range, mp_cost, weapon_name):
        char_pos = self.positions[self.current_character]
        enemy = self.enemies[0]
        enemy_pos = self.positions[enemy]
        
        if attack_type == "melee":
            if not self._is_in_melee_range(char_pos, enemy_pos):
                self.message = "Слишком далеко для ближней атаки!"
                return False
        else:
            distance = abs(char_pos[0] - enemy_pos[0]) + abs(char_pos[1] - enemy_pos[1])
            if distance > max_range:
                self.message = f"Слишком далеко! (макс. {max_range} клеток)"
                return False
        
        enemy.hp -= damage
        if mp_cost > 0:
            self.current_character.mp -= mp_cost
        self.actions_left -= 1
        self.message = f"{self.current_character.name} ({weapon_name}): {damage} урона! Осталось: {self.actions_left}"
        
        if enemy.hp <= 0:
            self._victory()
        elif self.actions_left == 0:
            self._next_character()
        
        return True
    
    def _next_character(self):
        self.current_character_index += 1
        if self.current_character_index >= len(self.party):
            self.state = "enemy_turn"
            self.actions_left = 0
        else:
            self.current_character = self.party[self.current_character_index]
            self.actions_left = self.max_actions
            self.message = f"Ход: {self.current_character.name}"
    
    def _victory(self):
        enemy = self.enemies[0]
        self.message = f"{enemy.name} повержен!"
        self.state = "victory"
        
        for item in enemy.loot:
            count = enemy.monster_type.get("loot_counts", {}).get(item, 1)
            self.game.party.inventory.add_item(item, count)
        
        loot_items = []
        for item in enemy.loot:
            count = enemy.monster_type.get("loot_counts", {}).get(item, 1)
            loot_items.append(f"{item} ({count}шт)" if count > 1 else item)
        self.loot_message = f"Получено: {', '.join(loot_items)}"
        
        for scene in self.game.scene_manager.scene_stack:
            if hasattr(scene, 'dungeon'):
                scene.dungeon.remove_entity(enemy)
                break
    
    def _has_item(self, item_name):
        return self.game.party.inventory.items.get(item_name, 0) > 0
    
    def _use_item(self, item_name, count):
        self.game.party.inventory.remove_item(item_name, count)
            
    def _enemy_turn(self):
        enemy = self.enemies[0]
        enemy_pos = self.positions[enemy]
        
        closest_target = min(self.party, key=lambda m: abs(self.positions[m][0] - enemy_pos[0]) + abs(self.positions[m][1] - enemy_pos[1]))
        target_pos = self.positions[closest_target]
        distance = abs(target_pos[0] - enemy_pos[0]) + abs(target_pos[1] - enemy_pos[1])
        
        if enemy.attack_type == "melee":
            if self._is_in_melee_range(target_pos, enemy_pos):
                self._enemy_attack(enemy, closest_target)
            else:
                self._enemy_move_towards(enemy_pos, target_pos, enemy.name)
        else:
            if self._is_in_melee_range(target_pos, enemy_pos):
                self._enemy_move_away(enemy_pos, target_pos, enemy.name)
            elif distance <= enemy.attack_range and enemy.mp >= enemy.mp_cost:
                self._enemy_attack(enemy, closest_target)
            elif distance <= enemy.attack_range:
                self._enemy_move_away(enemy_pos, target_pos, enemy.name)
            else:
                self._enemy_move_towards(enemy_pos, target_pos, enemy.name)
    
    def _enemy_attack(self, enemy, target):
        damage = enemy.damage
        target.hp -= damage
        
        if enemy.mp_cost > 0:
            enemy.mp -= enemy.mp_cost
            self.message = f"{enemy.name} атакует {target.name}: {damage} урона!"
        else:
            self.message = f"{enemy.name} атакует {target.name}: {damage} урона!"
        
        if self.player.hp <= 0:
            self.message = "Вы погибли!"
            self.state = "defeat"
        else:
            self.current_character_index = 0
            self.current_character = self.party[0]
            self.actions_left = self.max_actions
            self.state = "party_turn"
    
    def _enemy_move_towards(self, enemy_pos, target_pos, name):
        dx = target_pos[0] - enemy_pos[0]
        dy = target_pos[1] - enemy_pos[1]
        
        if abs(dx) > abs(dy):
            enemy_pos[0] += 1 if dx > 0 else -1
        else:
            enemy_pos[1] += 1 if dy > 0 else -1
        
        self.message = f"{name} подошел ближе"
        self.current_character_index = 0
        self.current_character = self.party[0]
        self.actions_left = self.max_actions
        self.state = "party_turn"
    
    def _enemy_move_away(self, enemy_pos, target_pos, name):
        dx = target_pos[0] - enemy_pos[0]
        dy = target_pos[1] - enemy_pos[1]
        
        if abs(dx) > abs(dy):
            if dx > 0 and enemy_pos[0] > 0:
                enemy_pos[0] -= 1
            elif dx < 0 and enemy_pos[0] < self.grid_width - 1:
                enemy_pos[0] += 1
        else:
            if dy > 0 and enemy_pos[1] > 0:
                enemy_pos[1] -= 1
            elif dy < 0 and enemy_pos[1] < self.grid_height - 1:
                enemy_pos[1] += 1
        
        self.message = f"{name} отошел"
        self.current_character_index = 0
        self.current_character = self.party[0]
        self.actions_left = self.max_actions
        self.state = "party_turn"
    
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
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                px = self.start_x + x * self.cell_size
                py = self.start_y + y * self.cell_size
                screen.blit(self.floor_grid[y][x], (px, py))
        
        # Отрисовка всех членов партии
        for member in self.party:
            pos = self.positions[member]
            mx = self.start_x + pos[0] * self.cell_size + self.cell_size // 2
            my = self.start_y + pos[1] * self.cell_size + self.cell_size // 2
            img = self.scaled_images[member]
            rect = img.get_rect(center=(mx, my))
            screen.blit(img, rect)
            
            # Подсветка активного персонажа
            if member == self.current_character and self.state == "party_turn":
                pygame.draw.rect(screen, (100, 255, 100), (self.start_x + pos[0] * self.cell_size, self.start_y + pos[1] * self.cell_size, self.cell_size, self.cell_size), 3)
        
        # Отрисовка врагов
        for enemy in self.enemies:
            pos = self.positions[enemy]
            ex = self.start_x + pos[0] * self.cell_size + self.cell_size // 2
            ey = self.start_y + pos[1] * self.cell_size + self.cell_size // 2
            img = self.scaled_images[enemy]
            rect = img.get_rect(center=(ex, ey))
            screen.blit(img, rect)
        
        # UI
        title = self.font.render("БОЙ", True, (255, 255, 255))
        screen.blit(title, (20, 20))
        
        enemy = self.enemies[0]
        enemy_name = self.small_font.render(enemy.name, True, (255, 200, 100))
        screen.blit(enemy_name, (20, 60))
        
        enemy_hp_text = self.small_font.render(f"HP: {enemy.hp}/{enemy.max_hp}", True, (255, 255, 255))
        screen.blit(enemy_hp_text, (20, 85))
        
        hp_bar_width = 200
        hp_ratio = max(0, enemy.hp / enemy.max_hp)
        pygame.draw.rect(screen, (50, 50, 50), (20, 110, hp_bar_width, 15))
        pygame.draw.rect(screen, (200, 50, 50), (20, 110, int(hp_bar_width * hp_ratio), 15))
        pygame.draw.rect(screen, (255, 255, 255), (20, 110, hp_bar_width, 15), 1)
        
        # Информация о текущем персонаже
        y_offset = 140
        char_name = self.small_font.render(f"Ход: {self.current_character.name}", True, (100, 255, 255))
        screen.blit(char_name, (20, y_offset))
        y_offset += 25
        
        char_hp = self.small_font.render(f"HP: {self.current_character.hp}/{self.current_character.max_hp}", True, (255, 255, 255))
        screen.blit(char_hp, (20, y_offset))
        y_offset += 20
        
        char_mp = self.small_font.render(f"MP: {self.current_character.mp}/{self.current_character.max_mp}", True, (100, 200, 255))
        screen.blit(char_mp, (20, y_offset))
        y_offset += 20
        
        if self.state == "party_turn":
            actions_text = self.small_font.render(f"Действий: {self.actions_left}/{self.max_actions}", True, (100, 255, 100))
            screen.blit(actions_text, (20, y_offset))
            y_offset += 25
        
        msg = self.small_font.render(self.message, True, (255, 255, 100))
        screen.blit(msg, (20, y_offset))
        
        if self.state == "party_turn":
            hint_y = screen.get_height() - 140
            hint1 = self.small_font.render("WASD - движение", True, (200, 200, 200))
            screen.blit(hint1, (20, hint_y))
            hint_y += 20
            
            hint2 = self.small_font.render("1-Руки(20) 2-Меч(75)", True, (200, 200, 200))
            screen.blit(hint2, (20, hint_y))
            hint_y += 20
            
            if self._has_item("Арбалет"):
                bolts = self.game.party.inventory.items.get("Арбалетные болты", 0)
                hint3 = self.small_font.render(f"3-Арбалет(50,6кл,болты:{bolts})", True, (100, 255, 100))
                screen.blit(hint3, (20, hint_y))
                hint_y += 20
            
            if self._has_item("Свиток огненного шара"):
                hint4 = self.small_font.render("4-Огн.шар(100,4кл,50MP)", True, (100, 255, 100))
                screen.blit(hint4, (20, hint_y))
                hint_y += 20
            
            hint_space = self.small_font.render("SPACE - Пропустить ход", True, (200, 200, 200))
            screen.blit(hint_space, (20, hint_y))
            
        elif self.state == "victory":
            victory_text = self.font.render("ПОБЕДА!", True, (100, 255, 100))
            screen.blit(victory_text, (screen.get_width() // 2 - victory_text.get_width() // 2, screen.get_height() // 2))
            if self.loot_message:
                loot_text = self.small_font.render(self.loot_message, True, (255, 255, 100))
                screen.blit(loot_text, (screen.get_width() // 2 - loot_text.get_width() // 2, screen.get_height() // 2 + 40))
            esc_text = self.small_font.render("ESC - Выход", True, (200, 200, 200))
            screen.blit(esc_text, (screen.get_width() // 2 - esc_text.get_width() // 2, screen.get_height() // 2 + 80))
            
        elif self.state == "defeat":
            defeat_title = self.font.render("ПОРАЖЕНИЕ", True, (255, 50, 50))
            screen.blit(defeat_title, (screen.get_width() // 2 - defeat_title.get_width() // 2, screen.get_height() // 2 - 50))
            restart_text = self.small_font.render("R - Начать заново", True, (200, 200, 200))
            screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, screen.get_height() // 2 + 20))
            quit_text = self.small_font.render("ESC - Выйти", True, (200, 200, 200))
            screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, screen.get_height() // 2 + 60))
