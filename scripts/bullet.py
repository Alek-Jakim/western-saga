import pygame
from pygame.math import Vector2 as Vec2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, dir, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(center=pos)

        self.pos = Vec2(self.rect.center)
        self.dir = dir

        self.speed = 600

    def update(self, dt):
        self.pos += self.dir * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
