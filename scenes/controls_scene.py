from scripts.game_state_manager import Scene
import pygame
import sys


class Controls(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            self.screen.fill("green")

            pygame.display.update()
