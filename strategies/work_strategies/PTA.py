import numpy as np
import pandas as pd
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi,add_enter_price2close,add_rsi_tw,add_sma,add_ema,add_mfi,add_ultimate_oscillator,add_stochastic,add_fractals
from ForBots.Indicators.pva_indicators import add_mean_on_fractals,add_smooth_channel
from utils.help_trades import reverse_action,chep
from strategies.work_strategies.BaseTA import BaseTABitget

            
class PTA2_BDDC_FIX(BaseTABitget):
    """period=20,can_long=True,can_short=True"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,can_long=True,can_short=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.can_long = can_long
        self.can_short = can_short
    def preprocessing(self,df):
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    
    def __call__(self,row, *args, **kwds):
        if row['high'] >= row['max_hb']:
            if self.can_long:
                return 'long_pw'
        if row['low'] <= row['min_hb']:
            if self.can_short:
                return 'short_pw'
        if row['low'] < row['avarege']:
            return "close_long_pw"
        if row['high'] > row['avarege']:
            return "close_short_pw"
            
class PTA2_BDDCr_UNIVERSAL(BaseTABitget):
    """period=20,can_long=True,can_short=True"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,can_long=True,can_short=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.can_long = can_long
        self.can_short = can_short
    def preprocessing(self,df):
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    
    def __call__(self,row, *args, **kwds):
        if row['high'] >= row['max_hb']:
            if self.can_long:
                return 'long_pw'
            else:
                return "close_short_pw"
        if row['low'] <= row['min_hb']:
            if self.can_short:
                return 'short_pw'
            else:
                return "close_long_pw"
            
