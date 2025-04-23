import numpy as np
import  matplotlib.pyplot as plt
import pandas as pd
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_ema,add_enter_price2close,add_rsi,add_chop,add_rsi_tw,add_cci,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_adx,add_donchan_channel,add_sma
from ForBots.Indicators.pva_indicators import add_velcro_indicator,add_pc_stair_fast,add_static_channel

class LTA2_MONSTER(BaseTABitget):
    """period=20,threshold=30,period2=10,shift=2,period_adx=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30,period2=10,shift=2,period_adx=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.period2 = period2
        self.shift = shift
        self.period_adx = period_adx
    def preprocessing(self, df):
        df = add_adx(df,self.period_adx)
        df['sma_adx'] = df['adx'].rolling(self.period).mean()
        df = add_donchan_channel(df,self.period2)
        df['stop_long'] = df['low'].shift(self.shift)
        df['stop_short'] = df['high'].shift(self.shift)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if self.threshold < row['adx'] > row['sma_adx']:
            if row['high'] == row['max_hb']:
                return 'long_pw'
            if row['low'] == row['min_hb']:
                return 'short_pw'
            if row['close'] < row['stop_long']:
                return 'close_long_pw'
            if row['close'] > row['stop_short']:
                return 'close_short_pw'
        return 'close_all_pw'
    
class LTA2_OVERLORD(BaseTABitget):
    """period=60,period2=20,period3=10,shift=2"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,period2=20,period3=10,shift=2):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.shift = shift
    def preprocessing(self, df):
        df = add_ema(df,self.period)
        df = add_chop(df,self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df['smab'] = df['chop'].rolling(window=self.period).mean()
        df['stop_long'] = df['low'].shift(self.shift)
        df['stop_short'] = df['high'].shift(self.shift)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['smab'] > row['sma'] < row['sma2']: 
            if row['close'] > row['stop_short']:
                if row['close'] > row['ema']:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
            if row['close'] < row['stop_long']:
                if row['close'] < row['ema']:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
        else:
            if row['close'] > row['stop_short']:
                return 'close_short_pw'
            if row['close'] < row['stop_long']:
                return 'close_long_pw'
            
# TODO
class LTA2_HARDWAY(BaseTABitget):
    """period=60,threshold=30,period2=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df:pd.DataFrame):
        df = add_donchan_channel(df,self.period)
        df = add_velcro_indicator(df,self.period)
        # df['hw'] = df['velcro'].diff().rolling(3).sum()
        df['s_velcro'] = df['velcro'].rolling(10).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['velcro'] > row['s_velcro']:
            return 'long_pw'
        else:
            return 'short_pw'
# TODO
class LTA2_BLAST(BaseTABitget):
    """period=60,threshold=30,period2=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,n_stairs=10,period2=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_stairs = n_stairs
        self.period2 = period2
    def preprocessing(self, df:pd.DataFrame):
        df = add_pc_stair_fast(df,self.n_stairs,self.period2)
        df['stair_s'] = df['stair'].rolling(self.period).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['open'] > row['stair_s'] < row['close']:
            return 'long_pw'
        if row['open'] < row['stair_s'] > row['close']:
            return 'short_pw'
        
class LTA2_LOGAN(BaseTABitget):
    """period=100,period2=50,threshold=50"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,period2=50,threshold=50):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.threshold = threshold
    def preprocessing(self, df:pd.DataFrame):
        df = add_static_channel(df,self.period)
        df = add_chop(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['chop'] > self.threshold:
            if row['top_line'] < row['close']:
                return 'short_pw'
            if row['bottom_line'] > row['close']:
                return 'long_pw'
            if row['center_line'] > row['close']:
                return 'close_short_pw'
            if row['center_line'] < row['close']:
                return 'close_long_pw'
        else:
            return 'close_all_pw'