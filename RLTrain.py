import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from ForBots.Indicators.classic_indicators import add_atr, add_sma, add_ema, add_bollinger, add_donchan_channel, add_rsi, add_slice_df

from RL_envs.envs1 import HELPGOD_Env as TradingEnv
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\oldBitget\DOGEUSDT_1m_1741087742_big.csv'



df = pd.read_csv(raw_file)

# Добавляем индикаторы
df = add_rsi(df)
df = add_bollinger(df,15)
df = add_ema(df,7)
df = add_atr(df)
df = add_slice_df(df)
# df = add_donchan_channel(df)


# Создаем среду
env = TradingEnv(df)
env = Monitor(env)
env = DummyVecEnv([lambda: env])
if __name__ == '__main__':
    # Создаем модель PPO
    model_path = "modelML/RL_models/HELPGOD_60"
    checkpoint_callback = CheckpointCallback(
    save_freq=10000,  # Сохранять каждые 100 000 шагов
    save_path="./modelML/RL_models/temp/",
    name_prefix="HELPGOD_60",
)
    while True:
        if os.path.exists(model_path+'.zip'):
            model = PPO.load(model_path,device="cpu") 
            print(f"Модель уже обучена на {model.num_timesteps} шагах.")
            model.set_env(env)
        else:
            model = PPO("MlpPolicy", env, verbose=1,device="cpu")


        # Обучаем модель
        model.learn(total_timesteps=100000,callback=checkpoint_callback, tb_log_name="HELPGOD_60")

        # Сохраняем модель
        model.save(model_path)