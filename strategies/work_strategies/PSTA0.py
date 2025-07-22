import pandas as pd
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close,add_fractals,add_average_fractals,add_dynamic_zigzag,add_dzz_peaks


class PSTA2_HERO(BaseTABitget):
    """period=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df):
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        pass
        # if self.threshold < row['adx'] > row['sma_adx']:
        #     if row['high'] == row['max_hb']:
        #         return 'long_pw'
        #     if row['low'] == row['min_hb']:
        #         return 'short_pw'
        #     if row['close'] < row['stop_long']:
        #         return 'close_long_pw'
        #     if row['close'] > row['stop_short']:
        #         return 'close_short_pw'
        # return 'close_all_pw'

class PSTA2_GGD(BaseTABitget):
    """period=20, n_candles=5,n_fractals=3"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_candles=5,n_fractals=3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_candles = n_candles
        self.n_fractals = n_fractals
    def preprocessing(self, df):
        df = add_fractals(df,self.n_candles)
        df = add_average_fractals(df,self.n_fractals)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['close'] >= row['ave_up']:
            return 'short_pw'
        if row['close'] <= row['ave_down']:
            return 'long_pw'
        
class PSTA3_ZEUS(BaseTABitget):
    """period=20, n_std=5,method='std'|'mean'"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_std=5,method='std'):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_std = n_std
        self.method = method
    def preprocessing(self, df):
        df = add_dynamic_zigzag(df,n_std=self.n_std,method=self.method,period=self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['zigzag_direction']:
            if row['zigzag_direction'] == -1:
                return 'short_pw'
            if row['zigzag_direction'] == 1:
                return 'long_pw'
            
class PSTA3_HADES(BaseTABitget):
    """period=20, n_std=5,method='std'|'mean'"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_std=5,method='std'):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_std = n_std
        self.method = method
    def preprocessing(self, df):
        df = add_dynamic_zigzag(df,n_std=self.n_std,method=self.method,period=self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['zigzag_direction']:
            if row['zigzag_direction'] == 1:
                return 'short_pw'
            if row['zigzag_direction'] == -1:
                return 'long_pw'

class PSTA3_REVAN(BaseTABitget):
    """period=60, n_std=5"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60, n_std=5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_std = n_std

    def preprocessing(self, df:pd.DataFrame):
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['zigzag_direction'] == -1:
            return 'long_pw'
        if row['zigzag_direction'] == 1:
            return 'short_pw'
        return None
