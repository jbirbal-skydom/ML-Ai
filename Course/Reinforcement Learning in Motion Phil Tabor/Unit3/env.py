import numpy as np


class Slots(object):
    def __init__(self, arms):
        # np.random.seed(92)
        self.action_space = np.random.randint(100, size=arms)
        self.action_space -= np.mean(self.action_space,  dtype=int)  # zero mean

    def payout(self, idx):
        a = np.random.normal(self.action_space[idx])
        return self.action_space[idx], a


class Constant(object):
    def __init__(self, arms):
        # np.random.seed(92)
        self.action_space = np.ones(arms)

    def payout(self, idx):
        a = np.random.normal(self.action_space[idx], 0.1)
        return self.action_space[idx], a
