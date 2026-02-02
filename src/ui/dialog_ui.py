from ui.base_ui import BaseUI

class DialogUI(BaseUI):
    """
    Диалоговое окно NPC.
    """

    def __init__(self, npc):
        self.npc = npc
        self.current_text = ""
        self.options = []

    def handle_event(self, event):
        """
        Выбор варианта ответа.
        """
        pass

    def render(self, screen):
        """
        Рисует:
        - портрет NPC
        - текст
        - кнопки выбора
        """
        pass