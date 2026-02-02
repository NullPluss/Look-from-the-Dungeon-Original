class Button:
    """
    Универсальная кнопка.
    """

    def __init__(self, rect, text, callback):
        self.rect = rect
        self.text = text
        self.callback = callback

    def handle_event(self, event):
        pass

    def render(self, screen):
        pass