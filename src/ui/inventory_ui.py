from ui.base_ui import BaseUI
from ui.widgets.slot import Slot

class InventoryUI(BaseUI):
    def __init__(self, rect, rows=4, cols=5):
        super().__init__(rect)
        self.slots = []
        w = self.rect.width//cols
        h = self.rect.height//rows
        for r in range(rows):
            for c in range(cols):
                self.slots.append(Slot((self.rect.x+c*w, self.rect.y+r*h, w, h)))

    def render(self, screen):
        for s in self.slots:
            s.render(screen)