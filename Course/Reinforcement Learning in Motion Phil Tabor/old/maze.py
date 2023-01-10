import numpy as np
import pandas as pd


class Maze(object):
    def __init__(self) -> None:
        # self.reset_env()
        self.add_walls()
        # self.viz_maze()

    def add_walls(self) -> None:
        for i in range(4):
            self.maze[i, 5] = 1
        for i in range(5):
            self.maze[5, i] = 1
        for i in range(2, 5):
            self.maze[2, i] = 1
        self.maze[3, 2] = 1


def viz_maze(self) -> None:
    print(pd.DataFrame(self.maze))


def reset_env(self) -> None:
    self.maze = np.zeros([6, 6], int)
    self.maze[0, 0] = 2  # robot


env = Maze()
