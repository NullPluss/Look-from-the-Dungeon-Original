class DungeonCell:
    """
    Одна клетка подземелья.
    Может содержать:
    - монстра
    - npc
    - сундук
    - быть пустой
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.content = None  # Entity | None
        self.type = "void"  # "void" | "floor" | "exit" | "start"

    def enter(self, party):
        if self.content:
            self.content.on_enter(party)

    def set_type(self, cell_type):
        self.type = cell_type

    def set_content(self, content):
        self.content = content

    def is_void(self):
        return self.type == "void"

    def is_floor(self):
        return self.type == "floor"

    def is_exit(self):
        return self.type == "exit"
    
    def is_start(self):
        return self.type == "start"