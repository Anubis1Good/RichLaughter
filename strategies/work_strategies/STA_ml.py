import numpy as np
import pandas as pd
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price
from ForBots.Indicators.price_funcs import get_universal_r,get_universal
from strategies.work_strategies.BaseTA import BaseTABitget
from xgboost import XGBRegressor
import warnings
# TODO пофиксить ворнинги
warnings.filterwarnings('ignore')
class STAML1_XGBR1(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.future_steps = future_steps
    def preprocessing(self, df):
        future_steps = self.future_steps  # Предсказание на 10 шагов вперёд
        lags = self.period  # Количество лагов для признаков
        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
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
        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
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