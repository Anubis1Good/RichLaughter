import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import numpy as np
from stable_baselines3 import PPO
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price,add_ema,add_stochastic,add_atr,add_local_extrema,add_enter_price2close,add_supertrend, add_rsi,add_bollinger

class STARL1_PPOPA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.model = PPO.load("modelML/RL_models/PPOPA_15",device="cpu")  # Загружаем обученную модель

    def get_rl_signal(self, df):
        """
        Генерация сигналов с использованием RL-модели.
        """
        signals = []
        for i in range(len(df)):
            # Получаем текущее состояние (окно данных)
            state = df.iloc[max(0, i - self.period):i][['open', 'high', 'low', 'close', 'volume']].values
            if len(state) < self.period:
                # Если данных недостаточно, пропускаем
                signals.append(0)
                continue
            
            # Предсказываем действие (0 - держать, 1 - покупать, 2 - продавать)
            action, _ = self.model.predict(state,deterministic=True)
            signals.append(action)
        
        return signals

    def preprocessing(self, df):
        """
        Предобработка данных и генерация сигналов.
        """
        # df = add_rsi(df)
        # df = add_bollinger(df,15)
        # df = add_ema(df,7)
        # df = add_atr(df)
        df = add_enter_price2close(df)
        
        # Генерация сигналов с использованием RL-модели
        df['signal'] = self.get_rl_signal(df)
        
        df = add_slice_df(df, self.period)
        return df

    def __call__(self, row, *args, **kwds):
        """
        Возвращает действие на основе финального сигнала.
        """
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == 2:  # RL-модель возвращает 2 для продажи
            return 'short_pw'
        else:
            return None  # Держать позицию
class STARL1_HELPGOD(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.model = PPO.load("modelML/RL_models/HELPGOD_60",device="cpu")  
        # self.model = PPO.load("modelML/RL_models/temp/HELPGOD_60_144_steps",device="cpu")  
        print(f"Модель уже обучена на {self.model.num_timesteps} шагах.")# Загружаем обученную модель

    def get_rl_signal(self, df):
        """
        Генерация сигналов с использованием RL-модели.
        """
        def normalize(series):
            return (series - series.mean()) / (series.std() + 1e-8)  # Добавляем небольшое значение, чтобы избежать деления на ноль

        signals = []
        for i in range(len(df)):
            # Получаем текущее состояние (окно данных)
            window = df.iloc[max(0, i - self.period):i]
            if len(window) < self.period:
                # Если данных недостаточно, пропускаем
                signals.append(0)
                continue
            
            # Нормализуем данные в окне
            normalized_window = np.array([
                normalize(window['open']),
                normalize(window['high']),
                normalize(window['low']),
                normalize(window['close']),
                normalize(window['volume']),
                normalize(window['rsi']),
                normalize(window['bbu']),
                normalize(window['bbd']),
                normalize(window['sma']),
                normalize(window['ema']),
                normalize(window['atr'])
            ]).T  # Транспонируем, чтобы получить (window_size, 11)
            
            # Предсказываем действие (0 - держать, 1 - покупать, 2 - продавать)
            action, _ = self.model.predict(normalized_window, deterministic=True)
            signals.append(action)
        
        return signals
    def preprocessing(self, df):
        """
        Предобработка данных и генерация сигналов.
        """
        df = add_rsi(df)
        df = add_bollinger(df,15)
        df = add_ema(df,7)
        df = add_atr(df)
        df = add_enter_price2close(df)
        
        # Генерация сигналов с использованием RL-модели
        
        df = add_slice_df(df, self.period)
        df['signal'] = self.get_rl_signal(df)
        return df

    def __call__(self, row, *args, **kwds):
        """
        Возвращает действие на основе финального сигнала.
        """
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == 2:  # RL-модель возвращает 2 для продажи
            return 'short_pw'
        else:
            return None  # Держать позицию