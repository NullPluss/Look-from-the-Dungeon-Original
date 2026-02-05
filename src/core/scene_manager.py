class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scene = None
        self.scene_stack = []

    def register(self, name, scene):
        self.scenes[name] = scene

    def remove(self, name):
        if name in self.scenes:
            del self.scenes[name]

    def push_scene(self, name):
        if self.active_scene:
            self.scene_stack.append(self.active_scene)
            self.active_scene.on_exit()

        self.active_scene = self.scenes.get(name)
        if self.active_scene:
            self.active_scene.on_enter()

    def pop_scene(self):
        if self.active_scene:
            self.active_scene.on_exit()

        if self.scene_stack:
            self.active_scene = self.scene_stack.pop()
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
