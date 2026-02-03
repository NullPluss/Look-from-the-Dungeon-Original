from pygame import Vector2

class Entity:
    """
    Базовый класс всех существ.
    """

    def __init__(self, name, hp, mana, x, y, rect):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.x = x
        self.y = y
        self.move_dir = Vector2(0, 0)  # Направление движения
        self.rect = rect  # Прямоугольник для столкновений

    def is_alive(self):
        return self.hp > 0