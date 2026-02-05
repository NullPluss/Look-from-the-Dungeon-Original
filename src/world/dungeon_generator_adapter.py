from world.dungeon_generator import DungeonGenerator


class DungeonGeneratorAdapter:
    def __init__(self, generator: DungeonGenerator):
        self.generator = generator

    def generate(self):
        return self.generator.generate()

    # def _spawn_content(self):
    #     from utils.constants import CELL_SPAWN_WEIGHTS
        
    #     return random.choices(
    #         population=list(CELL_SPAWN_WEIGHTS.keys()),
    #         weights=list(CELL_SPAWN_WEIGHTS.values()),
    #         k=1
    #     )[0]
