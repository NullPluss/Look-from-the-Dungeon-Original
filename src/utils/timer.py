class Timer:
    """
    Универсальный таймер.
    """

    def __init__(self, duration):
        self.duration = duration
        self.time = 0
        self.active = False

    def start(self):
        self.time = 0
        self.active = True

    def update(self, dt):
        if self.active:
            self.time += dt

    def finished(self):
        return self.active and self.time >= self.duration

    def reset(self):
        self.time = 0
        self.active = False