import numpy as np
from statistics import mean


class Robot (object):
    def __init__(self, action_space, epsilon=0.2, alpha=None):
        self.action_space = {}
        self.alpha = alpha
        for idx in range(len(action_space)):
            self.action_space[idx] = [0, 0]  # {id: mean, transactions}
        self.random_factor = epsilon

    def assessment(self, slot_number, new_score):
        average = self.action_space[slot_number][0]
        if self.alpha is None:
            visit = self.action_space[slot_number][1]
        elif self.alpha == "constant":
            visit = 0.1
        elif self.alpha == "fraction":
            visit = self.action_space[slot_number][1]

        if visit < 1:
            self.action_space[slot_number][0] = new_score
        else:
            self.action_space[slot_number][0] = average + (1 / visit)*(new_score - average)

        self.action_space[slot_number][1] += 1
        return self.action_space[slot_number][0]

    def choice(self):
        selection = list(self.action_space.keys())
        if np.random.random() < self.random_factor:
            prospect = np.random.choice(selection)
        else:
            prospect = max(self.action_space,  key=(lambda x:
                                                    self.action_space[x][0]
                                                    )
                           )
        return prospect

    def happiness(self) -> int:
        happy = []
        for x in self.action_space:
            rewards = self.action_space[x][0] * self.action_space[x][0]
            happy.append(rewards)
        return mean(happy)
