import unittest
from world.dungeon_generator import DungeonGenerator
from world.dungeon_generator_adapter import DungeonGeneratorAdapter

def test_dungeon_generation():
    generator = DungeonGenerator(width=32, height=32)
    adapter = DungeonGeneratorAdapter(generator)
    layout = adapter.build()

    print("Generated Dungeon Layout:")
    for row in layout:
        print("".join(" " if cell.is_exit() else " " if cell.is_floor() else " " if cell.is_void() else "S" for cell in row))

    assert len(layout) == 32
    assert all(len(row) == 32 for row in layout)
    # assert any(cell.is_exit() for row in layout for cell in row)

if __name__ == "__main__":
    test_dungeon_generation()
    print("All tests passed!")