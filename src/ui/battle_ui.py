from ui.base_ui import BaseUI

class BattleUI(BaseUI):
    """
    UI пошагового боя.
    """

    def __init__(self, combat_system):
        self.combat = combat_system

    def handle_event(self, event):
        """
        Выбор действий.
        """
        pass

    def render(self, screen):
        """
        HP бары, иконки, очередь ходов.
        """
        pass