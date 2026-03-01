class EntityManager:
    def __init__(self):
        self.entities = []
        self.entity_manager = self

    def add(self, ent):
        self.entities.append(ent)

    def update(self, dt):
        for e in self.entities:
            e.update(dt)

    def render(self, screen, camera):
        for e in self.entities:
            e.render(screen, camera)

    def get_near(self, rect, radius=40):
        return [e for e in self.entities if e.rect.colliderect(rect.inflate(radius, radius))]

    def remove_dead(self):
        self.entities = [e for e in self.entities if e.alive]