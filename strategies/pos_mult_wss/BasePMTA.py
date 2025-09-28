from ForBots.Indicators.classic_indicators import add_slice_df

class BasePMTA:
    def __init__(self,symbol="BTCUSDT",granularity="1m",pos=0,middle_price=None):
        self.symbol = symbol
        self.granularity = granularity
        self.pos = pos
        self.middle_price = middle_price
        self.need_pos = 0

    def change_data(self,pos,middle_price):
        self.pos = pos
        self.middle_price = middle_price
    def preprocessing(self,df,pos=0,middle_price=0):
        self.change_data(pos,middle_price)
        return df
    
    def get_test_df(self,df):
        df = self.preprocessing(df)
        return df
    
    def get_test_row(self,df):
        try:
            df = self.preprocessing(df)
            return df.iloc[-1]
        except Exception:
            # traceback.print_exc()
            pass
    
    def __call__(self,row, *args, **kwds):
        return None