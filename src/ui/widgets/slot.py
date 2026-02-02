class Slot:
    """
    Слот инвентаря.
    """

    def __init__(self, rect, item=None):
        self.rect = rect
        self.item = item

    def handle_event(self, event):
        pass

    def render(self, screen):
        pass