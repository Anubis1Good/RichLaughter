import os
import json
import numpy as np
import pandas as pd
import warnings
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price
from ForBots.Indicators.price_funcs import get_universal_r,get_universal
from strategies.work_strategies.BaseTA import BaseTABitget
from xgboost import XGBRegressor,Booster,DMatrix,train
from request_functions.download_bitget import download_bitget,create_df
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
        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
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

class STAML1_XGBR5(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=10, period=20,future_steps=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_parts = 10
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
        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
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