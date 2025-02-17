from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df

class PTA2_BDDC:
    def __init__(self,symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=1,period=20):
        self.period = period
        self.symbol = symbol
        self.granularity = granularity
        self.productType = productType
        self.n_parts = n_parts

    def preprocessing(self,df):
        df = add_donchan_channel(df,self.period)
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
    
    def __call__(self,row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long'
        elif row['low'] == row['min_hb']:
            return 'short'
        else:
            if row['low'] < row['avarege']:
                return "close_long"
            if row['high'] > row['avarege']:
                return "close_short"