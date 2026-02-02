from utils.constants import UI_BG, UI_PANEL

class UIManager:
    """
    Управляет активным UI.
    """

    def __init__(self):
        self.active_ui = None

    def set_ui(self, ui):
        self.active_ui = ui

    def clear(self):
        self.active_ui = None

    def handle_event(self, event):
        if self.active_ui:
            self.active_ui.handle_event(event)

    def update(self, dt):
        if self.active_ui:
            self.active_ui.update(dt)

    def render(self, screen):
        if self.active_ui:
            self.active_ui.render(screen)