# from ale_py import ALEInterface

# ale = ALEInterface()

# from ale_py.roms import Breakout

# ale.loadROM(Breakout)

import gym

env = gym.make('CartPole-v1', render_mode="human") 
obs = env.reset()
print (env.observation_space)
env.render()
############ Install virtual environment
# pip install virtualenv

######### To make virtual environment
#  python -m venv .venv

######### Start VEnv
# .\.venv\Scripts\activate

# python -m pip install -r requirements.txt