import numpy as np


class Robot(object):
    def __init__(self, action_space, states, discount=0.2):
        self.state_reward = {}  # (state, reward)
        self.gamma = discount
        self.policy = action_space # state to action
        self.history = []
        self.v = {}
        self.init_value(states)  # dictionary of rewards

    def init_value(self, states):
        for state in states:
            self.v[state] = 0

    def update_memory(self, state, reward):
        self.history.append((state, reward))

    def update_value(self):
        g = 0
        for state, reward in reversed(self.history):
            if state not in self.state_reward:
                self.state_reward[state] = g
            else:
                self.state_reward[state].append(g)
            g = reward + self.gamma * g

        for location in self.state_reward:
            self.v[location] = np.mean(self.state_reward[location])

        self.history = []

    def choice(self, state):
        action = self.policy[state]
        return action

    def print_value(self):
        for state in self.v:
            print(state, "{:.2f}".format(self.v[state]))


