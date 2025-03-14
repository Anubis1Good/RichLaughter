import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price,add_enter_price2close,add_rsi,add_donchan_channel
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

class ExpBot(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold  # Порог для RSI и других условий

    def find_local_extremes(self, df, window=10):
        """
        Находит локальные максимумы и минимумы в пределах скользящего окна.
        """
        df['local_max'] = df['high'].rolling(window=window).max()  # Локальные максимумы
        df['local_min'] = df['low'].rolling(window=window).min()  # Локальные минимумы
        return df

    def preprocessing(self, df):
        """
        Добавляем необходимые индикаторы:
        - Локальные максимумы и минимумы
        - Уровни Фибоначчи
        - Тренд (скользящие средние или наклон цены)
        - RSI (для перепроданности/перекупленности)
        - Сигналы на основе уровней Фибоначчи, RSI и тренда
        """
        # Добавляем разницу между ценой входа и закрытия
        df = add_enter_price2close(df)

        # Добавляем срезы данных
        df = add_slice_df(df, period=self.period)

        # Находим локальные максимумы и минимумы
        df = self.find_local_extremes(df, window=self.period)

        # Добавляем уровни Фибоначчи
        df['fib_23.6'] = df['local_max'] - (df['local_max'] - df['local_min']) * 0.236
        df['fib_38.2'] = df['local_max'] - (df['local_max'] - df['local_min']) * 0.382
        df['fib_50.0'] = df['local_max'] - (df['local_max'] - df['local_min']) * 0.5
        df['fib_61.8'] = df['local_max'] - (df['local_max'] - df['local_min']) * 0.618
        df['fib_78.6'] = df['local_max'] - (df['local_max'] - df['local_min']) * 0.786

        # Определяем тренд (например, с помощью скользящей средней)
        df['ma'] = df['close'].rolling(window=self.period).mean()  # Скользящая средняя
        df['trend'] = df['close'] > df['ma']  # True - восходящий тренд, False - нисходящий

        # Добавляем RSI для перепроданности/перекупленности
        df = add_rsi(df, period=self.period)

        # Генерация сигналов
        df['signal'] = self.generate_signals(df)
        # Локальные экстремумы
        plt.plot(df['local_max'], label='Локальные максимумы', linestyle='--', color='red')
        plt.plot(df['local_min'], label='Локальные минимумы', linestyle='--', color='green')

        # Уровни Фибоначчи
        plt.plot(df['fib_23.6'], color='purple', linestyle=':', label='Фибо 23.6%')
        plt.plot(df['fib_38.2'], color='orange', linestyle=':', label='Фибо 38.2%')
        plt.plot(df['fib_50.0'], color='brown', linestyle=':', label='Фибо 50.0%')
        plt.plot(df['fib_61.8'], color='pink', linestyle=':', label='Фибо 61.8%')
        plt.plot(df['fib_78.6'], color='gray', linestyle=':', label='Фибо 78.6%')

        # Скользящая средняя
        plt.plot(df['ma'], label='Скользящая средняя (MA)', color='cyan', linestyle='-.')
        return df

    def generate_signals(self, df):
        """
        Генерация сигналов на основе:
        - Уровней Фибоначчи
        - Тренда
        - RSI (перепроданность/перекупленность)
        """
        signals = [0] * len(df)  # По умолчанию сигналов нет

        for i in range(1, len(df)):
            row = df.iloc[i]

            # Восходящий тренд (лонг)
            if row['trend']:  # Если тренд восходящий
                if row['close'] <= row['fib_61.8']:  # Цена ниже уровня Фибо 38.2%
                    signals[i] = 1  # Сигнал на покупку (лонг)
                elif row['rsi'] > 70:  # Перекупленность (выход из лонга)
                    signals[i] = 2  # Закрыть лонг

            # Нисходящий тренд (шорт)
            else:  # Если тренд нисходящий
                if row['close'] >= row['fib_38.2']:  # Цена выше уровня Фибо 61.8%
                    signals[i] = -1  # Сигнал на продажу (шорт)
                elif row['rsi'] < 30:  # Перепроданность (выход из шорта)
                    signals[i] = -2  # Закрыть шорт

        return signals

    def __call__(self, row, *args, **kwds):
        """
        Генерация сигналов для выполнения сделок.
        """
        # Сигнал на покупку (лонг)
        if row['signal'] == 1:
            return 'long_pw'  # Сигнал на покупку

        # Сигнал на продажу (шорт)
        if row['signal'] == -1:
            return 'short_pw'  # Сигнал на продажу

        # Закрыть лонг (перекупленность или смена тренда)
        if row['signal'] == 2:
            return 'close_long_pw'

        # Закрыть шорт (перепроданность или смена тренда)
        if row['signal'] == -2:
            return 'close_short_pw'