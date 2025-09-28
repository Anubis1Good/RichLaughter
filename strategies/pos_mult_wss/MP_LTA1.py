from strategies.pos_mult_wss.BasePMTA import BasePMTA
from ForBots.Indicators.classic_indicators import add_slice_df,add_rsi

class MP_LTA_SHCHI(BasePMTA):
    """period=14"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", pos=0, middle_price=None,period=14):
        super().__init__(symbol, granularity, pos, middle_price)
        self.period = period
    def preprocessing(self, df, pos=0, middle_price=0):
        super().preprocessing(df, pos, middle_price)
        df = add_rsi(df,self.period)
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        need_pos = 0
        if row['rsi'] < 35:  
            need_pos += 1
        if row['rsi'] < 25:  
            need_pos += 1
        if row['rsi'] < 15:  
            need_pos += 1
        if row['rsi'] < 5:  
            need_pos += 1
        if row['rsi'] > 65:  
            need_pos -= 1
        if row['rsi'] > 75:  
            need_pos -= 1
        if row['rsi'] > 85:  
            need_pos -= 1
        if row['rsi'] > 95:  
            need_pos -= 1
        # добавить выход
        self.need_pos = need_pos
        return self.need_pos
