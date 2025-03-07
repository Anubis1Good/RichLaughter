import os
import json
import numpy as np
import pandas as pd
import warnings
from time import time
from datetime import datetime

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.varmax import VARMAX

from prophet import Prophet
from xgboost import XGBRegressor,Booster,DMatrix,train
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from skimage.metrics import mean_squared_error

from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price,add_enter_price2close, add_donchan_channel
from ForBots.Indicators.price_funcs import get_universal_r,get_universal
from strategies.work_strategies.BaseTA import BaseTABitget
from request_functions.download_bitget import download_bitget,create_df

import logging
logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.CRITICAL)

# TODO пофиксить ворнинги
warnings.filterwarnings('ignore')

class STAML1_XGBR1(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df = df.dropna()

        # Признаки
        X = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        # Целевые переменные
        y_high = df['target_high']
        y_low = df['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X)
        df['predicted_low'] = model_low.predict(X)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class STAML1_XGBR2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class STAML1_XGBR2e(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred) + df['high'].std()*0.05
        df['predicted_low'] = model_low.predict(X_pred) - df['high'].std() * 0.05
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
class STAML1_XGBR2h(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['predicted_middle'] = (df['predicted_high'] + df['predicted_low']) /2
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        if row['close'] < row['predicted_middle']:
            return 'close_short_pw'
        if row['close'] > row['predicted_middle']:
            return 'close_long_pw'
class STAML1_XGBR2he(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred) + df['high'].std()*0.05
        df['predicted_low'] = model_low.predict(X_pred) - df['high'].std() * 0.05
        df['predicted_middle'] = (df['predicted_high'] + df['predicted_low']) /2
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        if row['close'] < row['predicted_middle']:
            return 'close_short_pw'
        if row['close'] > row['predicted_middle']:
            return 'close_long_pw'
#D DC 
class STAML1_XGBR2_DC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        df = add_donchan_channel(df,self.period)
        df = add_slice_df(df,self.period)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['max_hb'].shift(i)
            df[f'low_lag_{i}'] = df['min_hb'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['max_hb'].shift(-future_steps)
        df['target_low'] = df['min_hb'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'     
         
class STAML1_XGBR2_DCh(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        df = add_donchan_channel(df,self.period)
        df = add_slice_df(df,self.period)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['max_hb'].shift(i)
            df[f'low_lag_{i}'] = df['min_hb'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['max_hb'].shift(-future_steps)
        df['target_low'] = df['min_hb'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['predicted_middle'] = (df['predicted_high'] + df['predicted_low']) /2
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'      
        if row['close'] < row['predicted_middle']:
            return 'close_short_pw'
        if row['close'] > row['predicted_middle']:
            return 'close_long_pw'
# BD
class STAML1_AXGBR2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = -1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = 1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class STAML1_XGBR3_Trainer(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
        filename = f'modelML/STAML1_XGBRs/{symbol}_{granularity}_{period}_{future_steps}_XGBR3'
        self.filename_high = filename + '_high.model'
        self.filename_low = filename + '_low.model'
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']

        # Обучение модели XGBoost для предсказания максимумов
        model_high = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_high.fit(X, y_high)

        # Обучение модели XGBoost для предсказания минимумов
        model_low = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model_low.fit(X, y_low)
        # Генерация торговых сигналов

        model_high.save_model(self.filename_high)
        model_low.save_model(self.filename_low)
        return df
    def __call__(self, row, *args, **kwds):
        return None

class STAML1_XGBR3_User(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
        filename = f'modelML/STAML1_XGBRs/{symbol}_{granularity}_{period}_{future_steps}_XGBR3'
        self.filename_high = filename + '_high.model'
        self.filename_low = filename + '_low.model'
    def preprocessing(self, df):
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)


        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        model_high = Booster()
        model_high.load_model(self.filename_high)

        model_low = Booster()
        model_low.load_model(self.filename_low)
        X_pred = DMatrix(X_pred)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
# Постоянная модель с дообучением и сохранением каждый шаг
class STAML1_XGBR4(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
        filename = f'modelML/STAML1_XGBRs/{symbol}_{granularity}_{period}_{future_steps}_XGBR4'
        self.filename_high = filename + '_high.model'
        self.filename_low = filename + '_low.model'
        self.have_models = False

    def get_model(self,filename,X,y):
        if not os.path.exists(filename):
        # Обучение модели XGBoost для предсказания максимумов
            model = XGBRegressor(n_estimators=100, learning_rate=0.1)
            model.fit(X, y)
        else:
            self.have_models = True
            model = Booster()
            model.load_model(filename)
            new_data = DMatrix(X, label=y)
            params = json.loads(model.save_config())
            model = train(params,new_data,xgb_model=model)
        model.save_model(filename)
        return model
    
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']
        model_high = self.get_model(self.filename_high,X,y_high)
        model_low = self.get_model(self.filename_low,X,y_low)
        if self.have_models:
            X_pred = DMatrix(X_pred)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'

# Постоянная модель с дообучением на последних данных при первом старте и дообучением на каждом шаге
class STAML1_XGBR5(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=10, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_parts = 50
        self.future_steps = future_steps
        filename = f'modelML/STAML1_XGBRs/{symbol}_{granularity}_{period}_{future_steps}_XGBR5'
        self.filename_high = filename + '_high.model'
        self.filename_low = filename + '_low.model'
        self.have_models = False
        self.is_first_start = True

    def first_start(self):
        df = download_bitget(self.symbol,self.granularity,self.productType,self.n_parts)
        df = create_df(df)
        df = self.help_preprocessing(df)
        self.is_first_start = False
        print('XGBR5update',datetime.now())
        return df
    
    def get_model(self,filename,X,y):
        if not os.path.exists(filename):
        # Обучение модели XGBoost для предсказания максимумов
            model = XGBRegressor(n_estimators=100, learning_rate=0.1)
            model.fit(X, y)
        else:
            self.have_models = True
            model = Booster()
            model.load_model(filename)
            new_data = DMatrix(X, label=y)
            params = json.loads(model.save_config())
            model = train(params,new_data,xgb_model=model)
        model.save_model(filename)
        return model
    
    def prepare_train(self,df):
        future_steps = self.future_steps
        lags = self.period
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']
        return X,y_high,y_low,X_pred
    
    def help_preprocessing(self,df):
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        X,y_high,y_low,X_pred = self.prepare_train(df)

        model_high = self.get_model(self.filename_high,X,y_high)
        model_low = self.get_model(self.filename_low,X,y_low)
        if self.have_models:
            X_pred = DMatrix(X_pred)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    
    def preprocessing(self, df):
        if self.is_first_start:
            df = self.first_start()
        df = self.help_preprocessing(df)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
# Постоянная модель с дообучением на последних данных при первом старте и дообучением на каждом шаге без сохранения    
class STAML1_XGBR6(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=10, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_parts = 50
        self.future_steps = future_steps
        filename = f'modelML/STAML1_XGBRs/{symbol}_{granularity}_{period}_{future_steps}_XGBR6'
        self.filename_high = filename + '_high.model'
        self.filename_low = filename + '_low.model'
        self.have_models = False
        self.is_first_start = True

    def first_start(self):
        df = download_bitget(self.symbol,self.granularity,self.productType,self.n_parts)
        df = create_df(df)
        df = self.help_preprocessing(df)
        self.is_first_start = False
        print('XGBR6update',datetime.now()) 
        return df
    
    def get_model(self,filename,X,y):
        if not os.path.exists(filename):
        # Обучение модели XGBoost для предсказания максимумов
            model = XGBRegressor(n_estimators=100, learning_rate=0.1)
            model.fit(X, y)
            model.save_model(filename)
        else:
            self.have_models = True
            model = Booster()
            model.load_model(filename)
            if self.is_first_start:
                new_data = DMatrix(X, label=y)
                params = json.loads(model.save_config())
                model = train(params,new_data,xgb_model=model)
        return model
    
    def prepare_train(self,df):
        future_steps = self.future_steps
        lags = self.period
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']
        return X,y_high,y_low,X_pred
    
    def help_preprocessing(self,df):
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        X,y_high,y_low,X_pred = self.prepare_train(df)

        model_high = self.get_model(self.filename_high,X,y_high)
        model_low = self.get_model(self.filename_low,X,y_low)
        if self.have_models:
            X_pred = DMatrix(X_pred)
        # Генерация торговых сигналов
        df['predicted_high'] = model_high.predict(X_pred)
        df['predicted_low'] = model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    
    def preprocessing(self, df):
        if self.is_first_start:
            df = self.first_start()
        df = self.help_preprocessing(df)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
# Модель с обучением на последних данных при первом старте и без дообучения на каждом шаге        
class STAML1_XGBR7(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=10, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_parts = 50
        self.future_steps = future_steps
        self.is_first_start = True

    def first_start(self):
        df = download_bitget(self.symbol,self.granularity,self.productType,self.n_parts)
        df = create_df(df)
        df = self.help_preprocessing(df)
        self.is_first_start = False
        print('XGBR7update',datetime.now())
        return df
    
    def get_model(self,X,y):
        # Обучение модели XGBoost для предсказания максимумов
        model = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model.fit(X, y)
        return model
    
    def prepare_train(self,df):
        future_steps = self.future_steps
        lags = self.period
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']
        return X,y_high,y_low,X_pred
    
    def prepare_work(self,df):
        lags = self.period
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)
        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        return X_pred

    def help_preprocessing(self,df):
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        if self.is_first_start:
            X,y_high,y_low,X_pred = self.prepare_train(df)
            self.model_high = self.get_model(X,y_high)
            self.model_low = self.get_model(X,y_low)
        else:
            X_pred = self.prepare_work(df)
        # Генерация торговых сигналов
        df['predicted_high'] = self.model_high.predict(X_pred)
        df['predicted_low'] = self.model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    
    def preprocessing(self, df):
        if self.is_first_start:
            df = self.first_start()
        df = self.help_preprocessing(df)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
# Модель с обучением на последних данных при первом старте и без дообучения на каждом шаге. Обновляется каждый час            
class STAML1_XGBR8(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=10, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_parts = 50
        self.future_steps = future_steps
        self.update_hour = (time()//3600) + 1
        self.need_train = True

    def update_model(self):
        df = download_bitget(self.symbol,self.granularity,self.productType,self.n_parts)
        df = create_df(df)
        df = self.help_preprocessing(df)
        print('XGBR8update',datetime.now())
        self.need_train = False
        return df
    
    def get_model(self,X,y):
        # Обучение модели XGBoost для предсказания максимумов
        model = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model.fit(X, y)
        return model
    
    def prepare_train(self,df):
        future_steps = self.future_steps
        lags = self.period
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)

        # Целевые переменные — максимумы и минимумы на future_steps вперёд
        df['target_high'] = df['high'].shift(-future_steps)
        df['target_low'] = df['low'].shift(-future_steps)

        # Убираем строки с NaN (из-за лагов и целевых переменных)
        df_train = df.dropna()

        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        X = df_train[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]

        # Целевые переменные
        y_high = df_train['target_high']
        y_low = df_train['target_low']
        return X,y_high,y_low,X_pred
    
    def prepare_work(self,df):
        lags = self.period
        # Создание признаков (фичей) — лаги цен (close, high, low)
        for i in range(1, lags + 1):
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)
        # Признаки
        X_pred = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
            [f'high_lag_{i}' for i in range(1, lags + 1)] + 
            [f'low_lag_{i}' for i in range(1, lags + 1)]]
        return X_pred  
    
    def help_preprocessing(self,df):
        df = add_enter_price2close(df)
        # Создание признаков (фичей) — лаги цен (close, high, low)
        if self.need_train:
            X,y_high,y_low,X_pred = self.prepare_train(df)
            self.model_high = self.get_model(X,y_high)
            self.model_low = self.get_model(X,y_low)
        else:
            X_pred = self.prepare_work(df)
        # Генерация торговых сигналов
        df['predicted_high'] = self.model_high.predict(X_pred)
        df['predicted_low'] = self.model_low.predict(X_pred)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Покупка: цена закрытия пересекает предсказанный минимум снизу вверх
        df.loc[df['close'] < df['predicted_low'], 'signal'] = 1

        # Продажа: цена закрытия пересекает предсказанный максимум сверху вниз
        df.loc[df['close'] > df['predicted_high'], 'signal'] = -1
        # Предсказание максимумов и минимумов

        df = add_slice_df(df,self.period)
        return df
    
    def preprocessing(self, df):
        ch = time()//3600
        if self.need_train:
            df = self.update_model()
        if self.update_hour <= ch:
            self.update_hour = ch + 1
            self.need_train = True
        df = self.help_preprocessing(df)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
# TODO
# def prepare_forecast_data(data, forecast_steps=10):
#     # Формируем признаки и целевые значения
#     X = data[['open', 'high', 'low', 'volume']].values[:-forecast_steps]
#     y = data['close'].values[forecast_steps:]
#     return X, y

# def fit_model(X_train, y_train):
#     model = LinearRegression()
#     model.fit(X_train, y_train)
#     return model

# def predict_future_prices(model, data, forecast_steps=10):
#     future_prices = []
#     last_index = data.index[-1]

#     required_columns = ['open', 'high', 'low', 'volume']  # Признаки, используемые моделью
#     data = data[required_columns]  # Оставляем только нужные признаки

#     for _ in range(forecast_steps):
#         features = data.tail(1).values.flatten()
#         prediction = model.predict([features])[0]
#         future_prices.append(prediction)

#         # Добавляем новый ряд с корректным индексом
#         new_index = last_index + 1
#         new_row = pd.DataFrame({col: prediction for col in required_columns}, index=[new_index])
#         data = pd.concat([data, new_row], ignore_index=False)
#         last_index = new_index

#     return future_prices

# def generate_signals(data, future_prices):
#     signals = []
#     current_price = data['close'].iloc[-1]
#     for price in future_prices:
#         if price > current_price:
#             signals.append(1)  # Покупка
#         else:
#             signals.append(-1)  # Продажа
#     return signals

# class STAML1_LR1(BaseTABitget):
#     def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
#         super().__init__(symbol, granularity, productType, n_parts, period)
#         self.model = None
#         self.forecast_steps = period
#     def fit_model(self, data):
#         X, y = prepare_forecast_data(data, self.forecast_steps)
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
#         self.model = fit_model(X_train, y_train)

#     def preprocessing(self, df):
#         if self.model is None:
#             self.fit_model(df)

#         future_prices = predict_future_prices(self.model, df, self.forecast_steps)
#         signals = generate_signals(df, future_prices)
#         df['signal'] = signals

#         df = add_enter_price2close(df)
#         df = add_slice_df(df,self.period)
#         return df
    
#     def __call__(self, row, *args, **kwds):
#         if row['signal'] == 1:
#             return 'long_pw'
#         if row['signal'] == -1:
#             return 'short_pw'

# Предсказывает прямую линию...
# D 
class STAML1_ARIMAS1(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, arima_order=(2, 1, 2), forecast_steps=10,n_percent=0.1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.order = arima_order
        self.forecast_steps = forecast_steps
        self.n_percent = n_percent
        self.model_high = None
        self.model_low = None

    def fit_model(self, data):
        try:
            model_arima = ARIMA(data['high'], order=self.order)
            self.model_high = model_arima.fit()
            model_arima = ARIMA(data['low'], order=self.order)
            self.model_low = model_arima.fit()
        except Exception as e:
            print(f"Error while fitting ARIMA model: {e}")

    def preprocessing(self, df):
        # if self.model is None:
        self.fit_model(df)

        forecast = self.model_high.forecast(steps=self.forecast_steps)
        shift_index = forecast.index - self.forecast_steps
        forecast = pd.Series(forecast.values,index=shift_index)
        df['arima_forecast_high'] = forecast + df['high'].std() * self.n_percent
        forecast = self.model_low.forecast(steps=self.forecast_steps)
        shift_index = forecast.index - self.forecast_steps
        forecast = pd.Series(forecast.values,index=shift_index)
        df['arima_forecast_low'] = forecast - df['low'].std() * self.n_percent
        df['signal'] = 0

        # Простое правило: покупаем, если прогнозируемый close больше текущего open
        df.loc[(df['arima_forecast_low'] > df['close']), 'signal'] = 1
        df.loc[(df['arima_forecast_high'] < df['close']), 'signal'] = -1
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'
# TODO period, low, high
# BD 
class STAML1_PROPHET1(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, forecast_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.forecast_steps = forecast_steps
        self.model = None

    def fit_model(self, data):
        start_date = '2023-01-01'  # Произвольная начальная точка
        data['ds'] = pd.date_range(start=start_date, periods=len(data), freq='D')
        prophet_data = data.reset_index()
        prophet_data.rename(columns={'close': 'y'}, inplace=True)
        try:
            model_prophet = Prophet()
            self.model = model_prophet.fit(prophet_data)
        except Exception as e:
            print(f"Error while fitting Prophet model: {e}")

    def preprocessing(self, df):
        # if self.model is None:
        self.fit_model(df)

        future = self.model.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model.predict(future)
        df['prophet_forecast'] = forecast['yhat']
        df['signal'] = 0

        # Простое правило: покупаем, если прогнозируемый close больше текущего open
        df.loc[(df['prophet_forecast'] > df['close']), 'signal'] = 1
        df.loc[(df['prophet_forecast'] < df['close']), 'signal'] = -1
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'
class STAML1_PROPHET1s(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, forecast_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.forecast_steps = forecast_steps
        self.model = None

    def fit_model(self, data):
        start_date = '2023-01-01'  # Произвольная начальная точка
        data['ds'] = pd.date_range(start=start_date, periods=len(data), freq='D')
        prophet_data = data.reset_index()
        prophet_data.rename(columns={'close': 'y'}, inplace=True)
        try:
            model_prophet = Prophet()
            self.model = model_prophet.fit(prophet_data)
        except Exception as e:
            print(f"Error while fitting Prophet model: {e}")

    def preprocessing(self, df):
        # if self.model is None:
        self.fit_model(df)

        future = self.model.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model.predict(future)
        forecast = forecast.iloc[self.forecast_steps:]
        forecast = forecast.reset_index(drop=True)
        df['prophet_forecast'] = forecast['yhat']
        df['signal'] = 0

        # Простое правило: покупаем, если прогнозируемый close больше текущего open
        df.loc[(df['prophet_forecast'] > df['close']), 'signal'] = 1
        df.loc[(df['prophet_forecast'] < df['close']), 'signal'] = -1
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'

#D Предсказание канала дончана   
class STAML1_PROPHET2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, forecast_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.forecast_steps = forecast_steps
        self.model_high = None
        self.model_low = None

    def fit_model(self, data):
        start_date = '2023-01-01'  # Произвольная начальная точка
        data['ds'] = pd.date_range(start=start_date, periods=len(data), freq='D')
        prophet_data_high = data.reset_index()
        prophet_data_high.rename(columns={'max_hb': 'y'}, inplace=True)
        prophet_data_low = data.reset_index()
        prophet_data_low.rename(columns={'min_hb': 'y'}, inplace=True)
        try:
            model_prophet_high = Prophet()
            self.model_high = model_prophet_high.fit(prophet_data_high)
            model_prophet_low = Prophet()
            self.model_low = model_prophet_low.fit(prophet_data_low)
        except Exception as e:
            print(f"Error while fitting Prophet model: {e}")

    def preprocessing(self, df):
        # if self.model is None:
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        self.fit_model(df)

        future = self.model_high.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_high.predict(future)
        df['prophet_forecast_high'] = forecast['yhat']
        future = self.model_low.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_low.predict(future)
        df['prophet_forecast_low'] = forecast['yhat']
        df['signal'] = 0

        # Простое правило: покупаем, если прогнозируемый close больше текущего open
        df.loc[(df['prophet_forecast_low'] > df['close']), 'signal'] = 1
        df.loc[(df['prophet_forecast_high'] < df['close']), 'signal'] = -1
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'
        
class STAML1_PROPHET2s(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, forecast_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.forecast_steps = forecast_steps
        self.model_high = None
        self.model_low = None

    def fit_model(self, data):
        start_date = '2023-01-01'  # Произвольная начальная точка
        data['ds'] = pd.date_range(start=start_date, periods=len(data), freq='D')
        prophet_data_high = data.reset_index()
        prophet_data_high.rename(columns={'max_hb': 'y'}, inplace=True)
        prophet_data_low = data.reset_index()
        prophet_data_low.rename(columns={'min_hb': 'y'}, inplace=True)
        try:
            model_prophet_high = Prophet()
            self.model_high = model_prophet_high.fit(prophet_data_high)
            model_prophet_low = Prophet()
            self.model_low = model_prophet_low.fit(prophet_data_low)
        except Exception as e:
            print(f"Error while fitting Prophet model: {e}")

    def preprocessing(self, df):
        # if self.model is None:
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        self.fit_model(df)

        future = self.model_high.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_high.predict(future)
        forecast = forecast.iloc[self.forecast_steps:]
        forecast = forecast.reset_index(drop=True)
        df['prophet_forecast_high'] = forecast['yhat']
        future = self.model_low.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_low.predict(future)
        forecast = forecast.iloc[self.forecast_steps:]
        forecast = forecast.reset_index(drop=True)
        df['prophet_forecast_low'] = forecast['yhat']
        df['signal'] = 0

        # Простое правило: покупаем, если прогнозируемый close больше текущего open
        df.loc[(df['prophet_forecast_low'] > df['close']), 'signal'] = 1
        df.loc[(df['prophet_forecast_high'] < df['close']), 'signal'] = -1
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'
        
# D по хаям и лоям с n-процента добавлением стандартного отклонения
class STAML1_PROPHET3(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, forecast_steps=10,n_percent=0.25):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.forecast_steps = forecast_steps
        self.n_percent = n_percent
        self.model_high = None
        self.model_low = None

    def fit_model(self, data):
        start_date = '2023-01-01'  # Произвольная начальная точка
        data['ds'] = pd.date_range(start=start_date, periods=len(data), freq='D')
        prophet_data_high = data.reset_index()
        prophet_data_high.rename(columns={'high': 'y'}, inplace=True)
        prophet_data_low = data.reset_index()
        prophet_data_low.rename(columns={'low': 'y'}, inplace=True)
        try:
            model_prophet_high = Prophet()
            self.model_high = model_prophet_high.fit(prophet_data_high)
            model_prophet_low = Prophet()
            self.model_low = model_prophet_low.fit(prophet_data_low)
        except Exception as e:
            print(f"Error while fitting Prophet model: {e}")

    def preprocessing(self, df):
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        self.fit_model(df)

        future = self.model_high.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_high.predict(future) 
        df['prophet_forecast_high'] = forecast['yhat'] + df['high'].std() * self.n_percent
        future = self.model_low.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_low.predict(future) 
        df['prophet_forecast_low'] = forecast['yhat'] - df['high'].std() * self.n_percent
        df['signal'] = 0

        # Простое правило: покупаем, если прогнозируемый close больше текущего open
        df.loc[(df['prophet_forecast_low'] > df['close']), 'signal'] = 1
        df.loc[(df['prophet_forecast_high'] < df['close']), 'signal'] = -1
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'
class STAML1_PROPHET3s(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, forecast_steps=10,n_percent=0.25):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.forecast_steps = forecast_steps
        self.n_percent = n_percent
        self.model_high = None
        self.model_low = None

    def fit_model(self, data):
        start_date = '2023-01-01'  # Произвольная начальная точка
        data['ds'] = pd.date_range(start=start_date, periods=len(data), freq='D')
        prophet_data_high = data.reset_index()
        prophet_data_high.rename(columns={'high': 'y'}, inplace=True)
        prophet_data_low = data.reset_index()
        prophet_data_low.rename(columns={'low': 'y'}, inplace=True)
        try:
            model_prophet_high = Prophet()
            self.model_high = model_prophet_high.fit(prophet_data_high)
            model_prophet_low = Prophet()
            self.model_low = model_prophet_low.fit(prophet_data_low)
        except Exception as e:
            print(f"Error while fitting Prophet model: {e}")

    def preprocessing(self, df):
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        self.fit_model(df)

        future = self.model_high.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_high.predict(future) 
        forecast = forecast.iloc[self.forecast_steps:]
        forecast = forecast.reset_index(drop=True)
        df['prophet_forecast_high'] = forecast['yhat'] + df['high'].std() * self.n_percent
        future = self.model_low.make_future_dataframe(periods=self.forecast_steps, freq='h')
        forecast = self.model_low.predict(future) 
        forecast = forecast.iloc[self.forecast_steps:]
        forecast = forecast.reset_index(drop=True)
        df['prophet_forecast_low'] = forecast['yhat'] - df['high'].std() * self.n_percent
        df['signal'] = 0

        # Простое правило: покупаем, если прогнозируемый close больше текущего open
        df.loc[(df['prophet_forecast_low'] > df['close']), 'signal'] = 1
        df.loc[(df['prophet_forecast_high'] < df['close']), 'signal'] = -1
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'
#долго...   
# class STAML1_SARIMAS1(BaseTABitget):
#     def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, sarima_order=(1, 1, 1), seasonal_order=(0, 1, 1, 24), forecast_steps=10):
#         super().__init__(symbol, granularity, productType, n_parts, period)
#         self.order = sarima_order
#         self.seasonal_order = seasonal_order
#         self.forecast_steps = forecast_steps
#         self.model_high = None
#         self.model_low = None

#     def fit_model(self, data):
#         try:
#             model_sarima = SARIMAX(data['high'], order=self.order, seasonal_order=self.seasonal_order)
#             self.model_high = model_sarima.fit(disp=False)
#             model_sarima = SARIMAX(data['low'], order=self.order, seasonal_order=self.seasonal_order)
#             self.model_low = model_sarima.fit(disp=False)
#         except Exception as e:
#             print(f"Error while fitting SARIMA model: {e}")

#     def preprocessing(self, df):
#         # if self.model is None:
#         self.fit_model(df)

#         forecast = self.model_high.forecast(steps=self.forecast_steps)
#         shift_index = forecast.index - self.forecast_steps
#         forecast = pd.Series(forecast.values, index=shift_index)
#         df['sarima_forecast_high'] = forecast
#         forecast = self.model_low.forecast(steps=self.forecast_steps)
#         shift_index = forecast.index - self.forecast_steps
#         forecast = pd.Series(forecast.values, index=shift_index)
#         df['sarima_forecast_low'] = forecast
#         df['signal'] = 0

#         # Простое правило: покупаем, если прогнозируемый close больше текущего open
#         df.loc[(df['sarima_forecast_high'] < df['close']), 'signal'] = -1
#         df.loc[(df['sarima_forecast_low'] > df['close']), 'signal'] = 1
#         df = add_enter_price2close(df)
#         df = add_slice_df(df, self.period)
#         return df

#     def __call__(self, row, *args, **kwargs):
#         if row['signal'] == 1:
#             return 'long_pw'
#         elif row['signal'] == -1:
#             return 'short_pw'


# Предсказывает прямую линию...
# class STAML1_VARMAS1(BaseTABitget):
#     def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, varma_order=(1, 0), forecast_steps=10):
#         super().__init__(symbol, granularity, productType, n_parts, period)
#         self.order = varma_order
#         self.forecast_steps = forecast_steps
#         self.model = None

#     def fit_model(self, data):
#         subset_data = data.sample(frac=0.1)
#         try:
#             model_varma = VARMAX(subset_data[['close','volume']], order=self.order)
#             self.model = model_varma.fit(maxiter=10,disp=False)
#         except Exception as e:
#             print(f"Error while fitting VARMA model: {e}")

#     def preprocessing(self, df):
#         # if self.model is None:
#         self.fit_model(df)

#         forecast = self.model.forecast(steps=self.forecast_steps)

#         forecast_close = pd.Series(forecast['close'].values, index=df.index[-self.forecast_steps:])
#         print(forecast_close)
#         df['varma_forecast'] = forecast_close
#         df['signal'] = 0

#         # Простое правило: покупаем, если прогнозируемый close больше текущего open
#         df.loc[(df['varma_forecast'] > df['close']), 'signal'] = -1
#         df.loc[(df['varma_forecast'] < df['close']), 'signal'] = 1
#         df = add_enter_price2close(df)
#         df = add_slice_df(df, self.period)
#         return df

#     def __call__(self, row, *args, **kwargs):
#         if row['signal'] == 1:
#             return 'long_pw'
#         elif row['signal'] == -1:
#             return 'short_pw'