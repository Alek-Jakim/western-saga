from scripts.entity import Entity
from pygame.math import Vector2 as Vec2


class Enemy:
    def __init__(self):
        pass

    def get_player_distance_dir(self):
        enemy_pos = Vec2(self.rect.center)
        player_pos = Vec2(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = Vec2()

        return (distance, direction)

    def walk_to_player(self):
        distance, direction = self.get_player_distance_dir()

        if self.attack_radius < distance < self.walk_radius:
            self.dir = direction
            self.status = self.status.split("_")[0]
        else:
            self.dir = Vec2()

    def face_player(self):
        distance, direction = self.get_player_distance_dir()

        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:  # player to the left
                    self.status = "left_idle"
                elif direction.x > 0:  # player to the right
                    self.status = "right_idle"
            else:
                if direction.y < 0:  # player top
                    self.status = "up_idle"
                elif direction.y > 0:  # player bottom
                    self.status = "down_idle"


class Coffin(Entity, Enemy):
    def __init__(self, pos, groups, path, collision_sprites, player):
        super().__init__(pos, groups, path, collision_sprites)

        self.speed = 150

        # player interaction
        self.player = player
        self.notice_radius = 550
        self.walk_radius = 400
        self.attack_radius = 50

    def attack(self):
        distance = self.get_player_distance_dir()[0]
        if distance < self.attack_radius and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0

        if self.is_attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += self.frame_speed * dt

        # attack player
        if int(self.frame_index) == 4 and self.is_attacking:
            if self.get_player_distance_dir()[0] < self.attack_radius:
                self.player.take_damage()

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt):
        self.face_player()
        self.walk_to_player()
        self.attack()
        self.move(dt)
        self.animate(dt)


class Cactus(Entity, Enemy):
    def __init__(self, pos, groups, path, collision_sprites, player):
        super().__init__(pos, groups, path, collision_sprites)
        self.player = player

        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 100

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += self.frame_speed * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt):
        self.face_player()
        self.walk_to_player()
        self.move(dt)
        self.animate(dt)
