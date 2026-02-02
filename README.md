<!-- Структура проекта: -->
Look from the Dungeoon Origin/src
    │
    ├── main.py
    │
    ├── core/
    │   ├── __init__.py
    │   ├── game.py
    │   ├── scene_manager.py
    │   ├── scene.py
    │   ├── event_manager.py
    │   ├── config.py
    │
    ├── world/
    │   ├── __init__.py
    │   ├── dungeon.py
    │   ├── dungeon_cell.py
    │   ├── dungeon_generator_adapter.py
    │
    ├── entities/
    │   ├── __init__.py
    │   ├── entity.py
    │   ├── party.py
    │   ├── character.py
    │   ├── npc.py
    │   ├── monster.py
    │   ├── mimic.py
    │
    ├── systems/
    │   ├── __init__.py
    │   ├── combat_system.py
    │   ├── inventory_system.py
    │   ├── quest_system.py
    │   ├── loot_system.py
    │
    ├── ui/
    │   ├── __init__.py
    │   ├── ui_manager.py
    │   ├── inventory_ui.py
    │   ├── map_ui.py
    │   ├── dialog_ui.py
    │   ├── battle_ui.py
    │
    ├── items/
    │   ├── __init__.py
    │   ├── item.py
    │   ├── potion.py
    │   ├── weapon.py
    │   ├── scroll.py
    │   ├── quest_item.py
    │
    ├── assets/
    │   ├── sprites/
    │   ├── sounds/
    │   └── fonts/
    │
    └── utils/
        ├── __init__.py
        ├── math.py
        ├── timer.py
        └── constants.py