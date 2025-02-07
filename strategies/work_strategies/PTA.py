from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel

class PTA2_BDDC:
    def __init__(self,period,symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=1):
        self.period = period
        self.symbol = symbol
        self.granularity = granularity
        self.productType = productType
        self.n_parts = n_parts
    
    def get_row(self):
        limit = self.period*2
        df = get_df(self.symbol,self.granularity,self.productType,limit)
        df = add_donchan_channel(df,self.period)
        return df.iloc[-1]
    
    def __call__(self, *args, **kwds):
        row = self.get_row()
        if row['high'] == row['max_hb']:
            return 'long'
        elif row['low'] == row['min_hb']:
            return 'short'
        else:
            if row['low'] < row['avarege']:
                return "close_long"
            if row['high'] > row['avarege']:
                return "close_short"