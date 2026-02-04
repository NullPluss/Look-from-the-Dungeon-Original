from utils.loader import AssetLoader

class TileRegistry:
    FLOOR = AssetLoader.load_image("src/assets/tiles/floor.png", scale=(32,32))
    VOID  = AssetLoader.load_image("src/assets/tiles/void.png", scale=(32,32))
    PLAYER = AssetLoader.load_image("src/assets/player_character/player.png", scale=(10,20))
    EXIT = AssetLoader.load_image("src/assets/tiles/exit_room.png", scale=(32,32))