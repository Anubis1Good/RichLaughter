from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df
from utils.help_trades import reverse_action
from strategies.work_strategies.BaseTA import BaseTABitget

# trand
class PTA2_BDDC(BaseTABitget):
    def preprocessing(self,df):
        df = add_donchan_channel(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    
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
            
class PTA2_BDDCm(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self,row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long_m'
        elif row['low'] == row['min_hb']:
            return 'short_m'
        else:
            if row['low'] < row['avarege']:
                return "close_long_m"
            if row['high'] > row['avarege']:
                return "close_short_m"
            
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

# conter-trend
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
        action = reverse_action(action)
        if action:
            action += '_r'
        return action
    
class PTA2_DDCde(PTA2_BDDCde):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        if action:
            action += '_r'
        return action

class PTA2_DDCdeDaddyNotShort(PTA2_BDDCde):
    '''Папа не шорти'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'short' in action:
                action = action.replace('short','long')+'_r'
        return action
    
class PTA2_DDCdeDaddyNotLong(PTA2_BDDCde):
    '''Папа не лонгуй'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'long' in action:
                action = action.replace('long','short')+'_r'
        return action
    
class PTA2_DDCLong(PTA2_BDDCde):
    '''Игнор Шорта'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'short' in action:
                action = action.replace('short','long')+'_r'
            elif 'long' in action:
                return None
        return action
class PTA2_DDCShort(PTA2_BDDCde):
    '''Игнор лонга'''
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        if action:
            if 'long' in action:
                action = action.replace('long','short')+'_r'
            elif 'short' in action:
                return None
        return action
    

