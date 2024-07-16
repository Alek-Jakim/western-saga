import pygame
from settings import *


class DialogueManager:
    def __init__(self, dialogue):
        self.current_dialogue = dialogue

    def get_dialogue(self):
        self.current_dialogue

    def set_dialogue(self, dialogue):
        self.current_dialogue = dialogue


class Dialogue(pygame.sprite.Sprite):
    def __init__(self, group, npc_icon, npc_name):
        super().__init__(group)

        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT / 2 - 100))
        self.image.fill("gray")

        self.rect = self.image.get_rect(
            topleft=(0, WINDOW_HEIGHT - (WINDOW_HEIGHT / 2 - 100))
        )

        self.npc_icon = pygame.image.load(npc_icon).convert_alpha()
        self.npc_icon_rect = self.npc_icon.get_rect(topleft=(15, 0))
        self.npc_name = npc_name

        self.close_icon = pygame.image.load(ICON_PATHS["close"]).convert_alpha()
        self.close_icon_rect = self.close_icon.get_rect(topleft=(WINDOW_WIDTH - 64, 0))

        self.clicked = False

    def draw_npc_info(self):
        self.image.blit(self.npc_icon, self.npc_icon_rect)
        draw_text(
            self.npc_name,
            50,
            "black",
            self.image,
            (self.npc_icon_rect.centerx, self.npc_icon_rect.bottom + 30),
        )
        # self.image.blit(self.close_icon, self.close_icon_rect)

    def update(self, _):
        self.draw_npc_info()
