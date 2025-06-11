from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close,add_fractals,add_average_fractals


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