class PTA2_BBBUr(BaseTABitget):
    """period=20,can_long=True,can_short=True"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,can_long=True,can_short=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.can_long = can_long
        self.can_short = can_short
    def preprocessing(self,df):
        df = add_bollinger(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self,row, *args, **kwds):
        if row['high'] > row['bbu']:
            if self.can_long:
                return 'long_pw'
            else:
                return "close_short_pw"
        if row['low'] < row['bbd']:
            if self.can_short:
                return 'short_pw'
            else:
                return "close_long_pw"

        
class PTA2_BBBU(BaseTABitget):
    """period=20,can_long=True,can_short=True"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,can_long=True,can_short=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.can_long = can_long
        self.can_short = can_short
    def preprocessing(self,df):
        df = add_bollinger(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    
    def __call__(self,row, *args, **kwds):
        if row['high'] > row['bbu']:
            if self.can_long:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if self.can_short:
                return 'short_pw'
        if row['low'] < row['sma']:
            return "close_long_pw"
        if row['high'] > row['sma']:
            return "close_short_pw"
            
class PTA2_BVGFIX(BaseTABitget):
    """period=20,can_long=True,can_short=True"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,can_long=True,can_short=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.can_long = can_long
        self.can_short = can_short
    def preprocessing(self,df):
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    
    def __call__(self,row, *args, **kwds):
        if row['high'] > row['max_vg']:
            if self.can_long:
                return 'long_pw'
            else:
                return "close_short_pw"
        if row['low'] < row['min_vg']:
            if self.can_short:
                return 'short_pw'
            else:
                return "close_long_pw"


#D      
class PTA2_DDCrWork(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb'] and nearest_long:
            return 'long_pw'
        if row['high'] >= row['max_hb'] and not nearest_long:
            return 'short_pw'
        
class PTA2_SDDCr(BaseTABitget):
    """period=20,period2=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period2=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_smooth_channel(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                return 'long_pw'
        if row['high'] >= row['max_hb']:
            return 'short_pw'
#D         
class PTA4_WDDCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class PTA4_WDDCr2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi_tw'] < self.threshold:
                    return 'long_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi_tw'] > 100-self.threshold:
                return 'short_pw'
#D         
class PTA4_WDDCr2E(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi_tw'] < self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi_tw'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
#D         
class PTA4_WDDCrE(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
#D             
class PTA4_WDDCde(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
        if row['high'] < row['avarege']:
            return "close_long_pw"
        if row['low'] > row['avarege']:
            return "close_short_pw"

class PTA4_UNIVERSAL(BaseTABitget):
    '''
    period,period_rsi,threshold_long,threshold_short
    kind_channel in ["DC","VG","BB","VC","WC"]
    kind_rsi in ["rsi","rsi_tw","mfi","s","uo"]
    can_long,can_short
    '''
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period_rsi=20,threshold_long=30,threshold_short=30,kind_channel='DC',kind_rsi='rsi',can_long=True,can_short=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold_long = threshold_long
        self.threshold_short = threshold_short
        self.period_rsi = period_rsi
        self.kind_channel = kind_channel
        self.kind_rsi = kind_rsi
        self.rsi = 'rsi'
        self.up = 'up'
        self.down = 'down'
        self.can_long = can_long
        self.can_short = can_short

    def add_channel(self,df:pd.DataFrame):
        if self.kind_channel == 'VG':
            df = add_donchan_channel(df,self.period)
            df = add_vangerchik(df)
            df = df.rename({'max_vg':self.up,'min_vg':self.down},axis=1)
        elif self.kind_channel == 'BB':
            df = add_bollinger(df,self.period)
            df = df.rename({'bbu':self.up,'bbd':self.down},axis=1)
        elif self.kind_channel == 'VC':
            df = add_vodka_channel(df,self.period)
            df = df.rename({'top_mean':self.up,'bottom_mean':self.down},axis=1)
        elif self.kind_channel == 'WC':
            df = add_vodka_channel(df,self.period)
            df = add_buffer_add(df,'top_mean','bottom_mean',2)
            df = df.rename({'top_buff':self.up,'bottom_buff':self.down},axis=1)
        else:
            df = add_donchan_channel(df,self.period)
            df = df.rename({'max_hb':self.up,'min_hb':self.down},axis=1)
        return df
    
    def add_rsi(self,df:pd.DataFrame):
        if self.kind_rsi == 'rsi_tw':
            df = add_rsi_tw(df,self.period_rsi)
            df = df.rename({'rsi_tw':'rsi'},axis=1)
        elif self.kind_rsi == 'mfi':
            df = add_mfi(df,self.period_rsi)
            df = df.rename({'mfi':'rsi'},axis=1)
        elif self.kind_rsi == 's':
            df = add_stochastic(df,self.period_rsi,self.period_rsi//3)
            df = df.rename({'%d':'rsi'},axis=1)
        elif self.kind_rsi == 'uo':
            df = add_ultimate_oscillator(df,self.period_rsi//3,self.period_rsi//2,self.period_rsi)
            df = df.rename({'ultimate_oscillator':'rsi'},axis=1)
        else:
            df = add_rsi(df,self.period_rsi)
        return df
    
    def preprocessing(self, df):
        df = self.add_channel(df)
        df = self.add_rsi(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row[self.down]:
            if nearest_long:
                if row['rsi'] < self.threshold_long:
                    if self.can_long:
                        return 'long_pw'
                    else:
                        return 'close_short_pw'
        if row['high'] >= row[self.up]:
            if row['rsi'] > 100-self.threshold_short:
                if self.can_short:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
                
class PTA4_UNIVERSAL2(BaseTABitget):
    '''
    period,period_rsi,threshold_long,threshold_short
    kind_channel in ["DC","VG","BB","VC","WC"]
    kind_rsi in ["rsi","rsi_tw","mfi","s","uo"]
    can_long,can_short
    '''
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period_rsi=20,threshold_long=30,threshold_short=30,kind_channel='DC',kind_rsi='rsi',can_long=True,can_short=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold_long = threshold_long
        self.threshold_short = threshold_short
        self.period_rsi = period_rsi
        self.kind_channel = kind_channel
        self.kind_rsi = kind_rsi
        self.rsi = 'rsi'
        self.up = 'up'
        self.down = 'down'
        self.can_long = can_long
        self.can_short = can_short

    def add_channel(self,df:pd.DataFrame):
        if self.kind_channel == 'VG':
            df = add_donchan_channel(df,self.period)
            df = add_vangerchik(df)
            df = df.rename({'max_vg':self.up,'min_vg':self.down},axis=1)
        elif self.kind_channel == 'BB':
            df = add_bollinger(df,self.period)
            df = df.rename({'bbu':self.up,'bbd':self.down},axis=1)
        elif self.kind_channel == 'VC':
            df = add_vodka_channel(df,self.period)
            df = df.rename({'top_mean':self.up,'bottom_mean':self.down},axis=1)
        elif self.kind_channel == 'WC':
            df = add_vodka_channel(df,self.period)
            df = add_buffer_add(df,'top_mean','bottom_mean',2)
            df = df.rename({'top_buff':self.up,'bottom_buff':self.down},axis=1)
        else:
            df = add_donchan_channel(df,self.period)
            df = df.rename({'max_hb':self.up,'min_hb':self.down},axis=1)
        return df
    
    def add_rsi(self,df:pd.DataFrame):
        if self.kind_rsi == 'rsi_tw':
            df = add_rsi_tw(df,self.period_rsi)
            df = df.rename({'rsi_tw':'rsi'},axis=1)
        elif self.kind_rsi == 'mfi':
            df = add_mfi(df,self.period_rsi)
            df = df.rename({'mfi':'rsi'},axis=1)
        elif self.kind_rsi == 's':
            df = add_stochastic(df,self.period_rsi,self.period_rsi//3)
            df = df.rename({'%d':'rsi'},axis=1)
        elif self.kind_rsi == 'uo':
            df = add_ultimate_oscillator(df,self.period_rsi//3,self.period_rsi//2,self.period_rsi)
            df = df.rename({'ultimate_oscillator':'rsi'},axis=1)
        else:
            df = add_rsi(df,self.period_rsi)
        return df
    
    def preprocessing(self, df):
        df = self.add_channel(df)
        df = self.add_rsi(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row[self.down]:
            if nearest_long:
                if row['rsi'] < self.threshold_long:
                    if self.can_long:
                        return 'long_pw'
                    else:
                        return 'close_short_pw'
        if row['high'] >= row[self.up]:
            if row['rsi'] > 100-self.threshold_short:
                if self.can_short:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
        if not self.can_long:
            return 'close_long_pw'
        if not self.can_short:
            return 'close_short_pw'

class PTA4_U3(BaseTABitget):
    '''
    period=20,period_rsi=20,period_fractal=10,period_mean=5
    kind_channel in ["DC","VG","BB","VC","WC"]
    kind_rsi in ["rsi","rsi_tw","mfi","s","uo"]
    
    '''
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period_rsi=20,period_fractal=10,period_mean=5,kind_channel='DC',kind_rsi='rsi'):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period_fractal = period_fractal
        self.period_mean = period_mean
        self.period_rsi = period_rsi
        self.kind_channel = kind_channel
        self.kind_rsi = kind_rsi
        self.rsi = 'rsi'
        self.up = 'up'
        self.down = 'down'

    def add_channel(self,df:pd.DataFrame):
        if self.kind_channel == 'VG':
            df = add_donchan_channel(df,self.period)
            df = add_vangerchik(df)
            df = df.rename({'max_vg':self.up,'min_vg':self.down},axis=1)
        elif self.kind_channel == 'BB':
            df = add_bollinger(df,self.period)
            df = df.rename({'bbu':self.up,'bbd':self.down},axis=1)
        elif self.kind_channel == 'VC':
            df = add_vodka_channel(df,self.period)
            df = df.rename({'top_mean':self.up,'bottom_mean':self.down},axis=1)
        elif self.kind_channel == 'WC':
            df = add_vodka_channel(df,self.period)
            df = add_buffer_add(df,'top_mean','bottom_mean',2)
            df = df.rename({'top_buff':self.up,'bottom_buff':self.down},axis=1)
        else:
            df = add_donchan_channel(df,self.period)
            df = df.rename({'max_hb':self.up,'min_hb':self.down},axis=1)
        return df
    
    def add_rsi(self,df:pd.DataFrame):
        if self.kind_rsi == 'rsi_tw':
            df = add_rsi_tw(df,self.period_rsi)
            df = df.rename({'rsi_tw':'rsi'},axis=1)
        elif self.kind_rsi == 'mfi':
            df = add_mfi(df,self.period_rsi)
            df = df.rename({'mfi':'rsi'},axis=1)
        elif self.kind_rsi == 's':
            df = add_stochastic(df,self.period_rsi,self.period_rsi//3)
            df = df.rename({'%d':'rsi'},axis=1)
        elif self.kind_rsi == 'uo':
            df = add_ultimate_oscillator(df,self.period_rsi//3,self.period_rsi//2,self.period_rsi)
            df = df.rename({'ultimate_oscillator':'rsi'},axis=1)
        else:
            df = add_rsi(df,self.period_rsi)
        return df
    
    def preprocessing(self, df):
        df = self.add_channel(df)
        df = self.add_rsi(df)
        df = add_fractals(df,self.period_fractal)
        df = add_mean_on_fractals(df,self.period_mean,'rsi')
        df['oversold'] = df['rsi'] < df['bottom_mean']
        df['overbought'] = df['rsi'] > df['top_mean']
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['low'] <= row[self.down]:
            if row['oversold']:
                return 'long_pw'
        if row['high'] >= row[self.up]:
            if row['overbought']:
                return 'short_pw'


class PTA4_WDDC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
        if row['close'] < row['avarege']:
            return "close_long_pw"
        if row['close'] > row['avarege']:
            return "close_short_pw"

# D     
class PTA2_DDCrVG(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['min_vg']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['max_vg']:
            return 'short_pw'

#D        
class PTA4_WDDCrVG(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['min_vg']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['max_vg']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
#D  
class PTA2_DVCr(BaseTABitget):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_mean']:
            return 'short_pw'
#D  
class PTA4_WDVCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['top_mean']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

#D        
class PTA2_VOLCHARA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,divider=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.divider = divider
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_buff']:
            return 'short_pw'
        if row['low'] < row['avarege_mean']:
            return 'close_short_pw'
        if row['high'] > row['avarege_mean']:
            return 'close_long_pw'
#D  
class PTA2_LISICA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,divider=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.divider = divider
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_buff']:
            return 'short_pw'
#D  
class PTA4_WLISICA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,divider=1,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.divider = divider
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['top_buff']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

# D 
class PTA8_DOBBY(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'short_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'long_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_short_pw'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_long_pw'
            

#D      
class PTA8_DOBBY_FREE(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'short_pw'
        if row['low'] < row['bbd']:
            return 'long_pw'
        if row['low'] < row['sma']:
            return 'close_short_pw'
        if row['high'] > row['sma']:
            return 'close_long_pw'
#D  
class PTA8_DOBBY_FREEr(PTA8_DOBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'short_pw'
        if row['low'] < row['bbd']:
            return 'long_pw'
#D  
class PTA8_WDOBBY_FREEr(BaseTABitget):
    """period=20,multiplier=2,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bbd']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['bbu']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

# trend
# BD
class PTA8_OBBY(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long_pw'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short_pw'
#BD        
class PTA8_OBBY_PF(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_pw'
        if row['low'] < row['sma']:
            return 'close_long_pw'
        if row['high'] > row['sma']:
            return 'close_short_pw'
#BD 
class PTA8_LOBBY(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['over_bbu']:
            return 'close_long'
        if row['over_bbd']:
            return 'close_short'
        if row['high'] > row['bbu']:
            if row['is_big']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big']:
                return 'short_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short'
#BD 
class PTA8_LOBSTER(PTA8_LOBBY):
    def __call__(self, row, *args, **kwds):
        if row['over_bbu']:
            return 'close_long_pw'
        if row['over_bbd']:
            return 'close_short_pw'
        if not (row['high'] > row['bbu'] and row['low'] < row['bbd']):
            if row['high'] > row['bbu']:
                if row['is_big']:
                    return 'long_pw'
            if row['low'] < row['bbd']:
                if row['is_big']:
                    return 'short_pw'
            if row['low'] < row['sma']:
                if row['is_big']:
                    return 'close_long_pw'
            if row['high'] > row['sma']:
                if row['is_big']:
                    return 'close_short_pw' 
#BD 
class PTA8_FOBBY(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big']:
                return 'short_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long_pw'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short_pw'
#BD 
class PTA8_OBBY_FREE(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'long_pw'
        if row['low'] < row['bbd']:
            return 'short_pw'
        if row['low'] < row['sma']:
            return 'close_long_pw'
        if row['high'] > row['sma']:
            return 'close_short_pw'
#BD           
class PTA8_OBBY_FREEr(PTA8_OBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'long_pw'
        if row['low'] < row['bbd']:
            return 'short_pw'
#BD               
class PTA8_OBBY_VOR(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_over_bb(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_pw'
        

# TODO
# D
class PTA9_CRAB(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=5,multiplier=2,period_slow=20,slope=0.5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
        self.period_slow = period_slow
        self.slope = slope
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_donchan_channel(df,self.period_slow)
        df = add_vangerchik(df)
        df = add_simple_dynamics_ma(df,self.period_slow,'avarege')
        df['slope'] = self.slope
        df = add_enter_price2close(df)
        max_period = max(self.period,self.period_slow)
        df = add_slice_df(df,period=max_period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['sdm'] >= self.slope and row['sma'] > row['avarege']:
            if row['low'] <= row['sma'] and chep(row,row['long_price']):
                return 'long_pw'

        if row['sdm'] <= -self.slope and row['sma'] < row['avarege']:
            if row['high'] >= row['sma'] and chep(row,row['short_price']):
                return 'short_pw'

        if -self.slope < row['sdm'] < self.slope:
            if row['high'] > row['max_vg'] and chep(row,row['short_price']):
                return 'short_pw'
            if row['low'] < row['min_vg'] and chep(row,row['long_price']):
                return 'long_pw'
        if row['sdm'] >= self.slope and row['sma'] < row['avarege']:
            return 'close_long_pw'
        if row['sdm'] <= -self.slope and row['sma'] > row['avarege']:
            return 'close_short_pw'
# BD
class PTA9_RAB(PTA9_CRAB):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period_slow,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period_slow)
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_simple_dynamics_ma(df,self.period,'avarege')
        df['slope'] = self.slope
        df = add_enter_price2close(df)
        max_period = max(self.period,self.period_slow)
        df = add_slice_df(df,period=max_period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['sdm'] >= self.slope and row['sma'] > row['avarege']:
            if row['low'] <= row['sma'] and chep(row,row['short_price']):
                return 'short_pw'

        if row['sdm'] <= -self.slope and row['sma'] < row['avarege']:
            if row['high'] >= row['sma'] and chep(row,row['long_price']):
                return 'long_pw'

        if -self.slope < row['sdm'] < self.slope:
            if row['high'] > row['max_vg'] and chep(row,row['short_price']):
                return 'long_pw'
            if row['low'] < row['min_vg'] and chep(row,row['long_price']):
                return 'short_pw'
        if row['sdm'] >= self.slope and row['sma'] < row['avarege']:
            return 'close_long_pw'
        if row['sdm'] <= -self.slope and row['sma'] > row['avarege']:
            return 'close_short_pw'
