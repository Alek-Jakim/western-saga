import pygame
from pygame.math import Vector2 as Vec2
from os import walk
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)
        self.import_assets(path)

        self.status = "down_idle"
        self.frame_index = 0
        self.frame_speed = 10

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = Vec2(self.rect.center)
        self.dir = Vec2()

        self.speed = 250

        # collisions
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        self.mask = pygame.mask.from_surface(self.image)

        self.is_attacking = False

        self.health = 3
        self.is_vulnerable = True
        self.hit_time = 0

    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def take_damage(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def vulnerability_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()

            if current_time - self.hit_time > 400:
                self.is_vulnerable = True

    def import_assets(self, path):
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    if name not in self.animations:
                        self.animations[name] = []

            else:
                for file_name in sorted(
                    folder[2], key=lambda string: string.split(".")[0]
                ):
                    file_path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pygame.image.load(file_path).convert_alpha()

                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)

    def move(self, dt):

        # Normalize vector to maintain diagonal speed
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()

        self.pos.x += self.dir.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        self.pos.y += self.dir.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.dir.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.dir.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                else:  # vertical
                    if self.dir.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.dir.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery
