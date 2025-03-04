import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd

class PPOPA_Env(gym.Env):
    def __init__(self, df, initial_balance=1000, window_size=15, commission=0.001):
        super(PPOPA_Env, self).__init__()
        
        # Данные
        self.df = df
        self.window_size = window_size  # Размер окна для наблюдения
        self.current_step = self.window_size
        
        # Баланс и позиция
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.shares_held = 0
        self.current_price = 0
        
        # Комиссия (например, 0.1%)
        self.commission = commission
        
        # Пространство действий: 0 - держать, 1 - покупать, 2 - продавать
        self.action_space = spaces.Discrete(3)
        
        # Пространство состояний: исторические данные + индикаторы
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.window_size, 5), dtype=np.float32
        )
        
    def _next_observation(self):
        # Возвращает текущее состояние (окно данных + индикаторы)
        frame = np.array([
            self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'open'].values,
            self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'high'].values,
            self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'low'].values,
            self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'close'].values,
            self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'volume'].values,
        ])
        return frame.T  # Транспонируем, чтобы получить (window_size, 5)
    
    def _take_action(self, action):
        # Выполняет действие (покупать, продавать, держать)
        self.current_price = self.df.loc[self.current_step, 'close']
        
        if action == 1:  # Покупать
            if self.balance > 0:
                # Учитываем комиссию при покупке
                cost = self.balance * (1 - self.commission)
                self.shares_held = cost / self.current_price
                self.balance = 0
        elif action == 2:  # Продавать
            if self.shares_held > 0:
                # Учитываем комиссию при продаже
                revenue = self.shares_held * self.current_price * (1 - self.commission)
                self.balance = revenue
                self.shares_held = 0
        
    def step(self, action):
        # Выполняет действие и возвращает новое состояние, награду и флаг завершения
        self._take_action(action)
        self.current_step += 1
        
        # Награда: изменение баланса
        reward = (self.balance + self.shares_held * self.current_price) - self.initial_balance
        
        # Проверяем, завершился ли эпизод
        done = self.current_step >= len(self.df) - 1
        
        # Новое состояние
        obs = self._next_observation()
        
        # Возвращаем 5 значений (состояние, награда, флаг завершения, флаг усечения, информация)
        return obs, reward, done, False, {}
    
    def reset(self, seed=None, options=None):
        # Сбрасывает среду к начальному состоянию
        super().reset(seed=seed)
        
        self.balance = self.initial_balance
        self.shares_held = 0
        self.current_step = self.window_size
        
        # Возвращаем начальное состояние и информацию
        return self._next_observation(), {}
    
    def render(self, mode='human'):
        # Выводит текущее состояние
        profit = (self.balance + self.shares_held * self.current_price) - self.initial_balance
        print(f"Step: {self.current_step}, Balance: {self.balance}, Shares: {self.shares_held}, Profit: {profit}")

class HELPGOD_Env(gym.Env):
    def __init__(self, df, initial_balance=1000, window_size=60, commission=0.001):
        super(HELPGOD_Env, self).__init__()
        
        # Данные
        self.df = df
        self.window_size = window_size  # Размер окна для наблюдения
        self.current_step = self.window_size
        
        # Баланс и позиция
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.shares_held = 0
        self.current_price = 0
        
        # Комиссия (например, 0.1%)
        self.commission = commission
        
        # Пространство действий: 0 - держать, 1 - покупать, 2 - продавать
        self.action_space = spaces.Discrete(3)
        
        # Пространство состояний: исторические данные + индикаторы
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.window_size, 11), dtype=np.float32
        )
        
    def _next_observation(self):
        def normalize(series):
                return (series - series.mean()) / (series.std() + 1e-8)  # Добавляем небольшое значение, чтобы избежать деления на ноль

        frame = np.array([
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'open']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'high']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'low']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'close']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'volume']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'rsi']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'bbu']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'bbd']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'sma']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'ema']),
            normalize(self.df.loc[self.current_step - self.window_size:self.current_step - 1, 'atr'])
        ])
        return frame.T  # Транспонируем, чтобы получить (window_size, 11)
    
    def _take_action(self, action):
        # Выполняет действие (покупать, продавать, держать)
        self.current_price = self.df.loc[self.current_step, 'close']
        
        if action == 1:  # Покупать
            if self.balance > 0:
                # Учитываем комиссию при покупке
                cost = self.balance * (1 - self.commission)
                self.shares_held = cost / self.current_price
                self.balance = 0
        elif action == 2:  # Продавать
            if self.shares_held > 0:
                # Учитываем комиссию при продаже
                revenue = self.shares_held * self.current_price * (1 - self.commission)
                self.balance = revenue
                self.shares_held = 0
        
    def step(self, action):
        # Выполняет действие и возвращает новое состояние, награду и флаг завершения
        self._take_action(action)
        self.current_step += 1
        
        # Награда: изменение баланса
        reward = (self.balance + self.shares_held * self.current_price) - self.initial_balance
        
        # Проверяем, завершился ли эпизод
        done = self.current_step >= len(self.df) - 1
        
        # Новое состояние
        obs = self._next_observation()
        
        # Возвращаем 5 значений (состояние, награда, флаг завершения, флаг усечения, информация)
        return obs, reward, done, False, {}
    
    def reset(self, seed=None, options=None):
        # Сбрасывает среду к начальному состоянию
        super().reset(seed=seed)
        
        self.balance = self.initial_balance
        self.shares_held = 0
        self.current_step = self.window_size
        
        # Возвращаем начальное состояние и информацию
        return self._next_observation(), {}
    
    def render(self, mode='human'):
        # Выводит текущее состояние
        profit = (self.balance + self.shares_held * self.current_price) - self.initial_balance
        print(f"Step: {self.current_step}, Balance: {self.balance}, Shares: {self.shares_held}, Profit: {profit}")