from entities.entity import Entity

class Character(Entity):
    """
    Персонаж игрока или NPC.
    Имеет:
    - инвентарь
    - навыки
    - экипировку
    """

    def __init__(self, name, hp, mana):
        super().__init__(name, hp, mana)

    def attack(self, target):
        pass