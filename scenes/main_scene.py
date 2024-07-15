from scripts.state_manager import *
from settings import *
import pygame
from pygame.math import Vector2 as Vec2

import sys

from levels.level_one import LevelOne


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


class Main(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        # loading assets takes time, if I load bullet each time it is created it will drop performance
        # so, I load it once here and then pass the create_bullet function to player

        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites_group = AllSprites()
        self.obstacle_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.groups = {
            "all_sprites_group": self.all_sprites_group,
            "obstacle_group": self.obstacle_group,
            "bullet_group": self.bullet_group,
            "enemy_group": self.enemy_group,
        }

        # Levels
        self.level_state_manager = StateManager("level_one")

        self.level_one = LevelOne(self.screen, self.level_state_manager, self.groups)

        self.levels = {"level_one": self.level_one}

        self.music = pygame.mixer.Sound(root_path + "/sound/music.mp3")
        self.music.play(loops=-1)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state_manager.set_state("menu")
                        running = False
                        self.reset_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            self.levels[self.level_state_manager.get_state()].run()

            dt = self.clock.tick(60) / 1000

            self.all_sprites_group.update(dt)
            self.bullet_collision()

            self.screen.fill("black")

            self.all_sprites_group.custom_draw(self.player)

            self.clicked = False

            pygame.display.update()
