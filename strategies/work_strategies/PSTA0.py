import pandas as pd
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close,add_fractals,add_average_fractals,add_dynamic_zigzag,add_dzz_peaks,add_rsi
from ForBots.Indicators.pva_indicators import add_plus_delta_fc ,add_exp_pdfc,add_analys_dzz,add_mean_on_fractals,add_ext_on_fractals

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

class PSTA2_GOOSE(BaseTABitget):
    """period=20, n_candles=5,n_fractals=3"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_candles=5,n_fractals=3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_candles = n_candles
        self.n_fractals = n_fractals
    def preprocessing(self, df):
        df = add_fractals(df,self.n_candles)
        df = add_exp_pdfc(df,self.n_fractals)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['close'] >= row['pdf_up']:
            return 'short_pw'
        if row['close'] <= row['pdf_down']:
            return 'long_pw'
        
class PSTA2_DUCK(BaseTABitget):
    """period=20, n_candles=5,n_fractals=3"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_candles=5,n_fractals=3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_candles = n_candles
        self.n_fractals = n_fractals
    def preprocessing(self, df):
        df = add_fractals(df,self.n_candles)
        df = add_plus_delta_fc(df,self.n_fractals)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['close'] >= row['pdf_up']:
            return 'short_pw'
        if row['close'] <= row['pdf_down']:
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

class PSTA4_FALCON(BaseTABitget):
    """period=20, n_candles=5,n_fractals=3,allowance=0.1"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_candles=5,n_fractals=3,allowance=0.1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.allowance = allowance
    def preprocessing(self, df):
        df = add_fractals(df,self.n_candles)
        df = add_plus_delta_fc(df,self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['allowance']:
            if row['close'] >= row['pdf_up']:
                return 'short_pw'
            if row['close'] <= row['pdf_down']:
                return 'long_pw'

class PSTA4_PELICAN(BaseTABitget):
    """period=20, n_candles=5,n_fractals=3,allowance=0.1"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20, n_candles=5,n_fractals=3,allowance=0.1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.allowance = allowance
    def preprocessing(self, df):
        df = add_fractals(df,self.n_candles)
        df = add_exp_pdfc(df,self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['allowance']:
            if row['close'] >= row['pdf_up']:
                return 'short_pw'
            if row['close'] <= row['pdf_down']:
                return 'long_pw'
            
class PSTA5_HAWK(BaseTABitget):
    """period=100,n_candles=5,n_fractals=3,period_rsi=20,type_treshold=0,period_mean=5,n_std=1.5,period_sma=3,threshold_trend=0.5,allowance=0.1,use_stop=0"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,n_candles=5,n_fractals=3,period_rsi=20,type_treshold=0,period_mean=5,n_std=1.5,period_sma=3,threshold_trend=0.5,allowance=0.1,use_stop=0):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.type_treshold = type_treshold
        self.period_mean = period_mean
        self.period_sma = period_sma
        self.n_std = n_std
        self.threshold_trend = threshold_trend
        self.period_rsi = period_rsi
        self.allowance = allowance
        self.use_stop = use_stop
    def add_threshold(self,df):
        if self.type_treshold == 0:
            df = add_mean_on_fractals(df,self.period_mean,'rsi')
            df['oversold'] = df['rsi'] < df['bottom_mean']
            df['overbought'] = df['rsi'] > df['top_mean']
        else:
            df = add_ext_on_fractals(df,self.period_mean,'rsi')
            df['oversold'] = df['rsi'] < df['bottom_ext']
            df['overbought'] = df['rsi'] > df['top_ext']
        return df
    def preprocessing(self, df):
        df = add_fractals(df,self.n_candles)
        df = add_exp_pdfc(df,self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = add_rsi(df,self.period_rsi)
        df = self.add_threshold(df)
        df = add_dzz_peaks(df,n_std=self.n_std)
        df = add_analys_dzz(df,self.period_sma)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['allowance']:
            if row['low'] <= row['pdf_down'] and row['oversold']:
                if row['trend_sma'] >= -self.threshold_trend:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
            if row['high'] >= row['pdf_up'] and row['overbought']:
                if row['trend_sma'] <= self.threshold_trend:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
        if self.use_stop:
            if row['trend_sma'] < -0.8:
                return 'close_long_pw'
            if row['trend_sma'] > 0.8:
                return 'close_short_pw'