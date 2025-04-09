import numpy as np
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_ema,add_enter_price2close,add_rsi
from ForBots.Indicators.rare_indicators import add_dynamic_trend_lines_slope_reversed,add_segmented_regression_from_end
from ForBots.Indicators.ml_indicators import add_find_similar_pattern_lite

class STAML2_CHAOS(BaseTABitget):
    """ period=60,min_points=2,divider=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=2,divider=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.divider = divider
    def preprocessing(self, df):
        df = add_dynamic_trend_lines_slope_reversed(df,self.min_points,self.divider)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['trend_up_combined'] < row['trend_down_combined']:
            if row['trend_down_combined'] < row['close']:
                return 'short_pw'
            if row['trend_up_combined'] > row['close']:
                return 'long_pw'
            
class STAML2_FLUX(BaseTABitget):
    """period=60,threshold=0.1,min_points=2,divider=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,threshold=0.1,min_points=2,divider=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.divider = divider
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_dynamic_trend_lines_slope_reversed(df,self.min_points,self.divider)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['trend_up_combined'] < row['trend_down_combined']:
            if row['trend_down_combined'] < row['close']:
                if row['trend_mean_slope'] < self.threshold:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
            if row['trend_up_combined'] > row['close']:
                if row['trend_mean_slope'] > -self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
                
class STAML2_LEGACY(BaseTABitget):
    """period=60,threshold=0.1,min_points=5,multiplier=1"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,threshold=0.1,min_points=5,multiplier=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.threshold = threshold
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_segmented_regression_from_end(df,self.period,self.multiplier,self.min_points)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['upper_channel'] < row['close']:
            if row['regression_slope'] < self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
        if row['lower_channel'] > row['close']:
            if row['regression_slope'] > -self.threshold:
                return 'long_pw'
            else:
                return 'close_short_pw'
                
class STAML2_TRADITION(BaseTABitget):
    """period=60,min_points=5,multiplier=1"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=5,multiplier=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_segmented_regression_from_end(df,self.period,self.multiplier,self.min_points)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['upper_channel'] < row['close']:
            return 'short_pw'
        if row['lower_channel'] > row['close']:
            return 'long_pw'
        
class STAML2_NEWAVE(BaseTABitget):
    """period=60,min_points=5,multiplier=1,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=5,multiplier=1,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.multiplier = multiplier
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_segmented_regression_from_end(df,self.period,self.multiplier,self.min_points)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['upper_channel'] < row['close']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
        if row['lower_channel'] > row['close']:
            if row['rsi'] < self.threshold:
                return 'long_pw'

class STAML2_BALANCE(BaseTABitget):
    """ period=60,min_points=2,divider=30,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=2,divider=30,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.divider = divider
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_dynamic_trend_lines_slope_reversed(df,self.min_points,self.divider)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['trend_up_combined'] < row['trend_down_combined']:
            if row['trend_down_combined'] < row['close']:
                if row['rsi'] > 100-self.threshold:
                    return 'short_pw'
            if row['trend_up_combined'] > row['close']:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
            

class STAML2_SID(BaseTABitget):
    """period=200,window=20,forecast_length=30,threshold=30
    \n
    """
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=200,window=10,forecast_length=5,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.window = window
        self.forecast_length = forecast_length
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_rsi(df,self.window)
        df = add_find_similar_pattern_lite(df,self.window,self.period,forecast_length=self.forecast_length)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, period=self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        delta_fc = (row['forecast_high'] - row['forecast_low'])/10
        if row['close'] > row['forecast_high'] - delta_fc :
            if row['per_fs'] > 0.1 and row['rsi'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
        if row['close'] < row['forecast_low'] + delta_fc :
            if row['per_fs'] > 0.1 and row['rsi'] < self.threshold:
                return 'long_pw'
            else:
                return 'close_short_pw'