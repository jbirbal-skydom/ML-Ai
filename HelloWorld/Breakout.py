import gym
import time
env = gym.make("BreakoutNoFrameskip-v4", render_mode='human' )

print("Observation Space: ", env.observation_space)
print("Action Space       ", env.action_space)
obs = env.reset()


for i in range(1000):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    time.sleep(0.1)

env.close()