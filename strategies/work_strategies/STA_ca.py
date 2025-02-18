from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_bollinger,add_big_volume,add_attached_bb,add_over_bb,add_dynamics_ma,add_slice_df

class STA1e:
    def __init__(self,symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=1,period=20,multiplier=2,slope=5):
        self.period = period
        self.multiplier = multiplier
        self.symbol = symbol
        self.granularity = granularity
        self.productType = productType
        self.n_parts = n_parts
        self.bbu_attached = False
        self.bbd_attached = False
        self.slope = slope

    def preprocessing(self,df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_over_bb(df)
        df = add_attached_bb(df)
        df = add_dynamics_ma(df,period=self.period//2)
        df = add_slice_df(df,period=self.period)
        return df
    
    def get_test_df(self,df):
        df = self.preprocessing(df)
        return df
    
    def get_row(self):
        limit = self.period*2
        df = get_df(self.symbol,self.granularity,self.productType,limit)
        df = self.preprocessing(df)
        return df.iloc[-1]
    
    def __call__(self, row, *args, **kwds):
        if row['attached_change']:
            if row['bbu_attached'] != self.bbu_attached:
                return 'close_long'
            if row['bbd_attached'] != self.bbd_attached:
                return 'close_short'
        self.bbu_attached = row['bbu_attached']
        self.bbd_attached = row['bbd_attached']
        if row['dynamics_ma'] > self.slope:
            if row['low'] < row['sma']:
                return 'long'
        if row['dynamics_ma'] < -self.slope:
            if row['high'] > row['sma']:
                return 'short'
        if row['is_big']:
            if row['bbu_attached']:
                return 'close_long'
            if row['bbd_attached']:
                return 'close_short'
        if row['over_bbu']:
            return 'close_long'
        if row['over_bbd']:
            return 'close_short'
