from enum import Enum

class LayoutCell(Enum):
    VOID = 0     # пустота / стена
    FLOOR = 1    # проходимая клетка
    EXIT = 2     # выход