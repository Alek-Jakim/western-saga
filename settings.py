from os import path

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720


root_path = path.dirname(__file__).replace("\\", "/")

PATHS = {
    "player": root_path + "/graphics/player",
    "coffin": root_path + "/graphics/monster/coffin",
    "cactus": root_path + "/graphics/monster/cactus",
}
