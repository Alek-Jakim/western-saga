from scripts.entity import Entity
from scripts.dialogue import Dialogue
import pygame
from settings import *


class NPC(Entity):
    def __init__(
        self, pos, groups, path, collision_sprites, player, npc_icon, npc_name
    ):
        super().__init__(pos, groups, path, collision_sprites)

        self.frame_speed = 5

        self.group = groups[1]

        self.player = player

        self.dialogue = None
        self.is_dialogue_open = False
        self.dialogue_rect = self.rect.inflate(2, 2)

        self.npc_icon = npc_icon
        self.npc_name = npc_name

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += self.frame_speed * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def input(self):

        keys = pygame.key.get_pressed()

        if len(self.group.sprites()) == 0:
            self.is_dialogue_open = False

        if self.dialogue_rect.colliderect(self.player.rect):
            if keys[pygame.K_e] and not self.is_dialogue_open:
                self.dialogue = Dialogue(self.group, self.npc_icon, self.npc_name)
                self.is_dialogue_open = True

    def update(self, dt):
        self.animate(dt)
        self.input()
