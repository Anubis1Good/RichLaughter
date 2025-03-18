import pandas as pd
import numpy as np
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
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
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=14,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_CDV(df)
        df = add_rsi(df,self.period,'cdv')
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):
        if row['rsi'] < self.threshold:  
            return 'long_pw'
        if row['rsi'] > 100-self.threshold:  
            return 'short_pw'
