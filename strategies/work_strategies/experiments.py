import pandas as pd
import numpy as np
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.ml_indicators import *
from strategies.work_strategies.BaseTA import BaseTABitget
import matplotlib.pyplot as plt

class TemplateBot(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)

    def preprocessing(self, df):

        df = add_enter_price2close(df)  
        df = add_slice_df(df, period=self.period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):

        # Сигнал на покупку (long)
        if row['signal'] == 1:  
            return 'long_pw'  # Сигнал на покупку

        # Сигнал на продажу (short)
        if row['signal'] == -1:  
            return 'short_pw'  # Сигнал на продажу
        
        # так же могут быть 'close_long_pw','close_short_pw'

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

class ToThinkBot(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1,
                 period=200, period2=20, threshold_fr=0.001):
        super().__init__(symbol, granularity, productType, n_parts, period=period)
        self.period2 = period2
        self.threshold_fr = threshold_fr
        self.model = None
        self.scaler = StandardScaler()
        self.volume_ma_window = 50  # Уменьшенное окно для объема

    def preprocessing(self, df: pd.DataFrame):
        # Добавление индикаторов
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = add_adx(df, self.period2)
        df = add_atr(df, self.period2)

        # Нормализация относительно скользящего среднего
        close_ma = df['close'].rolling(self.period2, min_periods=1).mean().shift(1).replace(0, 1e-5)
        volume_ma = df['volume'].rolling(self.volume_ma_window, min_periods=1).mean().replace(0, 1e-5)
        
        # Основные фичи (сохраняем исходные названия)
        df['max_hb'] = df['max_hb'] / close_ma - 1  # Отклонение от нормы в %
        df['min_hb'] = df['min_hb'] / close_ma - 1
        df['avarege'] = df['avarege'] / close_ma - 1
        
        # Добавляем производные фичи
        df['price_change'] = df['close'].pct_change()
        df['volatility'] = df['close'].rolling(5).std() / close_ma
        
        # Целевая переменная
        df['future_return'] = df['close'].pct_change().shift(-5)
        df['signal'] = np.where(df['future_return'] > self.threshold_fr, 1, 
                              np.where(df['future_return'] < -self.threshold_fr, -1, 0))

        # Формируем финальный набор фичей
        features = [
            'max_hb', 'min_hb', 'avarege', 'rsi', 'adx', 'atr',
            'price_change', 'volatility'
        ]
        
        df_train = df.dropna()
        
        # Балансировка классов (если нужно)
        # class_counts = df_train['signal'].value_counts()
        # print(f"Распределение классов:\n{class_counts}")
        
        # Создаем pipeline с нормализацией и моделью
        self.model = make_pipeline(
            StandardScaler(),
            DecisionTreeClassifier()
            # LogisticRegression(
            #     max_iter=1000,
            #     penalty='l2',
            #     C=0.1,  # Сила регуляризации
            #     class_weight='balanced',  # Автобалансировка классов
            #     random_state=42
            # )
        )
        
        try:
            self.model.fit(df_train[features], df_train['signal'])
            # print("Модель успешно обучена!")
        except Exception as e:
            # print(f"Ошибка обучения: {e}")
            return df

        df = add_enter_price2close(df)
        return add_slice_df(df, period=self.period2)

    def __call__(self, row, *args, **kwds):
        if self.model is None:
            return None

        # Подготовка фичей в реальном времени
        current_ma = row['close']  # Упрощенная нормализация для текущего бара
        current_features = pd.DataFrame({
            'max_hb': [(row['max_hb'] / current_ma - 1)],
            'min_hb': [(row['min_hb'] / current_ma - 1)],
            'avarege': [(row['avarege'] / current_ma - 1)],
            'rsi': [row['rsi']],
            'adx': [row['adx']],
            'atr': [row['atr']],
            'price_change': [row['close'] / row['open'] - 1],
            'volatility': [row['atr'] / current_ma]  # Используем ATR как proxy волатильности
        }, index=[0])

        try:
            signal = self.model.predict(current_features)[0]
            if signal == 1:
                return 'long_pw'
            elif signal == -1:
                return 'short_pw'
        except Exception as e:
            # print(f"Ошибка предсказания: {e}")
            pass
        
        return None
    

