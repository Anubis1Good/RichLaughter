import numpy as np
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price,add_ema,add_stochastic,add_atr,add_local_extrema
from ForBots.Indicators.price_funcs import get_universal_r,get_universal

class LTA_LAKSA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period2=5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
    def preprocessing(self, df):
        df = add_ema(df,self.period)
        df = add_local_extrema(df,self.period2)

        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['close'] == df['local_min']) & (df['close'] > df['ema']), 'signal'] = 1  # Покупка
        df.loc[(df['close'] == df['local_max']) & (df['close'] < df['ema']), 'signal'] = -1 

        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
        max_period = max(self.period,self.period2)
        df = add_slice_df(df,max_period)
        # df[df['signal'] != 0].info()
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'

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

        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
        max_period = max(self.period,self.period2)
        df = add_slice_df(df,max_period)
        # df[df['signal'] != 0].info()
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
#TODO
class LTA_TOMYAM(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,k_period=14,d_period=3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.k_period = k_period
        self.d_period = d_period
    def preprocessing(self, df):
        df = add_ema(df,self.period)
        df = add_stochastic(df)
        df = add_atr(df)
        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['%k'] > df['%d']) & (df['%k'].shift(1) <= df['%d'].shift(1)) & (df['%k'] < 20) & (df['atr'] > 0.5), 'signal'] = 1  # Покупка
        df.loc[(df['%k'] < df['%d']) & (df['%k'].shift(1) >= df['%d'].shift(1)) & (df['%k'] > 80) & (df['atr'] > 0.5), 'signal'] = -1 #Продажа
        max_period = max(self.period,self.k_period,self.d_period)
        df = add_slice_df(df,max_period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'