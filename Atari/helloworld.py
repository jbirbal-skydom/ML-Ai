import gym 
num_steps = 10
env = gym.make("LunarLander-v2") # Make the gym environment 

obs = env.reset() # This will reset the environment state 

for step in range(num_steps):
    # For each step, take random action
    # You can modify this to something else
    action = env.action_space.sample()  # Take a random action from the action space 
    obs, reward, done, info = env.step(action) # This will apply the action 
    env.render(mode = 'rgb_array') # Render the env

env.close() # close the env once you are done 