class Scene:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state_manager = game_state_manager

    def run(self):
        pass


class GameStateManager:
    def __init__(self, current_scene, current_level=None):
        self.current_scene = current_scene
        self.current_level = current_level

    def get_scene(self):
        return self.current_scene

    def set_scene(self, scene):
        self.current_scene = scene

    def get_level(self):
        return self.current_level

    def set_level(self, level):
        self.current_level = level


class Level(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

    def run(self):
        pass
