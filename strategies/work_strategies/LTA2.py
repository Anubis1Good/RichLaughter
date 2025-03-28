import numpy as np
import  matplotlib.pyplot as plt

from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_ema,add_enter_price2close,add_rsi,add_chop,add_rsi_tw,add_cci,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_adx,add_donchan_channel,add_sma

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
            
