from ale_py import ALEInterface

ale = ALEInterface()

# from ale_py.roms import Breakout

# ale.loadROM(Breakout)

import gym

env = gym.make('Breakout-v4') 
############ Install virtual environment
# pip install virtualenv

######### To make virtual environment
#  python -m venv .venv

######### Start VEnv
# .\.venv\Scripts\activate

# python -m pip install -r requirements.txt