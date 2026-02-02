class Scene:
    """
    Базовый класс сцены.
    Все игровые режимы наследуются от него.
    """

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass