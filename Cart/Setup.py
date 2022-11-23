import gym
import random
from rl.agents import SARSAAgent
from rl.policy import EpsGreedyQPolicy
from Skydom.NN.RL import FullyConnected
from keras.optimizers import Adam

env = gym.make("CartPole-v1", render_mode='human')

print("[INFO] loading images...")
print("Observation Space: ", env.observation_space)
print("Action Space       ", env.action_space)
states = env.observation_space.shape[0]
actions = env.action_space.n

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

# initialize the optimizer and model
print("[INFO] compiling model...")
model = FullyConnected.build(states=states, height=24, depth=3, actions=actions)
policy = EpsGreedyQPolicy()
sarsa = SARSAAgent(model = model, policy = policy, nb_actions = env.action_space.n)
sarsa.compile('adam', metrics = ['mse'])


print("[INFO] training network...")
sarsa.fit(env, nb_steps = 50000, visualize = False, verbose = 1)


print("[INFO] serializing network...")
sarsa.save_weights('sarsa_weights.h5f', overwrite=True)

print("[INFO] evaluating network...")
scores = sarsa.test(env, nb_episodes = 100, visualize= False)
print('Average score over 100 test games:{}'.format(np.mean(scores.history['episode_reward'])))

