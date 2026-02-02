import random
from entities.chest import Chest
from entities.factories import MonsterFactory
from entities.factories import NPCFactory
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
        self.grid = []

    def build(self):
        layout = self.generator.generate()

        for y, row in enumerate(layout):
            dungeon_row = []
            for x, cell in enumerate(row):
                dungeon_cell = DungeonCell(x, y)

                if cell == LayoutCell.FLOOR:
                    dungeon_cell.content = self._spawn_content()
                elif cell == LayoutCell.EXIT:
                    dungeon_cell.content = "exit"

                dungeon_row.append(dungeon_cell)
            self.grid.append(dungeon_row)

        return self.grid

    def _spawn_content(self):
        from utils.constants import CELL_SPAWN_WEIGHTS
        
        return random.choices(
            population=list(CELL_SPAWN_WEIGHTS.keys()),
            weights=list(CELL_SPAWN_WEIGHTS.values()),
            k=1
        )[0]

    def __init__(self, generator):
        self.generator = generator

    def build_dungeon(self):
        return self.generator.generate()