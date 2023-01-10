class RandomAgent:
    def __init__(self, env) -> None:
        self.env = env
    def get_action(self, state) ->int:
        return self.env.action_space.sample()
        