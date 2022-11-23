import gym
import random
env = gym.make("CartPole-v1", render_mode='human' )

print("Observation Space: ", env.observation_space)
print("Action Space       ", env.action_space)


episodes = 10

for episode in range(1,episodes+1):
    # At each begining reset the game 
    state = env.reset()
    # set done to False
    done = False
    # set score to 0
    score = 0
    # while the game is not finished
    while not done:
        # visualize each step
        env.render()
        # choose a random action
        action = random.choice([0,1])
        # execute the action
        n_state, reward, done, _, info = env.step(action)
        # keep track of rewards
        score+=reward
    print('episode {} score {}'.format(episode, score))

env.close()