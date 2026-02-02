from ui.base_ui import BaseUI

class InventoryUI(BaseUI):
    """
    UI инвентаря.
    """

    def __init__(self, game, party):
        self.game = game
        self.party = party

    def handle_event(self, event):
        """
        - клики по предметам
        - ESC / I → закрыть
        """
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        """
        Отрисовывает:
        - фон
        - сетку предметов
        - описания
        """
        pass