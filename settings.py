from os import path
from pygame.font import Font

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

TILE_SIZE = 64


root_path = path.dirname(__file__).replace("\\", "/")

PATHS = {
    "player": root_path + "/graphics/player",
    "coffin": root_path + "/graphics/enemy/coffin",
    "cactus": root_path + "/graphics/enemy/cactus",
}


def draw_text(text, font_size, color, surface, pos=(0, 0)):
    font = Font(root_path + "/font/western_font.TTF", font_size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=pos)
    surface.blit(textobj, textrect)
