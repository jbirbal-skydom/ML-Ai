import numpy as np
import pandas as pd


class NoMove (BaseException):
    pass


class Maze(object):

    def __init__(self):
        self.maze = np.zeros([6, 6], dtype=np.int8)
        self.set_walls()
        # robot
        self.maze[0, 0] = 2
        self.robot = None
        self.steps = 0
        # action
        self.direction = {
            'U': [-1, 0],
            'R': [0, 1],
            'D': [1, 0],
            'L': [0, -1]
        }
        # Allowed States  {  (0,0):"D","R"  ...  (5,5):" "  }
        self.allowed_states = {}
        self.construct_allowed_states()

        # start
        self.state()

    def __str__(self):

        return "Robot named {} is at {} that took {}". format(id(self), self.robot, self.steps)

    def print_maze(self):
        print(pd.DataFrame(self.maze))

    def set_walls(self):
        self.maze[:4, 5] = 1
        self.maze[5, :4] = 1
        self.maze[2, 2:] = 1
        self.maze[3, 2] = 1

    def state(self, action=None):  # update maze
        move = None
        x, y = np.transpose(np.nonzero(self.maze == 2))[0]
        self.robot = (x, y)
        if action:
            try:
                move = self.is_move_allowed(action)
            except NoMove as e:
                # print(e)
                pass

        reward = self.update_maze(move)
        return self.robot, reward

    def is_move_allowed(self, action, state=None):
        if state is None:
            state = self.robot
        x, y = tuple([sum(x) for x in zip(state, self.direction[action])])
        # x, y = state
        # x += self.direction[action][0]
        # y += self.direction[action][1]
        if x > 5 or y > 5 or x < 0 or y < 0:
            return False
            # raise NoMove("Boundary")
        elif self.maze[x, y] == 1:
            return False
            # raise NoMove("Wall")
        else:
            return x, y

    def construct_allowed_states(self):
        allowed_states = {}
        for index, state in np.ndenumerate(self.maze):
            if state != 1:
                allowed_states[index] = []
                for action in self.direction:
                    try:
                        if self.is_move_allowed(action, index):
                            allowed_states[index].append(action)
                    except NoMove:
                        continue
        self.allowed_states = allowed_states

    def update_maze(self, move=None):
        if move:
            self.maze[self.robot] = 0
            self.robot = move
            self.maze[self.robot] = 2
        self.steps += 1
        return self.give_reward()

    def give_reward(self):
        if self.robot == (5, 5):
            return 0
        else:
            return -1

    def game_over(self):
        if self.robot == (5, 5):
            # print(self)
            return True
        else:
            return False


if __name__ == '__main__':
    maze = Maze()
    maze.print_maze()
    maze.state()
    print(maze.robot)
    maze.state(action="D")
    maze.state(action="D")
    maze.state(action="D")
    maze.state(action="D")
    maze.state(action="R")
    maze.state(action="R")
    maze.state(action="R")
    maze.state(action="R")
    maze.state(action="R")
    print(maze)
    while not maze.game_over():
        direction = input().upper()
        if direction in maze.direction:
            print('Ok')
            maze.state(action=direction)
            print(maze)
            if maze.steps % 5 == 0:
                maze.print_maze()
        else:
            print('No, sorry')
