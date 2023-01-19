import gymnasium as gym

env = gym.make('FrozenLake-v1', render_mode="ansi")

for epoch in range(5):
    obs = env.reset()
    terminated = False
    action = 1
    print(obs, action)
    for step in range(5):
        print(env.render())
        action = 1
        obs, reward, terminated, truncated, info = env.step(action)
        print(obs, action)
        if terminated or truncated:
            print("eps: ", epoch, " in ", step)
            break
