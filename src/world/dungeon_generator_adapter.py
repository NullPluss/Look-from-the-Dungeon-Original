import random
from world.dungeon_cell import DungeonCell
from utils.layout import LayoutCell
from utils.probability import weighted_choice, chance
from world.dungeon_generator import DungeonGenerator


class DungeonGeneratorAdapter:
    """
    Превращает layout в игровой мир.
    """
    
    def __init__(self, generator: DungeonGenerator):
        self.generator = generator

    def build(self):
        layout = self.generator.generate()
        grid = []

        for y, row in enumerate(layout):
            dungeon_row = []
            for x, cell in enumerate(row):
                dungeon_cell = DungeonCell(x, y)

                if cell == LayoutCell.FLOOR:
                    dungeon_cell.set_type("floor")
                    dungeon_cell.set_content(self._spawn_content())
                if cell == LayoutCell.EXIT:
                    dungeon_cell.set_type("exit")
                if cell == LayoutCell.VOID:
                    dungeon_cell.set_type("void")
                if cell == LayoutCell.START:
                    dungeon_cell.set_type("start")

                dungeon_row.append(dungeon_cell)
            grid.append(dungeon_row)

        return grid

    def _spawn_content(self):
        from utils.constants import CELL_SPAWN_WEIGHTS
        
        return random.choices(
            population=list(CELL_SPAWN_WEIGHTS.keys()),
            weights=list(CELL_SPAWN_WEIGHTS.values()),
            k=1
        )[0]
