import numpy as np
import pandas as pd
from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi,add_enter_price2close,add_macd,add_rsi_tw,add_adx,add_chop,add_kusuruken_channel
from utils.help_trades import reverse_action,chep
from strategies.work_strategies.BaseTA import BaseTABitget


# BD
class PTA10_MAGIC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=26, period2=12, period3=9):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
    def preprocessing(self, df):
        df = add_macd(df,self.period2,self.period,self.period3)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # Покупка
        df.loc[df['macd'] < df['signal_line'], 'signal'] = -1  # Продажа
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class PTA10_WIZARD(BaseTABitget):
    'period=26, period2=12, period3=9,threshold=20,threshold_adx=20'
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=26, period2=12, period3=9,threshold=20,threshold_adx=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.threshold = threshold
        self.threshold_adx = threshold_adx
    def preprocessing(self, df):
        df = add_macd(df,self.period2,self.period,self.period3)
        df = add_adx(df,self.period2)
        df = add_rsi_tw(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # Покупка
        df.loc[df['macd'] < df['signal_line'], 'signal'] = -1  # Продажа
        return df
    def __call__(self, row, *args, **kwds):
        if row['adx'] > self.threshold_adx:
            if row['signal'] == 1 and row['rsi_tw'] < 100-self.threshold:
                return 'long_pw'
            if row['signal'] == -1 and row['rsi_tw'] > self.threshold:
                return 'short_pw'
        if row['rsi_tw'] < self.threshold:
            return 'close_short_pw'
        if row['rsi_tw'] > 100-self.threshold:
            return 'close_long_pw'
        
class PTA10_SORCERER(BaseTABitget):
    'period=26, period2=12, period3=9,threshold=20,period4=12,toffset=10'
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=26, period2=12, period3=9,threshold=20,period4=12,toffset=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.period4 = period4
        self.threshold = threshold
        self.toffset = toffset
    def preprocessing(self, df):
        df = add_macd(df,self.period,self.period2,self.period3)
        df = add_rsi(df,self.period3)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # Покупка
        df.loc[df['macd'] < df['signal_line'], 'signal'] = -1  # Продажа
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1 and row['rsi'] < self.threshold:
            return 'long_pw'
        if row['signal'] == -1 and row['rsi'] > 100-self.threshold:
            return 'short_pw'
        if row['rsi'] < 100-self.threshold-self.toffset:
            return 'close_short_pw'
        if row['rsi'] > self.threshold+self.toffset:
            return 'close_long_pw'
        
class PTA11_KUSURUKEN(BaseTABitget):
    """period=60, period2=10, period3=20,threshold=20, kind_enter='hl'
    kind_enter -> hl | c
    """
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60, period2=10, period3=20,threshold=20,kind_enter='hl'):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.threshold = threshold
        self.kind_enter_l = 'low' if kind_enter == 'hl' else 'close'
        self.kind_enter_s = 'high' if kind_enter == 'hl' else 'close'
    def preprocessing(self, df):
        df = add_kusuruken_channel(df,self.period2,self.period)
        df = add_rsi(df,self.period3)
        df = add_chop(df,self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        # trend_context
        if row['sma'] > row['sma2']: 
            # long_context
            if row["avarege"] > row['avarege2']:
                if row['rsi'] > 100-self.threshold+10:
                    return 'close_long_pw'
                if row[self.kind_enter_l] <= row['avarege2']:
                    return 'long_pw'
            # short_context
            else:
                if row['rsi'] < self.threshold-10:
                    return 'close_short_pw'
                if row[self.kind_enter_s] >= row['avarege2']:
                    return 'short_pw'
        # range_context
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
            if row['low'] == row['min_hb']:
                if nearest_long:
                    if row['rsi'] < self.threshold:
                        return 'long_pw'
            if row['high'] == row['max_hb']:
                if row['rsi'] > 100-self.threshold:
                    return 'short_pw'

class PTA12_SWDDCr(BaseTABitget):
    """period=20,threshold=30,stop=1,shift=10,rolling=10"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30,stop=1,shift=10,rolling=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.stop = stop
        self.shift = shift
        self.rolling = rolling
    def preprocessing(self, df:pd.DataFrame):
        df = add_donchan_channel(df,self.period)
        df['buffer'] = (df['max_hb'] - df['min_hb']) * self.stop
        df['stop_long'] = (df['min_hb'] - df['buffer']).shift(self.shift).rolling(self.rolling).mean().rolling(self.rolling).min()
        df['stop_short'] = (df['max_hb'] + df['buffer']).shift(self.shift).rolling(self.rolling).mean().rolling(self.rolling).max()
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['close'] < row['stop_long']:
            return 'close_all_pw'
        if row['close'] > row['stop_short']:
            return 'close_all_pw'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
#TODO действует только в сторону тренда    
class PTA13_DWDDCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30,stop=1,shift=10,rolling=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.stop = stop
        self.shift = shift
        self.rolling = rolling
    def preprocessing(self, df:pd.DataFrame):
        df = add_donchan_channel(df,self.period)
        df['buffer'] = (df['max_hb'] - df['min_hb']) * self.stop
        df['stop_long'] = (df['min_hb'] - df['buffer']).shift(self.shift).rolling(self.rolling).mean().rolling(self.rolling).min()
        df['stop_short'] = (df['max_hb'] + df['buffer']).shift(self.shift).rolling(self.rolling).mean().rolling(self.rolling).max()
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['close'] < row['stop_long']:
            return 'close_all_pw'
        if row['close'] > row['stop_short']:
            return 'close_all_pw'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class PTA14_RWDDCr(BaseTABitget):
    """period=20,threshold=30,period2=10, period3=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30,period2=10, period3=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.period2 = period2
        self.period3 = period3
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_chop(df,self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['sma'] > row['sma2']: 
            return 'close_all_pw'
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
            if row['low'] == row['min_hb']:
                if nearest_long:
                    if row['rsi'] < self.threshold:
                        return 'long_pw'
            if row['high'] == row['max_hb']:
                if row['rsi'] > 100-self.threshold:
                    return 'short_pw'
                
class PTA15_NOVA(BaseTABitget):
    """period=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df:pd.DataFrame):
        # df = add_donchan_channel(df,self.period)
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)

        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if not np.isnan(row['end_up']):
            return 'short_pw'
        if not np.isnan(row['end_down']):
            return 'long_pw'
        
class PTA15_KERRIGAN(BaseTABitget):
    """period=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df:pd.DataFrame):
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)

        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['low'] < row['min_hb']:
            return 'close_long_pw'
        if row['high'] > row['max_hb']:
            return 'close_short_pw'
        if not np.isnan(row['end_up']):
            return 'short_pw'
        if not np.isnan(row['end_down']):
            return 'long_pw'

class PTA15_WIDOWMAKER(BaseTABitget):
    """period=20,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df:pd.DataFrame):
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df = add_rsi(df,self.period)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if not np.isnan(row['end_down']):
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if not np.isnan(row['end_up']):
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'