from entities.character import Character

class NPC(Character):
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