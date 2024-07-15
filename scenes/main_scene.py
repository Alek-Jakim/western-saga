from scripts.game_state_manager import Scene
from settings import *
import pygame
from pygame.math import Vector2 as Vec2
from pytmx.util_pygame import load_pygame
import sys

from scripts.player import Player
from scripts.sprite import Sprite
from scripts.bullet import Bullet
from scripts.enemy import Coffin, Cactus


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
        self.bullet_surf = pygame.image.load(
            root_path + "/graphics/other/particle.png"
        ).convert_alpha()

        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites_group = AllSprites()
        self.obstacle_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.music = pygame.mixer.Sound(root_path + "/sound/music.mp3")
        self.music.play(loops=-1)

        self.bullet_sound = pygame.mixer.Sound(root_path + "/sound/bullet.wav")
        self.hit_sound = pygame.mixer.Sound(root_path + "/sound/hit.mp3")

        self.setup()

    def bullet_collision(self):

        # buildings and objects
        for obstacle in self.obstacle_group.sprites():
            pygame.sprite.spritecollide(
                obstacle, self.bullet_group, True, pygame.sprite.collide_mask
            )

        # enemies
        for bullet in self.bullet_group.sprites():
            sprites = pygame.sprite.spritecollide(
                bullet, self.enemy_group, False, pygame.sprite.collide_mask
            )

            if sprites:
                bullet.kill()
                self.hit_sound.play()
                for sprite in sprites:
                    sprite.take_damage()

        # player
        if pygame.sprite.spritecollide(
            self.player, self.bullet_group, True, pygame.sprite.collide_mask
        ):
            self.player.take_damage()
            bullet.kill()
            self.hit_sound.play()

    def create_bullet(self, pos, dir):
        self.bullet_sound.play()
        Bullet(pos, dir, self.bullet_surf, [self.all_sprites_group, self.bullet_group])

    def reset_game(self):
        self.all_sprites_group.empty()
        self.enemy_group.empty()
        self.obstacle_group.empty()
        self.bullet_group.empty()

        self.setup()

    def setup(self):
        tmx_data = load_pygame(root_path + "/data/western-saga-map.tmx")
        # Fence
        for x, y, surf in tmx_data.get_layer_by_name("fence").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                [self.all_sprites_group, self.obstacle_group],
            )

        # Objects
        for obj in tmx_data.get_layer_by_name("object"):
            Sprite(
                (obj.x, obj.y), obj.image, [self.all_sprites_group, self.obstacle_group]
            )

        # Entities
        for obj in tmx_data.get_layer_by_name("entity"):
            if obj.name == "player":
                # Player gets reference to obstacles but doesn't belong to the group itself
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites_group,
                    path=PATHS["player"],
                    collision_sprites=self.obstacle_group,
                    create_bullet=self.create_bullet,
                )

            if obj.name == "coffin":
                # Player gets reference to obstacles but doesn't belong to the group itself
                Coffin(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites_group, self.enemy_group],
                    path=PATHS["coffin"],
                    collision_sprites=self.obstacle_group,
                    player=self.player,
                )

            if obj.name == "cactus":
                # Player gets reference to obstacles but doesn't belong to the group itself
                Cactus(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites_group, self.enemy_group],
                    path=PATHS["cactus"],
                    collision_sprites=self.obstacle_group,
                    player=self.player,
                    create_bullet=self.create_bullet,
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
                        self.game_state_manager.set_state("menu")
                        running = False
                        self.reset_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            dt = self.clock.tick(60) / 1000

            self.all_sprites_group.update(dt)
            self.bullet_collision()

            self.screen.fill("black")

            self.all_sprites_group.custom_draw(self.player)

            self.clicked = False

            pygame.display.update()
