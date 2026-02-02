from enum import Enum, auto

class CellType(Enum):
    EMPTY = auto()
    MONSTER = auto()
    NPC = auto()
    CHEST = auto()
    EXIT = auto()
    MIMIC = auto()


BASE_W = 1280
BASE_H = 720

# FPS
FPS = 60

# Размер клетки подземелья
TILE_SIZE = 64

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

# UI
UI_BG = (20, 20, 30)
UI_PANEL = (40, 40, 55)
UI_BORDER = (80, 80, 110)

# Вероятности
MIMIC_CHANCE = 0.10
NPC_CHANCE = 0.20
MONSTER_CHANCE = 0.30

CELL_SPAWN_WEIGHTS = {
    CellType.EMPTY: 40,
    CellType.MONSTER: 30,
    CellType.CHEST: 15,
    CellType.NPC: 10,
    CellType.MIMIC: 5
}