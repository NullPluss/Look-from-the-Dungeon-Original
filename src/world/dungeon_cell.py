from entities.chest import Chest
from entities.monster import Monster
from entities.npc import NPC
from systems.events import StartBattleEvent, StartDialogEvent, StartOpenChestEvent


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

    def enter(self, party):
        if self.content:
            self.content.on_enter(party)


    # def enter(self, party):
    #     if isinstance(self.content, Monster):
    #         self.event_manager.emit(
    #             StartBattleEvent([self.content])
    #         )

    #     if isinstance(self.content, NPC):
    #         event_manager.emit(
    #             StartDialogEvent([self.content])
    #         )

    #     if isinstance(self.content, Chest):
    #         event_manager.emit(
    #             StartOpenChestEvent([self.content])
    #         )