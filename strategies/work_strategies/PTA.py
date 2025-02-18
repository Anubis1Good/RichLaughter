from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df
from utils.help_trades import reverse_action
from strategies.work_strategies.BaseTA import BaseTABitget

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
            
class PTA2_BDDCde(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long'
        elif row['low'] == row['min_hb']:
            return 'short'
        else:
            if row['high'] < row['avarege']:
                return "close_long"
            if row['low'] > row['avarege']:
                return "close_short"
            
class PTA2_BDDCr(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long'
        elif row['low'] == row['min_hb']:
            return 'short'
        
class PTA2_DDCr(PTA2_BDDCr):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        return reverse_action(action)
    
class PTA2_DDCde(PTA2_BDDCde):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        return reverse_action(action)

class PTA2_DDCdeDaddyNotShort(PTA2_BDDCde):
    '''Папа не шорти'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'short' in action:
                action = action.replace('short','long')
        return action
    
class PTA2_DDCdeDaddyNotLong(PTA2_BDDCde):
    '''Папа не лонгуй'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'long' in action:
                action = action.replace('long','short')
        return action
    
class PTA2_DDCLong(PTA2_BDDCde):
    '''Игнор Шорта'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'short' in action:
                action = action.replace('short','long')
            elif 'long' in action:
                return None
        return action
class PTA2_DDCShort(PTA2_BDDCde):
    '''Игнор лонга'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'long' in action:
                action = action.replace('long','short')
            elif 'short' in action:
                return None
        return action
    

