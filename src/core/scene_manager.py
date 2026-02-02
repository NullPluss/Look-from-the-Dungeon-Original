import pygame

class SceneManager:
    """
    Менеджер сцен.
    Отвечает за:
    - переключение между сценами (игра, бой, меню, карта, инвентарь)
    """
    
    def __init__(self):
        self.current_scene = None

    def change_scene(self, scene):
        """
        Полностью меняет активную сцену.
        """
        self.current_scene = scene

    def push(self, scene):
        """
        Сохраняет текущую сцену и переключается на новую.
        """
        # Здесь можно реализовать стек сцен, если нужно
        self.current_scene = scene

    def handle_event(self, event):
        self.current_scene.handle_event(event)

    def update(self, dt):
        self.current_scene.update(dt)

    def render(self, screen):
        self.current_scene.render(screen)