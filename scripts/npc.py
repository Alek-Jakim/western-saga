from scripts.entity import Entity


class NPC(Entity):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(pos, groups, path, collision_sprites)

        self.frame_speed = 5

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += self.frame_speed * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
