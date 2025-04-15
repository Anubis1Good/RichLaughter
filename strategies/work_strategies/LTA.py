import numpy as np
import  matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price,add_ema,add_stochastic,add_atr,add_local_extrema,add_enter_price2close,add_supertrend,add_rsi,add_chop,add_rsi_tw,add_cci,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo
from ForBots.Indicators.price_funcs import get_universal_r,get_universal
from utils.help_trades import reverse_action
#D Похоже на WDDCr
class LTA_LAKSA(BaseTABitget):
    """period=20,period2=5"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period2=5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
    def preprocessing(self, df):
        df = add_ema(df,self.period)
        df = add_local_extrema(df,self.period2)

        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['close'] == df['local_min']) & (df['close'] > df['ema']), 'signal'] = 1  # Покупка
        df.loc[(df['close'] == df['local_max']) & (df['close'] < df['ema']), 'signal'] = -1 

        df = add_enter_price2close(df)
        max_period = max(self.period,self.period2)
        df = add_slice_df(df,max_period)
        # df[df['signal'] != 0].info()
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
#D Похоже на WDDCr + work
class LTA_LAKSAe(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period2=5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
    def preprocessing(self, df):
        df = add_ema(df,self.period)
        df = add_local_extrema(df,self.period2)
        df['nearest_long'] = df['high'] - df['close'] > df['close'] - df['low'] 
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['low'] <= df['local_min']) & (df['close'] > df['ema']) & (df['nearest_long'] == True), 'signal'] = 1  # Покупка
        df.loc[(df['high'] >= df['local_max']) & (df['close'] < df['ema'])& (df['nearest_long'] == False), 'signal'] = -1 

        df = add_enter_price2close(df)
        max_period = max(self.period,self.period2)
        df = add_slice_df(df,max_period)
        # df[df['signal'] != 0].info()
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'

#D Выделение уровней поддержки и сопротивления с помощью кластеризации. 
class LTA_TOMYAM(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)

    def preprocessing(self, df):
        kmeans = KMeans(n_clusters=3)
        df['cluster'] = kmeans.fit_predict(df[['close']])

        support_levels = df.groupby('cluster')['close'].min().values
        resistance_levels = df.groupby('cluster')['close'].max().values
        for i in range(1, len(df)):
            close = df.loc[i, 'close']
            # Проверка на покупку (цена вблизи поддержки и начинает расти)
            for level in support_levels:
                    df.loc[i, 'signal'] = 1  # Покупка
            # Проверка на продажу (цена вблизи сопротивления и начинает падать)
            for level in resistance_levels:
                if close > level:  # Порог 1 для "близости"
                    df.loc[i, 'signal'] = -1  # Продажа

        # Убираем повторяющиеся сигналы
        df['signal'] = df['signal'].replace(to_replace=0, method='ffill')

        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df

    def __call__(self, row, *args, **kwargs):
        if row['signal'] == 1:
            return 'long_pw'
        elif row['signal'] == -1:
            return 'short_pw'

#D Выделение уровней поддержки и сопротивления с помощью кластеризации  за период. 
class LTA_RAMEN(BaseTABitget):
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
#BD Изменение супертренда
class LTA_PHOBO(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=10,multiplier=3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_supertrend(df,self.period,self.multiplier)
        df = add_enter_price2close(df)
        df['signal'] = 0
        # Генерация сигналов
        for i in range(1, len(df)):
            if df['in_uptrend'].iloc[i] and not df['in_uptrend'].iloc[i - 1]:
                df.loc[df.index[i], 'signal'] = 1  # Покупать
            elif not df['in_uptrend'].iloc[i] and df['in_uptrend'].iloc[i - 1]:
                df.loc[df.index[i], 'signal'] = -1  # Продавать
        df = add_slice_df(df,self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
#D reverse PHOBO   
class LTA_APHOBO(LTA_PHOBO):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
# TODO
class LTA_WAPHOBO(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,multiplier=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_supertrend(df,self.period,self.multiplier)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df['signal'] = 0
        # Генерация сигналов
        for i in range(1, len(df)):
            if df['in_uptrend'].iloc[i] and not df['in_uptrend'].iloc[i - 1]:
                df.loc[df.index[i], 'signal'] = 1  # Покупать
            elif not df['in_uptrend'].iloc[i] and df['in_uptrend'].iloc[i - 1]:
                df.loc[df.index[i], 'signal'] = -1  # Продавать
        df = add_slice_df(df,self.period)
        plt.plot(df['supertrend'])
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['in_uptrend'] and row['rsi'] < 30:
            return 'long_pw'
        if not row['in_uptrend'] and row['rsi'] > 70:
            return 'short_pw'
        if row['rsi'] < 30:
            return 'close_short_pw'
        if row['rsi'] > 70:
            return 'close_long_pw'
# BD PHOBO c фильтрацией по объему
class LTA_PHOGA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=10,multiplier=3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_supertrend(df,self.period,self.multiplier)
        df = add_enter_price2close(df)
        mean_volume = df['volume'].mean()
        df['signal'] = 0

        for i in range(1, len(df)):
            if df['in_uptrend'].iloc[i] and not df['in_uptrend'].iloc[i - 1] and df['volume'].iloc[i] > mean_volume:
                df.loc[df.index[i], 'signal'] = 1  # Покупать
            elif not df['in_uptrend'].iloc[i] and df['in_uptrend'].iloc[i - 1] and df['volume'].iloc[i] > mean_volume:
                df.loc[df.index[i], 'signal'] = -1  # Продавать
        df = add_slice_df(df,self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
#D reverse PHOGA          
class LTA_APHOGA(LTA_PHOGA):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
    
#BD По сути BDCC только с фильтрацией
class LTA_BORSCH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,momentum_period=14):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.momentum_period = momentum_period
        self.lookback_period = period
    def preprocessing(self, df):
 # Расчёт момента (momentum)
        # df['momentum'] = df['close'].pct_change(periods=self.momentum_period) * 100

        # Добавление уровней недавних максимумов и минимумов
        df['recent_max'] = df['high'].rolling(window=self.lookback_period).max()
        df['recent_min'] = df['low'].rolling(window=self.lookback_period).min()

        # Фильтр по объёму
        mean_volume = df['volume'].mean()
        df['above_avg_volume'] = df['volume'] > mean_volume

        # Добавление сигнала
        df['signal'] = 0

        # Генерация сигналов
        for i in range(len(df)):

            if df['close'].iloc[i] > df['recent_max'].iloc[i-1] and df['above_avg_volume'].iloc[i]:
                df.loc[df.index[i], 'signal'] = 1
            elif df['close'].iloc[i] < df['recent_min'].iloc[i-1] and df['above_avg_volume'].iloc[i]:
                df.loc[df.index[i], 'signal'] = -1

        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
#BD Ишимоку  
class LTA_MISO(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=52,tenkan_period=9, kijun_period=26, senkou_span_b_period=52,rsi_period=14, macd_fast=12, macd_slow=26, macd_signal=9):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_span_b_period = senkou_span_b_period
        self.rsi_period = rsi_period
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
    def preprocessing(self, df):
        # Расчёт Tenkan-sen (период 9)
        df['tenkan_sen'] = (df['high'].rolling(window=self.tenkan_period).max() + df['low'].rolling(window=self.tenkan_period).min()) / 2

        # Расчёт Kijun-sen (период 26)
        df['kijun_sen'] = (df['high'].rolling(window=self.kijun_period).max() + df['low'].rolling(window=self.kijun_period).min()) / 2

        # Расчёт Senkou Span A (середина между Tenkan-sen и Kijun-sen, смещённая вперёд на 26 периодов)
        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(self.kijun_period)

        # Расчёт Senkou Span B (среднее значение максимальной и минимальной цены за последние 52 периода, смещённое вперёд на 26 периодов)
        df['senkou_span_b'] = ((df['high'].rolling(window=self.senkou_span_b_period).max() + df['low'].rolling(window=self.senkou_span_b_period).min()) / 2).shift(self.kijun_period)

        # Расчёт Chikou Span (цена закрытия, смещённая назад на 26 периодов)
        df['chikou_span'] = df['close'].shift(-self.kijun_period)

        # Фильтр по объёму
        df['relative_volume'] = df['volume'] / df['volume'].rolling(window=10).mean()
        df['strong_volume'] = df['relative_volume'] > 1.5  # Объём превышает среднее значение на 50%

        # Расчёт RSI
        delta = df['close'].diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        rs = up.ewm(alpha=1/self.rsi_period, adjust=False).mean() / down.ewm(alpha=1/self.rsi_period, adjust=False).mean()
        df['rsi'] = 100 - (100 / (1 + rs))

        # Расчёт MACD
        ema_fast = df['close'].ewm(span=self.macd_fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.macd_slow, adjust=False).mean()
        df['macd'] = ema_fast - ema_slow
        df['signal_line'] = df['macd'].ewm(span=self.macd_signal, adjust=False).mean()

        # Генерация сигналов
        df['signal'] = 0
        for i in range(1, len(df)):
            # Пересечения Tenkan-sen и Kijun-sen
            if df['tenkan_sen'].iloc[i] > df['kijun_sen'].iloc[i] and df['tenkan_sen'].iloc[i - 1] < df['kijun_sen'].iloc[i - 1] and df['strong_volume'].iloc[i]:
                # Бычий сигнал
                if df['close'].iloc[i] > df['senkou_span_a'].iloc[i] and df['close'].iloc[i] > df['senkou_span_b'].iloc[i] and df['rsi'].iloc[i] < 70 and df['macd'].iloc[i] > df['signal_line'].iloc[i]:
                    df.loc[df.index[i], 'signal'] = 1  # Покупка
            elif df['tenkan_sen'].iloc[i] < df['kijun_sen'].iloc[i] and df['tenkan_sen'].iloc[i - 1] > df['kijun_sen'].iloc[i - 1] and df['strong_volume'].iloc[i]:
                # Медвежий сигнал
                if df['close'].iloc[i] < df['senkou_span_a'].iloc[i] and df['close'].iloc[i] < df['senkou_span_b'].iloc[i] and df['rsi'].iloc[i] > 30 and df['macd'].iloc[i] < df['signal_line'].iloc[i]:
                    df.loc[df.index[i], 'signal'] = -1  # Продажа

        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'

class LTA_OKROSHKA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,period_chop=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period_chop = period_chop
    def preprocessing(self, df):
        df = add_rsi(df,self.period)
        df = add_chop(df,self.period_chop)
        df = add_enter_price2close(df)  
        period = max(self.period,self.period_chop)
        df = add_slice_df(df, period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):
        threshold = 30
        if 60 > row['chop'] > 45:
            threshold = 30
        elif row['chop'] > 60:
            threshold = 25
        elif 45 > row['chop'] > 30:
            threshold = 20
        else:
            threshold = 10
        if row['rsi'] < threshold:  
            return 'long_pw'
        if row['rsi'] > 100-threshold:  
            return 'short_pw'
        
class LTA_OKROSHKA2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,period_chop=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period_chop = period_chop
    def preprocessing(self, df):
        df = add_rsi_tw(df,self.period)
        df = add_chop(df,self.period_chop)
        df = add_enter_price2close(df)  
        period = max(self.period,self.period_chop)
        df = add_slice_df(df, period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):
        threshold = 30
        if 60 > row['chop'] > 45:
            threshold = 30
        elif row['chop'] > 60:
            threshold = 25
        elif 45 > row['chop'] > 30:
            threshold = 20
        else:
            threshold = 10
        if row['rsi_tw'] < threshold:  
            return 'long_pw'
        if row['rsi_tw'] > 100-threshold:  
            return 'short_pw'
        
class LTA_KROSH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_rsi(df,self.period)

        df = add_enter_price2close(df)  

        df = add_slice_df(df, self.period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):
        if row['rsi'] < self.threshold:  
            return 'long_pw'
        if row['rsi'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_KARYCH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_rsi_tw(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['rsi_tw'] < self.threshold:  
            return 'long_pw'
        if row['rsi_tw'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_SAVUNIA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_williams_r(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['williams_r'] < -100+self.threshold:  
            return 'long_pw'
        if row['williams_r'] > 0-self.threshold:  
            return 'short_pw'
        
class LTA_NUSHA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_mfi(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['mfi'] < self.threshold:  
            return 'long_pw'
        if row['mfi'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_KOPATYCH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=40):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_ultimate_oscillator(df,self.period//3,self.period//2,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['ultimate_oscillator'] < self.threshold:  
            return 'long_pw'
        if row['ultimate_oscillator'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_LOSYASH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=40):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_cmo(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['cmo'] < -100+self.threshold:  
            return 'long_pw'
        if row['cmo'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_BARASH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_cci(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['cci'] < -200+self.threshold:  
            return 'long_pw'
        if row['cci'] > 200-self.threshold:  
            return 'short_pw'
        
class LTA_EJIK(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,period2=3,threshold=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_stochastic(df,self.period,self.period2)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['%k'] > row['%d'] < self.threshold:  
            return 'long_pw'
        if row['%k'] < row['%d'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_PIN(BaseTABitget):
    'period=15,period2=3,threshold=30,solution = 5'
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,period2=3,threshold=30,solution = 5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.threshold = threshold
        self.solution = solution
    def preprocessing(self, df):
        df = add_rsi(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_williams_r(df,self.period)
        df = add_mfi(df,self.period)
        df = add_ultimate_oscillator(df,self.period//3,self.period//2,self.period)
        df = add_cmo(df,self.period)
        df = add_cci(df,self.period)
        df = add_stochastic(df,self.period,self.period2)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        pins_solution = 0
        if row['rsi'] < self.threshold:  
            pins_solution += 1
        if row['rsi_tw'] < self.threshold:  
            pins_solution += 1
        if row['williams_r'] < -100+self.threshold:  
            pins_solution += 1
        if row['mfi'] < self.threshold:  
            pins_solution += 1
        if row['ultimate_oscillator'] < self.threshold+10:  
            pins_solution += 1
        if row['cmo'] < -100+self.threshold+10:  
            pins_solution += 1
        if row['cci'] < -200+self.threshold:  
            pins_solution += 1
        if row['%k'] > row['%d'] < self.threshold:  
            pins_solution += 1
        if row['rsi'] > 100-self.threshold:  
            pins_solution -= 1
        if row['rsi_tw'] > 100-self.threshold:  
            pins_solution -= 1
        if row['williams_r'] > 0-self.threshold:  
            pins_solution -= 1
        if row['mfi'] > 100-self.threshold:  
            pins_solution -= 1
        if row['ultimate_oscillator'] > 100-self.threshold-10:  
            pins_solution -= 1
        if row['cmo'] > 100-self.threshold-10:  
            pins_solution -= 1
        if row['cci'] > 200-self.threshold:  
            pins_solution -= 1
        if row['%k'] < row['%d'] > 100-self.threshold:  
            pins_solution -= 1
        if pins_solution > self.solution:
            return 'long_pw'
        if pins_solution < -self.solution:
            return 'short_pw'
        
        
