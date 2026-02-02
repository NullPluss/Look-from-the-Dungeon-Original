class Dungeon:
    """
    Хранит структуру подземелья.
    Управляет клетками, комнатами, коридорами.
    """

    def __init__(self, generator_adapter):
        self.adapter = generator_adapter
        self.grid = []
        

    def generate(self):
        """
        Вызывает DungeonGenerator.
        """
        self.grid = self.adapter.build_dungeon()
        pass

    def get_cell(self, x, y):
        """
        Возвращает клетку по координатам.
        """
        return self.grid[y][x]
    