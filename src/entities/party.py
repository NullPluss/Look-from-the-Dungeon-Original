from entities.character import Character

class Party:
    """
    Отряд игрока.
    Управляет:
    - персонажами
    - общим инвентарём
    """

    def __init__(self):
        self.members = [Character("Hero", 100, 100)]  # Заглушка для главного героя
        self.inventory = []

    def add_member(self, character):
        self.members.append(character)

    def add_item(self, item):
        self.inventory.append(item)