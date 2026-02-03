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
        self.grid = self.adapter.build()

    def get_cell(self, x, y):
        """
        Возвращает клетку по координатам.
        """
        return self.grid[y][x]
    
    def get_grid(self):
        return self.grid
    
    def get_starting_position(self):
        for row in self.grid:
            for cell in row:
                if cell.is_start():
                    return cell.x, cell.y
        return 0, 0
    