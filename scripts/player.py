import pygame
from pygame.math import Vector2 as Vec2
from settings import *
from scripts.entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet):
        super().__init__(pos, groups, path, collision_sprites)

        self.speed = 800

        self.is_bullet_fired = False
        self.create_bullet = create_bullet
        self.bullet_dir = Vec2()

    def get_status(self):
        # idle
        if self.dir.x == 0 and self.dir.y == 0:
            self.status = self.status.split("_")[0] + "_idle"

        if self.is_attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += self.frame_speed * dt

        # shoot bullet
        if (
            int(self.frame_index) == 2
            and self.is_attacking
            and not self.is_bullet_fired
        ):

            # give bullet offset so it starts next to player
            bul_start_pos = self.rect.center + self.bullet_dir * 80
            self.create_bullet(
                bul_start_pos,
                self.bullet_dir,
            )
            self.is_bullet_fired = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]

    def keyboard_input(self):
        keys = pygame.key.get_pressed()

        if not self.is_attacking:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.dir.x = -1
                self.status = "left"
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.dir.x = 1
                self.status = "right"
            else:
                self.dir.x = 0

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.dir.y = -1
                self.status = "up"
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.dir.y = 1
                self.status = "down"
            else:
                self.dir.y = 0

            if keys[pygame.K_SPACE]:
                self.is_attacking = True
                self.dir = Vec2()
                self.frame_index = 0
                self.is_bullet_fired = False

                match self.status.split("_")[0]:
                    case "left":
                        self.bullet_dir = Vec2(-1, 0)
                    case "right":
                        self.bullet_dir = Vec2(1, 0)
                    case "up":
                        self.bullet_dir = Vec2(0, -1)
                    case "down":
                        self.bullet_dir = Vec2(0, 1)

    def update(self, dt):
        self.keyboard_input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
