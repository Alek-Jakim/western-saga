from scripts.state_manager import Scene
import pygame
from settings import *
import sys


class Button:
    def __init__(self, btn_size, btn_color, btn_pos, text, text_color, font):
        self.btn_rect = pygame.Rect(*btn_size)
        self.btn_rect.centerx = btn_pos[0]
        self.btn_rect.centery = btn_pos[1]

        self.btn_color = btn_color

        self.font = font
        self.text = self.font.render(text, True, text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.btn_rect.center

    def render(self, surface):
        pygame.draw.rect(surface, self.btn_color, self.btn_rect)
        surface.blit(self.text, self.text_rect)


class Menu(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        self.bg = pygame.image.load(root_path + "/graphics/other/bg.png").convert()
        self.bg_rect = self.bg.get_rect(topleft=(0, 0))

        # Button states
        self.button_states = {
            "new_game": pygame.transform.scale_by(
                pygame.image.load(root_path + "/graphics/menu/new_game.png").convert(),
                0.4,
            ),
            "new_game_col": pygame.transform.scale_by(
                pygame.image.load(
                    root_path + "/graphics/menu/new_game_col.png"
                ).convert(),
                0.4,
            ),
            "controls": pygame.transform.scale_by(
                pygame.image.load(root_path + "/graphics/menu/controls.png").convert(),
                0.4,
            ),
            "controls_col": pygame.transform.scale_by(
                pygame.image.load(
                    root_path + "/graphics/menu/controls_col.png"
                ).convert(),
                0.4,
            ),
            "quit": pygame.transform.scale_by(
                pygame.image.load(root_path + "/graphics/menu/quit.png").convert(),
                0.4,
            ),
            "quit_col": pygame.transform.scale_by(
                pygame.image.load(root_path + "/graphics/menu/quit_col.png").convert(),
                0.4,
            ),
        }

        # Button images

        # New Game
        self.new_game_btn = self.button_states["new_game"]
        self.new_game_btn_rect = self.new_game_btn.get_rect(
            center=((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
        )

        # Controls
        self.controls_btn = self.button_states["controls"]
        self.controls_btn_rect = self.controls_btn.get_rect(
            center=((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
        )

        self.quit_btn = self.button_states["quit"]
        self.quit_btn_rect = self.quit_btn.get_rect(
            center=((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 150))
        )

        self.clicked = False

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            self.screen.blit(self.bg, self.bg_rect)

            mouse_pos = pygame.mouse.get_pos()

            draw_text(
                "Western Saga",
                90,
                "brown",
                self.screen,
                (self.screen.get_width() // 2, self.screen.get_height() // 2 - 200),
            )

            self.screen.blit(self.new_game_btn, self.new_game_btn_rect)
            self.screen.blit(self.controls_btn, self.controls_btn_rect)
            self.screen.blit(self.quit_btn, self.quit_btn_rect)

            # Hover event
            if self.new_game_btn_rect.collidepoint(mouse_pos):
                self.new_game_btn = self.button_states["new_game_col"]
            else:
                self.new_game_btn = self.button_states["new_game"]

            if self.controls_btn_rect.collidepoint(mouse_pos):
                self.controls_btn = self.button_states["controls_col"]
            else:
                self.controls_btn = self.button_states["controls"]

            if self.quit_btn_rect.collidepoint(mouse_pos):
                self.quit_btn = self.button_states["quit_col"]
            else:
                self.quit_btn = self.button_states["quit"]

            # Click event
            if self.new_game_btn_rect.collidepoint(mouse_pos):
                if self.clicked:
                    # START GAME
                    self.game_state_manager.set_level("level_one")
                    self.game_state_manager.set_scene("main")
                    running = False

            if self.controls_btn_rect.collidepoint(mouse_pos):
                if self.clicked:
                    # START GAME
                    self.game_state_manager.set_scene("controls")
                    running = False

            if self.quit_btn_rect.collidepoint(mouse_pos):
                if self.clicked:
                    pygame.quit()
                    sys.exit()

            self.clicked = False

            pygame.display.update()
