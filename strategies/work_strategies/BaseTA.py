from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_slice_df
class BaseTABitget:
    def __init__(self,symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=1,period=20):
        self.symbol = symbol
        self.granularity = granularity
        self.productType = productType
        self.n_parts = n_parts
        self.period = period

    def preprocessing(self,df):
        df = add_slice_df(df,period=self.period)
        return df
    
    def get_test_df(self,df):
        df = self.preprocessing(df)
        return df
    
    def get_test_row(self):
        pass
    
    def get_row(self):
        limit = self.period*3
        df = get_df(self.symbol,self.granularity,self.productType,limit)
        df = self.preprocessing(df)
        return df.iloc[-1]
    
    # def get_middle_price(self,row):
    #     return row['middle']
    
    def __call__(self,row, *args, **kwds):
        return None