from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close


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