from entities.monster import Monster
from entities.npc import NPC
import random

class MonsterFactory:
    def __init__(self):
        self.templates = [
            {"hp": 30, "atk": 5},
            {"hp": 50, "atk": 8},
            {"hp": 80, "atk": 12}
        ]

    def create(self, pos):
        return Monster(pos, random.choice(self.templates))

class NPCFactory:
    def __init__(self):
        self.dialogues = [
            ["Привет.", "Береги себя."],
            ["Опасно здесь...", "Я видел монстра..."],
            ["Ты ищешь выход?"]
        ]

    def create(self, pos):
        return NPC(pos, random.choice(self.dialogues))