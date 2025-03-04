import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price,add_enter_price2close,add_rsi
from strategies.work_strategies.BaseTA import BaseTABitget
import matplotlib.pyplot as plt

class ExpStrategy(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=50,n_clusters = 3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.window_size = period  # Количество последних свечей для анализа
        self.n_clusters = n_clusters
    def find_support_resistance(self,data):
        # Кластеризация
        kmeans = KMeans(n_clusters=self.n_clusters)
        kmeans.fit(data.reshape(-1, 1))
        
        # Определение зон поддержки и сопротивления
        support_levels = np.min(kmeans.cluster_centers_)
        resistance_levels = np.max(kmeans.cluster_centers_)
        
        return support_levels, resistance_levels
    def preprocessing(self, df):
        df['support'] = np.nan
        df['resistance'] = np.nan
        df['signal'] = 0   
        df['stop_loss'] = np.nan 
        for i in range(self.window_size, len(df)):
    # Берем окно данных
            window_data = df['close'].iloc[i - self.window_size:i]
            
            # Находим зоны поддержки и сопротивления
            support_levels, resistance_levels = self.find_support_resistance(window_data.values)
            stop = (resistance_levels - support_levels)
            # Записываем зоны в датафрейм
            df.loc[df.index[i], 'support'] = support_levels
            df.loc[df.index[i], 'resistance'] = resistance_levels
            df.loc[df.index[i], 'stop_long'] = support_levels - stop 
            df.loc[df.index[i], 'stop_short'] = resistance_levels + stop
            
            # Генерация сигналов
            close = df.loc[i, 'close']
            # Проверка на покупку (цена вблизи поддержки и начинает расти)

            if close < support_levels:  # Порог 1 для "близости"
                df.loc[i, 'signal'] = 1  # Покупка
            
            # Проверка на продажу (цена вблизи сопротивления и начинает падать)

            if close > resistance_levels:  # Порог 1 для "близости"
                df.loc[i, 'signal'] = -1  # Продажа

        # Убираем повторяющиеся сигналы
        df['signal'] = df['signal'].replace(to_replace=0, method='ffill')

        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df

    def __call__(self, row, *args, **kwargs):
        if row['stop_long'] > row['close']:
            return 'close_long_pw'
        if row['stop_short'] < row['close']:
            return 'close_short_pw'
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'