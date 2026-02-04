import pygame
from ui.base_ui import BaseUI

class CameraUI(BaseUI):
    def __init__(self, camera):
        super().__init__((0,0,0,0))
        self.camera = camera

    def update(self, dt):
        self.camera.update(dt)

    def render(self, screen):
        pass  # overlay effects, shake, filters, debug