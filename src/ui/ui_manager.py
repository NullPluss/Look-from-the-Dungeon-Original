class UIManager:
    def __init__(self):
        self.elements = []

    def add(self, ui):
        self.elements.append(ui)

    def remove(self, ui):
        if ui in self.elements:
            self.elements.remove(ui)

    def update(self, dt):
        for e in self.elements:
            if e.visible:
                e.update(dt)

    def render(self, screen):
        for e in self.elements:
            if e.visible:
                e.render(screen)

    def handle_event(self, event):
        for e in self.elements:
            if e.visible:
                e.handle_event(event)