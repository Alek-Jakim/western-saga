import pygame, sys
from settings import *
from scripts.player import Player
from scripts.sprite import Sprite
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

        # groups
        self.all_sprites = AllSprites()

        self.setup()

    def setup(self):
        tmx_data = load_pygame(root_path + "/data/western-saga-map.tmx")
        # Fence
        for x, y, surf in tmx_data.get_layer_by_name("fence").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # Objects
        for obj in tmx_data.get_layer_by_name("object"):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        # Entities
        for obj in tmx_data.get_layer_by_name("entity"):
            if obj.name == "player":
                self.player = Player(
                    (obj.x, obj.y), self.all_sprites, PATHS["player"], None
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
