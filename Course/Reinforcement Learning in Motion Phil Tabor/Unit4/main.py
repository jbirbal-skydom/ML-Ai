import gymnasium as gym


env = gym.make('FrozenLake-v1')

for epoch in range(5):
    obs = env.reset()
    done = False
    for step in range(5):
        env.render()
        action = 1
        print(obs, action)
        obs, reward, terminated, truncated, info = env.step(action)
        if done:
            print("eps: ", epoch, " in ", step)