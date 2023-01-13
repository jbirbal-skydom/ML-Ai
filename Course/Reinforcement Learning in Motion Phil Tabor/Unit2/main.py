from environment import Maze
from agent import Agent
import matplotlib.pyplot as plt
import logging
import numpy as np

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)

debug = 0

if __name__ == '__main__':
    maze = Maze()
    robot = Agent(maze.allowed_states, maze.direction, alpha=0.1, random_factor=0.25)
    location, reward = maze.state()
    move_history = []

    for i in range(5000):
        if i % 1000 == 0:
            print(i)

        while not maze.game_over():

            if debug:
                direction = input().upper()
                if direction in maze.direction:
                    state, reward = maze.state(action=direction)
                    print(state, reward)

            direction = robot.choose_action(location, maze.allowed_states[location])
            location, reward = maze.state(action=direction)
            robot.update_state_history(location, reward)
            if maze.steps > 1000:
                maze.robotPosition = (5, 5)
            if i > 4998:
                logger.info(location)
                viz = np.zeros([6, 6], dtype=np.int8)
                for state in robot.G:
                    viz[state] = robot.G[state]
                print("done")


        # after epoch
        robot.learn()
        move_history.append(maze.steps)
        maze = Maze()

    # after all epoch
    plt.subplot(211)
    plt.semilogy(move_history, 'b--')
    plt.legend(['alpha=0.1'])
    plt.show()

