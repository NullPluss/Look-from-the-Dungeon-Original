class UIManager:
    def __init__(self):
        self.stack = []

    def add(self, ui):
        self.stack.append(ui)

    def remove(self, cls):
        self.stack = [u for u in self.stack if not isinstance(u, cls)]

    def has(self, cls):
        return any(isinstance(u, cls) for u in self.stack)

    def handle_event(self, event):
        for ui in reversed(self.stack):
            if hasattr(ui, "handle_event"):
                ui.handle_event(event)

    def render(self, screen):
        for ui in self.stack:
            ui.render(screen)

    def update(self, dt):
        for e in self.stack:
            if hasattr(e, "update"):
                e.update(dt)