from os import path

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

TILE_SIZE = 64


root_path = path.dirname(__file__).replace("\\", "/")

PATHS = {
    "player": root_path + "/graphics/player",
    "coffin": root_path + "/graphics/enemy/coffin",
    "cactus": root_path + "/graphics/enemy/cactus",
}
