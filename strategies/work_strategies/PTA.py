from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_donchan_middle,add_donchan_prev
from ForBots.Indicators.price_funcs import get_price_dbb,get_price_reverse_dbb,get_price_bb,get_price_reverse_bb, get_price_bddc,get_price_ddc,get_price_rbddc,get_price_rddc,get_price_rddc_prev,get_price_ddc_prev
from utils.help_trades import reverse_action
from strategies.work_strategies.BaseTA import BaseTABitget

# trand
class PTA2_BDDC(BaseTABitget):
    def preprocessing(self,df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_middle(df)
        df = add_enter_price(df,get_price_bddc)
        df = add_slice_df(df,period=self.period)
        return df
    
    def __call__(self,row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long_p'
        elif row['low'] == row['min_hb']:
            return 'short_p'
        else:
            if row['low'] < row['avarege']:
                return "close_long_p"
            if row['high'] > row['avarege']:
                return "close_short_p"
            
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
            
class PTA2_BDDCmLC(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_big_volume(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self,row, *args, **kwds): 
        if row['high'] == row['max_hb']:
            if row['is_big']:
                return 'close_long_m'
            else:
                return 'long_m'
        elif row['low'] == row['min_hb']:
            if row['is_big']:
                return 'close_short_m'
            else:
                return 'short_m'

            
class PTA2_BDDCde(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_middle(df)
        df = add_enter_price(df,get_price_bddc)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long_p'
        elif row['low'] == row['min_hb']:
            return 'short_p'
        else:
            if row['high'] < row['avarege']:
                return "close_long_p"
            if row['low'] > row['avarege']:
                return "close_short_p"

class PTA2_BDDCr(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_middle(df)
        df = add_enter_price(df,get_price_rbddc)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long_p'
        elif row['low'] == row['min_hb']:
            return 'short_p'
# conter-trend
        
class PTA2_DDCr(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_prev(df)
        df = add_enter_price(df,get_price_rddc_prev)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
    
class PTA2_DDCde(PTA2_BDDCde):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_prev(df)
        df = add_enter_price(df,get_price_ddc_prev)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
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
    

# универсальный

class PTA2_UDC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,slope=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.slope = slope
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_dynamics_ma(df,self.period//2,'avarege')
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self,row, *args, **kwds):
        if row['high'] == row['max_hb']:
            if row['dynamics_ma'] > self.slope:
                return 'long_m'
            else:
                return 'short_r'
        elif row['low'] == row['min_hb']:
            if row['dynamics_ma'] < -self.slope:
                return 'short_m'
            else:
                return 'long_r' 
        else:
            if row['low'] < row['avarege']:
                if row['dynamics_ma'] > self.slope:
                    return 'close_short_r'
                else:
                    return "close_long_m"
            if row['high'] > row['avarege']:
                if row['dynamics_ma'] < -self.slope:
                    return "close_long_r"
                else:
                    return "close_short_m"

# conter-trend      
class PTA8_DOBBY(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price(df,get_price_dbb)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'short_p'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'long_p'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_short_p'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_long_p'
            
class PTA8_ODOBBY(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['over_bbu']:
                return 'short_mt'
        if row['low'] < row['bbd']:
            if row['over_bbd']:
                return 'long_mt'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_short_mt'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_long_mt'


class PTA8_ODOBBY_FREE(PTA8_ODOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['over_bbu']:
                return 'short_mt'
        if row['low'] < row['bbd']:
            if row['over_bbd']:
                return 'long_mt'
        if row['low'] < row['sma']:
                return 'close_short_mt'
        if row['high'] > row['sma']:
                return 'close_long_mt'
        
    
class PTA8_ODOBBY_FREEr(PTA8_ODOBBY_FREE):
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['over_bbu']:
                return 'short_mt'
        if row['low'] < row['bbd']:
            if row['over_bbd']:
                return 'long_mt'
        
            
class PTA8_DOBBY_FREE(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price(df,get_price_dbb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'short_p'
        if row['low'] < row['bbd']:
            return 'long_p'
        if row['low'] < row['sma']:
            return 'close_short_p'
        if row['high'] > row['sma']:
            return 'close_long_p'
        
class PTA8_DOBBY_FREEr(PTA8_DOBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price(df,get_price_reverse_dbb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'short_p'
        if row['low'] < row['bbd']:
            return 'long_p'
# trend
class PTA8_OBBY(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price(df,get_price_bb)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_mt'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_mt'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long_p'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short_p'
            
class PTA8_OBBY_PF(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price(df,get_price_bb)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_mt'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_mt'
        if row['low'] < row['sma']:
            return 'close_long_p'
        if row['high'] > row['sma']:
            return 'close_short_p'
            
class PTA8_LOBBY(PTA8_OBBY):
    def __call__(self, row, *args, **kwds):
        if row['over_bbu']:
            return 'close_long'
        if row['over_bbd']:
            return 'close_short'
        if row['high'] > row['bbu']:
            if row['is_big']:
                return 'long_mt'
        if row['low'] < row['bbd']:
            if row['is_big']:
                return 'short_mt'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long_p'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short_p'
            
class PTA8_FOBBY(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_enter_price(df,get_price_bb)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big']:
                return 'long_mt'
        if row['low'] < row['bbd']:
            if row['is_big']:
                return 'short_mt'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long_p'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short_p'

class PTA8_OBBY_FREE(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price(df,get_price_bb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'long_mt'
        if row['low'] < row['bbd']:
            return 'short_mt'
        if row['low'] < row['sma']:
            return 'close_long_p'
        if row['high'] > row['sma']:
            return 'close_short_p'
        
class PTA8_OBBY_FREEr(PTA8_OBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        # df = add_enter_price(df,get_price_reverse_bb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'long_mt'
        if row['low'] < row['bbd']:
            return 'short_mt'
        
class PTA8_OBBY_VOR(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_over_bb(df)
        # df = add_enter_price(df,get_price_reverse_bb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_mt'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_mt'
        
class PTA8_OOBBY(PTA8_ODOBBY):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
class PTA8_OOBBY_FREE(PTA8_ODOBBY_FREE):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
class PTA8_OOBBY_FREEr(PTA8_ODOBBY_FREEr):
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action