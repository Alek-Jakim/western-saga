import pygame, sys
from settings import *
from scripts.state_manager import *


# Scenes
from scenes.menu_scene import Menu
from scenes.main_scene import Main
from scenes.controls_scene import Controls


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Western Saga")

        self.game_state_manager = GameStateManager("menu")

        self.clock = pygame.time.Clock()

        self.menu_scene = Menu(self.screen, self.game_state_manager)
        self.main_scene = Main(self.screen, self.game_state_manager)
        self.controls_scene = Controls(self.screen, self.game_state_manager)

        self.game_states = {
            "menu": self.menu_scene,
            "main": self.main_scene,
            "controls": self.controls_scene,
        }

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(60)

            self.game_states[self.game_state_manager.get_scene()].run()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
