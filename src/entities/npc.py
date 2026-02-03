from entities.entity import Entity

class NPC(Entity):
    """
    NPC.
    Имеет:
    - профессию
    - квест
    - торговлю
    """

    def __init__(self, name, profession):
        pass

    def give_quest(self):
        pass

    def trade(self, party):
        pass