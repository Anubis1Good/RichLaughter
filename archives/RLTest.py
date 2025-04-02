from stable_baselines3 import PPO
from RLTrain import env, df
model = PPO.load("modelML/RL_models/trading_agent",device="cpu")
# Сбрасываем среду
obs = env.reset()

# Тестируем агента
for _ in range(len(df) - env.window_size):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
    if done:
        break