import pygame, sys
from settings import *
from scripts.player import Player
from scripts.sprite import Sprite
from scripts.bullet import Bullet
from scripts.enemy import Coffin
from pygame.math import Vector2 as Vec2
from pytmx.util_pygame import load_pygame


# Camera - replace vanilla draw method with a custom one so that camera follows player
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = Vec2()
        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load(
            root_path + "/graphics/other/bg.png"
        ).convert()

    def custom_draw(self, player):

        # Change offset
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # Blit surf
        self.screen.blit(self.background, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.screen.blit(
                sprite.image,
                offset_rect,
            )


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Western Saga")
        self.clock = pygame.time.Clock()

        # loading assets takes time, if I load bullet each time it is created it will drop performance
        self.bullet_surf = pygame.image.load(
            root_path + "/graphics/other/particle.png"
        ).convert_alpha()

        # groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.setup()

    def create_bullet(self, pos, dir):
        Bullet(pos, dir, self.bullet_surf, [self.all_sprites, self.bullets])

    def setup(self):
        tmx_data = load_pygame(root_path + "/data/western-saga-map.tmx")
        # Fence
        for x, y, surf in tmx_data.get_layer_by_name("fence").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.obstacles]
            )

        # Objects
        for obj in tmx_data.get_layer_by_name("object"):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

        # Entities
        for obj in tmx_data.get_layer_by_name("entity"):
            if obj.name == "player":
                # Player gets reference to obstacles but doesn't belong to the group itself
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS["player"],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet,
                )

            if obj.name == "coffin":
                # Player gets reference to obstacles but doesn't belong to the group itself
                Coffin(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS["coffin"],
                    collision_sprites=self.obstacles,
                )

            if obj.name == "cactus":
                # Player gets reference to obstacles but doesn't belong to the group itself
                Coffin(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS["cactus"],
                    collision_sprites=self.obstacles,
                )

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000

            self.all_sprites.update(dt)

            self.screen.fill("black")

            self.all_sprites.custom_draw(self.player)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
