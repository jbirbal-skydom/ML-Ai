import numpy as np


class Agent(object):
    def __init__(self, env: dict, action_space: dict,  alpha=0.1, random_factor=0.2):
        self.state_history = [((0, 0), 0)]
        self.G = {}
        self.reward = 0
        self.random_factor = random_factor
        self.alpha = alpha
        self.init_reward(env)
        self.action_space = action_space

    def choose_action(self, location, allowed):
        # print(location, reward, allowed)
        g1 = -10e3
        prospect = None
        if np.random.random() < self.random_factor:
            prospect = np.random.choice(allowed)
        else:
            for action in allowed:
                x, y = tuple([sum(x) for x in zip(location, self.action_space[action])])
                # x, y = location
                # x += self.action_space[action][0]
                # y += self.action_space[action][1]
                if g1 < self.G[(x, y)]:
                    g1 = self.G[(x, y)]
                    prospect = action
        return prospect

    def init_reward(self, states):
        for state in states:
            self.G[state] = np.random.uniform(low=-1.0, high=-0.1)

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        target = 0  # we only learn when we beat the maze

        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []
        self.random_factor -= 10e-5
