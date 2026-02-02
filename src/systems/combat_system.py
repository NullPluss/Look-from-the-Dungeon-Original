import pygame
from systems.events import EndBattleEvent
from utils.timer import Timer
from utils.probability import chance

class CombatSystem:
    """
    Пошаговая боевая система.
    Управляет:
    - инициативой
    - очередностью ходов
    - логикой боя
    """

    def start_battle(self, party, enemies):
        pass

    def process_turn(self):
        pass

    def end_battle(self):
        if self.is_finished():
            self.event_manager.emit(EndBattleEvent())