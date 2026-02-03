class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scene = None

    def register(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if self.active_scene:
            self.active_scene.on_exit()
        self.active_scene = self.scenes.get(name)
        if self.active_scene:
            self.active_scene.on_enter()

    def update(self, dt):
        if self.active_scene:
            self.active_scene.update(dt)

    def render(self, screen):
        if self.active_scene:
            self.active_scene.render(screen)

    def handle_event(self, event):
        if self.active_scene:
            self.active_scene.handle_event(event)