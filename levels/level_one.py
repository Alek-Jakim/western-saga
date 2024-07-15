from scripts.state_manager import Level
import pygame
import sys
from settings import *

from pytmx.util_pygame import load_pygame

from scripts.npc import NPC
from scripts.player import Player
from scripts.sprite import Sprite
from scripts.bullet import Bullet
from scripts.enemy import Coffin, Cactus


class LevelOne(Level):
    def __init__(self, screen, game_state_manager, groups):
        super().__init__(screen, game_state_manager)

        self.groups = groups

        self.game_state_manager = game_state_manager

        self.bullet_surf = pygame.image.load(
            root_path + "/graphics/other/particle.png"
        ).convert_alpha()

        self.clock = pygame.time.Clock()

        self.setup()

        self.bullet_sound = pygame.mixer.Sound(root_path + "/sound/bullet.wav")
        self.hit_sound = pygame.mixer.Sound(root_path + "/sound/hit.mp3")

    def bullet_collision(self):

        # buildings and objects
        for obstacle in self.groups["obstacle_group"].sprites():
            pygame.sprite.spritecollide(
                obstacle, self.groups["bullet_group"], True, pygame.sprite.collide_mask
            )

        # enemies
        for bullet in self.groups["bullet_group"].sprites():
            sprites = pygame.sprite.spritecollide(
                bullet, self.groups["enemy_group"], False, pygame.sprite.collide_mask
            )

            if sprites:
                bullet.kill()
                self.hit_sound.play()
                for sprite in sprites:
                    sprite.take_damage()

        # player
        if pygame.sprite.spritecollide(
            self.player, self.groups["bullet_group"], True, pygame.sprite.collide_mask
        ):
            self.player.take_damage()
            bullet.kill()
            self.hit_sound.play()

    def create_bullet(self, pos, dir):
        self.bullet_sound.play()
        Bullet(
            pos,
            dir,
            self.bullet_surf,
            [self.groups["all_sprites_group"], self.groups["bullet_group"]],
        )

    def empty_groups(self):
        self.groups["all_sprites_group"].empty()
        self.groups["enemy_group"].empty()
        self.groups["obstacle_group"].empty()
        self.groups["bullet_group"].empty()

    def setup(self):
        tmx_data = load_pygame(root_path + "/data/western-saga-map.tmx")
        # Fence
        for x, y, surf in tmx_data.get_layer_by_name("fence").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                [self.groups["all_sprites_group"], self.groups["obstacle_group"]],
            )

        # Objects
        for obj in tmx_data.get_layer_by_name("object"):
            Sprite(
                (obj.x, obj.y),
                obj.image,
                [self.groups["all_sprites_group"], self.groups["obstacle_group"]],
            )

        # Entities
        for obj in tmx_data.get_layer_by_name("entity"):
            if obj.name == "player":
                # Player gets reference to obstacles but doesn't belong to the group itself
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.groups["all_sprites_group"],
                    path=PATHS["player"],
                    collision_sprites=self.groups["obstacle_group"],
                    create_bullet=self.create_bullet,
                )

            if obj.name == "coffin":
                # Player gets reference to obstacles but doesn't belong to the group itself
                Coffin(
                    pos=(obj.x, obj.y),
                    groups=[
                        self.groups["all_sprites_group"],
                        self.groups["enemy_group"],
                    ],
                    path=PATHS["coffin"],
                    collision_sprites=self.groups["obstacle_group"],
                    player=self.player,
                )

            if obj.name == "cactus":
                # Player gets reference to obstacles but doesn't belong to the group itself
                Cactus(
                    pos=(obj.x, obj.y),
                    groups=[
                        self.groups["all_sprites_group"],
                        self.groups["enemy_group"],
                    ],
                    path=PATHS["cactus"],
                    collision_sprites=self.groups["obstacle_group"],
                    player=self.player,
                    create_bullet=self.create_bullet,
                )

            if obj.name == "stranger":
                # Player gets reference to obstacles but doesn't belong to the group itself
                NPC(
                    pos=(obj.x, obj.y),
                    groups=self.groups["all_sprites_group"],
                    path=PATHS["stranger"],
                    collision_sprites=self.groups["obstacle_group"],
                )

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state_manager.set_level(None)
                        self.game_state_manager.set_scene("menu")
                        self.empty_groups()
                        self.setup()
                        running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            dt = self.clock.tick(60) / 1000

            self.groups["all_sprites_group"].update(dt)
            self.bullet_collision()

            self.screen.fill("black")

            self.groups["all_sprites_group"].custom_draw(self.player)

            self.clicked = False

            pygame.display.update()
