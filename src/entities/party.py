class Party:
    """
    Отряд игрока.
    Управляет:
    - персонажами
    - общим инвентарём
    """

    def __init__(self, player, inventory):
        self.player = player
        self.members = [self.player]
        self.inventory = inventory

    def get_player(self):
        return self.player

    def add_member(self, character):
        self.members.append(character)

    def add_item(self, item):
        self.inventory.add_item(item)

    def get_inventory(self):
        return self.inventory
    
    def remove_item(self, item):
        self.inventory.remove_item(item)

    def get_members(self):
        return self.members
    
    def remove_member(self, character):
        self.members.remove(character)

    def set_inventory(self, inventory):
        self.inventory = inventory

    def get_hero(self):
        return self.members[0]