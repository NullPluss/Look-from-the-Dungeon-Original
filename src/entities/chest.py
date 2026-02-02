class Chest:
    def __init__(self, position):
        self.position = position
        self.contents = self.generate_contents()

    def generate_contents(self):
        # Логика генерации содержимого сундука
        return ["gold", "potion", "sword"]