import pandas as pd
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close,add_dzz_peaks
from ForBots.Indicators.pva_indicators import add_pattern18_dzz

class VSAT1_(BaseTABitget):
    """period=20, n_std=5,threshold_dzz=0.2,buff=0.1)"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_std=5,threshold_dzz=0.2,buff=0.1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_std = n_std
        self.threshold_dzz = threshold_dzz
        self.buff = buff
    def preprocessing(self, df):
        df = add_dzz_peaks(df,period=self.period,n_std=self.n_std)
        df = add_pattern18_dzz(df,self.threshold_dzz,self.buff)
        # df['signal'] = df.apply(self.__call__,axis=1)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        # long
        if row['pattern18'] == 'joc':
            if row['close'] <= row['bzp2']:
                return 'long_pw'
            if row['close'] < row['zp3']:
                return 'close_long_pw'
        if row['pattern18'] == 'btc':
            if row['close'] >= row['btarget']:
                return 'close_long_pw'
            if row['close'] <= row['bzp4']:
                return 'long_pw'
            if row['close'] <= row['mzp']:
                return 'close_short_pw'
        # short
        if row['pattern18'] == 'bui':
            if row['close'] > row['zp3']:
                return 'close_short_pw'
            if row['close'] >= row['bzp2']:
                return 'short_pw'
        if row['pattern18'] == 'bti':
            if row['close'] <= row['btarget']:
                return 'close_short_pw'
            if row['close'] >= row['bzp4']:
                return 'short_pw'
            if row['close'] >= row['mzp']:
                return 'close_long_pw'
        # range
        if row['pattern18'] == 'top_range':
            if row['close'] <= row['bzp3']:
                return 'long_pw'
            if row['close'] >= row['bzp4']:
                return 'short_pw'
        if row['pattern18'] == 'bottom_range':
            if row['close'] >= row['bzp3']:
                return 'short_pw'
            if row['close'] <= row['bzp4']:
                return 'long_pw'
        if row['pattern18'] == 'narrowing_up':
            if row['close'] >= row['bzp3']:
                return 'close_long_pw'
            if row['close'] <= row['mzp']:
                return 'close_short_pw'
        if row['pattern18'] == 'narrowing_down':
            if row['close'] <= row['bzp3']:
                return 'close_short_pw'
            if row['close'] >= row['mzp']:
                return 'close_long_pw'
        if row['pattern18'] == 'upthrust':
            if row['close'] >= row['bzp3']:
                return 'short_pw'
            if row['close'] <= row['bzp4']:
                return 'long_pw'            
            if row['close'] >= row['mzp']:
                return 'close_long_pw'            
        if row['pattern18'] == 'spring':
            if row['close'] <= row['bzp3']:
                return 'long_pw'
            if row['close'] >= row['bzp4']:
                return 'short_pw'
            if row['close'] <= row['mzp']:
                return 'close_short_pw'         
        if row['pattern18'] == 'sow':
            if row['close'] >= row['bzp2']:
                return 'short_pw'
        if row['pattern18'] == 'sos':
            if row['close'] <= row['bzp2']:
                return 'long_pw'
        if row['pattern18'] == 'double_bottom':
            if row['close'] >= row['bzp3']:
                return 'close_long_pw'
            if row['close'] <= row['bzp4']:
                return 'long_pw'
        if row['pattern18'] == 'double_top':
            if row['close'] <= row['bzp3']:
                return 'close_short_pw'
            if row['close'] >= row['bzp4']:
                return 'short_pw'
        if row['pattern18'] == 'weak_long':
            if row['close'] >= row['bzp4']:
                return 'short_pw'
            if row['close'] >= row['mzp']:
                return 'close_long_pw'
        if row['pattern18'] == 'weak_short':
            if row['close'] <= row['bzp4']:
                return 'long_pw'
            if row['close'] <= row['mzp']:
                return 'close_short_pw'