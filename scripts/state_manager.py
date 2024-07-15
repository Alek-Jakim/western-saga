class Scene:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state_manager = game_state_manager

    def run(self):
        pass


class StateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state


class Level(Scene):
    def __init__(self, screen, state_manager):
        super().__init__(screen, game_state_manager=state_manager)

    def run(self):
        pass
