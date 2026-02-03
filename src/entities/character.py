from entities.entity import Entity

class Character(Entity):
    """
    Персонаж игрока.
    Имеет:
    - навыки
    - экипировку
    """

    def __init__(self, name, hp, mana, x, y, rect):
        super().__init__(name, hp, mana, x, y, rect)

    def attack(self, target):
        pass

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y
    
    def update(self, dt):
        self.x += self.move_dir.x * dt * 10  # Скорость движения 100 пикселей в секунду
        self.y += self.move_dir.y * dt * 10
        self.rect.topleft = (self.x, self.y)