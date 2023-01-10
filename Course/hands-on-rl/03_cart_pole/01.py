
# # 01 Random agent baseline
# 
# #### 👉Before you try to solve a Reinforcement Learning problem you should get a grasp of its difficulty.
# 
# #### 👉 To do so, you need to design a dummy agent that can peform the task without much brains, and evaluate its performance.
# 
# #### 👉A simple way to do so is by using a Random Agent, that chooses its next action randomly, without paying attention at the current state of the environment.



# ## Environment 🌎

import gym
import numpy as np
from src.random_agent import RandomAgent
import matplotlib.pyplot as plt
import pandas as pd
from src.viz import show_video
import os
from src.loops import evaluate

# If this import fails, run this in your shell and relaunch jupyter:
# `export PYTHONPATH=".."`

env = gym.make('CartPole-v1')
agent = RandomAgent(env)


# ## Evaluate the agent ⏱️


n_episodes = 1000
rewards, steps = evaluate(agent, env, n_episodes)


reward_avg = np.array(rewards).mean()
reward_std = np.array(rewards).std()
print(f'Reward average {reward_avg:.2f}, std {reward_std:.2f}')


# ## Let's see how far we got in each attempt




fig, ax = plt.subplots(figsize = (10, 4))
ax.set_title("Rewards")    
pd.Series(rewards).plot(kind='hist', bins=100)

plt.show()


# ## Let's see our agent in action 🎬
# Workaround for pygame error: "error: No available video device"
# See https://stackoverflow.com/questions/15933493/pygame-error-no-available-video-device?rq=1
# This is probably needed only for Linux

os.environ["SDL_VIDEODRIVER"] = "dummy"



show_video(agent, env, sleep_sec=0.01, seed=0)



