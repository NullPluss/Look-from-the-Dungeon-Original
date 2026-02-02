from ui.base_ui import BaseUI

class MapUI(BaseUI):
    """
    UI карты подземелья.
    """

    def __init__(self, dungeon):
        self.dungeon = dungeon

    def handle_event(self, event):
        """
        M / ESC → закрыть
        """
        pass

    def render(self, screen):
        """
        Рисует:
        - исследованные клетки
        - стены
        - NPC
        """
        pass