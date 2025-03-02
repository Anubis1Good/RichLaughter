from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_donchan_middle,add_donchan_prev,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi
from ForBots.Indicators.price_funcs import get_price_dbb,get_price_reverse_dbb,get_price_bb,get_price_reverse_bb, get_price_bddc,get_price_ddc,get_price_rbddc,get_price_rddc,get_price_rddc_prev,get_price_ddc_prev,get_price_rddc_prev_ba,get_price_bb_buff,get_price_crab,get_price_rab,get_price_rddc_prev_ba_test,get_universal_r,get_universal
from utils.help_trades import reverse_action,chep
from strategies.work_strategies.BaseTA import BaseTABitget

# trend
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
        df = add_enter_price(df,lambda row: get_universal_r(row,'middle','middle'))
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self,row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long_pw'
        elif row['low'] == row['min_hb']:
            return 'short_pw'
        else:
            if row['low'] < row['avarege']:
                return "close_long_pw"
            if row['high'] > row['avarege']:
                return "close_short_pw"
            
# class PTA2_BDDCmLC(BaseTABitget):
#     def preprocessing(self, df):
#         df = add_donchan_channel(df,self.period)
#         df = add_big_volume(df)
#         df = add_slice_df(df,period=self.period)
#         return df
#     def __call__(self,row, *args, **kwds): 
#         if row['high'] == row['max_hb']:
#             if row['is_big']:
#                 return 'close_long_m'
#             else:
#                 return 'long_m'
#         elif row['low'] == row['min_hb']:
#             if row['is_big']:
#                 return 'close_short_m'
#             else:
#                 return 'short_m'

            
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
            return 'long_pw'
        elif row['low'] == row['min_hb']:
            return 'short_pw'
# conter-trend
        
class PTA2_DDCr(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_prev(df)
        df = add_buffer_sub(df,'prev_max','prev_min')
        df = add_enter_price(df,get_price_rddc_prev_ba_test)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
    
class PTA2_DDCrWork(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_prev(df)
        df = add_buffer_sub(df)
        df = add_enter_price(df,get_price_rddc_prev_ba)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb'] or row['low'] < row['long_price']:
            if nearest_long:
                return 'long_pw'
        if row['high'] == row['max_hb'] or row['high'] > row['short_price']:
            return 'short_pw'
        
class PTA4_WDDCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_prev(df)
        df = add_buffer_sub(df)
        df = add_rsi(df,self.period)
        df = add_enter_price(df,get_price_rddc_prev_ba)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb'] or row['low'] < row['long_price']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb'] or row['high'] > row['short_price']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class PTA4_WDDCde(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_prev(df)
        df = add_buffer_sub(df)
        df = add_rsi(df,self.period)
        df = add_enter_price(df,get_price_ddc_prev)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb'] or row['low'] < row['long_price']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb'] or row['high'] > row['short_price']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
        if row['high'] < row['avarege']:
            return "close_long_pw"
        if row['low'] > row['avarege']:
            return "close_short_pw"
        
class PTA2_DDCrVG(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_donchan_prev(df,'max_vg','min_vg')
        df = add_buffer_sub(df,'prev_max','prev_min')
        df = add_enter_price(df,get_price_rddc_prev_ba_test)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb'] or row['low'] < row['long_price']:
            if nearest_long:
                return 'long_pw'
        if row['high'] == row['max_hb'] or row['high'] > row['short_price']:
            return 'short_pw'
        
class PTA2_DVCr(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price(df,lambda row: get_universal_r(row,'bottom_mean','top_mean'))
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_mean']:
            return 'short_pw'
        
class PTA2_BDVCr(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price(df,lambda row: get_universal_r(row,'top_mean','bottom_mean'))
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                return 'short_pw'
        if row['high'] > row['top_mean']:
            return 'long_pw'
        
class PTA2_ALKASH(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                return 'short_pw'
        if row['high'] > row['top_mean']:
            return 'long_pw'
        
class PTA2_VOLCHARA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,divider=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.divider = divider
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price(df,lambda row: get_universal(row,'bottom_buff','top_buff','avarege_mean','avarege_mean'))
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_buff']:
            return 'short_pw'
        if row['low'] < row['avarege_mean']:
            return 'close_short_pw'
        if row['high'] > row['avarege_mean']:
            return 'close_long_pw'
        
class PTA2_LISICA(PTA2_VOLCHARA):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price(df,lambda row: get_universal_r(row,'bottom_buff','top_buff'))
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_buff']:
            return 'short_pw'

# revers volchara
class PTA2_ZAYAC(PTA2_VOLCHARA):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price(df,lambda row: get_universal(row,'top_buff','bottom_buff','avarege_mean','avarege_mean'))
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
# revers lisica
class PTA2_KOLOBOK(PTA2_LISICA):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price(df,lambda row: get_universal_r(row,'top_buff','bottom_buff'))
        df = add_slice_df(df,self.period)
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

# class PTA2_DDCdeDaddyNotShort(PTA2_BDDCde):
#     '''Папа не шорти'''
#     def __call__(self, row, *args, **kwds):
#         action = super().__call__(row, *args, **kwds)
#         if action:
#             if 'short' in action:
#                 action = action.replace('short','long')+'_r'
#         return action
    
# class PTA2_DDCdeDaddyNotLong(PTA2_BDDCde):
#     '''Папа не лонгуй'''
#     def __call__(self, row, *args, **kwds):
#         action = super().__call__(row, *args, **kwds)
#         if action:
#             if 'long' in action:
#                 action = action.replace('long','short')+'_r'
#         return action
    
# class PTA2_DDCLong(PTA2_BDDCde):
#     '''Игнор Шорта'''
#     def __call__(self, row, *args, **kwds):
#         action = super().__call__(row, *args, **kwds)
#         if action:
#             if 'short' in action:
#                 action = action.replace('short','long')+'_r'
#             elif 'long' in action:
#                 return None
#         return action
# class PTA2_DDCShort(PTA2_BDDCde):
    # '''Игнор лонга'''
    # def __call__(self, row, *args, **kwds):
    #     action = super().__call__(row, *args, **kwds)
    #     if action:
    #         if 'long' in action:
    #             action = action.replace('long','short')+'_r'
    #         elif 'short' in action:
    #             return None
    #     return action
    

# универсальный
# TODO enter_price
class PTA2_UDC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,slope=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.slope = slope
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_dynamics_ma(df,self.period//2,'avarege')
        df = add_enter_price(df,lambda row:get_universal_r(row,'middle','middle'))
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self,row, *args, **kwds):
        if row['high'] == row['max_hb']:
            if row['dynamics_ma'] > self.slope:
                return 'long_pw'
            else:
                return 'short_pw'
        elif row['low'] == row['min_hb']:
            if row['dynamics_ma'] < -self.slope:
                return 'short_pw'
            else:
                return 'long_pw' 
        else:
            if row['low'] < row['avarege']:
                if row['dynamics_ma'] > self.slope:
                    return 'close_short_pw'
                else:
                    return "close_long_pw"
            if row['high'] > row['avarege']:
                if row['dynamics_ma'] < -self.slope:
                    return "close_long_pw"
                else:
                    return "close_short_pw"
class PTA2_AUDC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,slope=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.slope = slope
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_dynamics_ma(df,self.period//2,'avarege')
        df = add_enter_price(df,lambda row:get_universal_r(row,'middle','middle'))
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self,row, *args, **kwds):
        if row['high'] == row['max_hb']:
            if row['dynamics_ma'] > self.slope:
                return 'short_pw'
            else:
                return 'long_pw'
        elif row['low'] == row['min_hb']:
            if row['dynamics_ma'] < -self.slope:
                return 'long_pw' 
            else:
                return 'short_pw'
        else:
            if row['low'] < row['avarege']:
                if row['dynamics_ma'] > self.slope:
                    return "close_long_pw"
                else:
                    return 'close_short_pw'
            if row['high'] > row['avarege']:
                if row['dynamics_ma'] < -self.slope:
                    return "close_short_pw"
                else:
                    return "close_long_pw"

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
                return 'short_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'long_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_short_pw'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_long_pw'
            
class PTA8_ODOBBY(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price(df,lambda row:get_universal_r(row,'middle','middle'))
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['over_bbu']:
                return 'short_pw'
        if row['low'] < row['bbd']:
            if row['over_bbd']:
                return 'long_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_short_pw'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_long_pw'


class PTA8_ODOBBY_FREE(PTA8_ODOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_enter_price(df,lambda row:get_universal_r(row,'middle','middle'))
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['over_bbu']:
                return 'short_pw'
        if row['low'] < row['bbd']:
            if row['over_bbd']:
                return 'long_pw'
        if row['low'] < row['sma']:
                return 'close_short_pw'
        if row['high'] > row['sma']:
                return 'close_long_pw'
        
    
class PTA8_ODOBBY_FREEr(PTA8_ODOBBY_FREE):
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['over_bbu']:
                return 'short_pw'
        if row['low'] < row['bbd']:
            if row['over_bbd']:
                return 'long_pw'
        
            
class PTA8_DOBBY_FREE(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price(df,get_price_dbb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'short_pw'
        if row['low'] < row['bbd']:
            return 'long_pw'
        if row['low'] < row['sma']:
            return 'close_short_pw'
        if row['high'] > row['sma']:
            return 'close_long_pw'
        
class PTA8_DOBBY_FREEr(PTA8_DOBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price(df,get_price_reverse_dbb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'short_pw'
        if row['low'] < row['bbd']:
            return 'long_pw'
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
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long_pw'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short_pw'
            
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
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_pw'
        if row['low'] < row['sma']:
            return 'close_long_pw'
        if row['high'] > row['sma']:
            return 'close_short_pw'
            
class PTA8_LOBBY(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_buffer_add(df,'bbu','bbd',5)
        df = add_enter_price(df,get_price_bb_buff)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['over_bbu']:
            return 'close_long'
        if row['over_bbd']:
            return 'close_short'
        if row['high'] > row['bbu']:
            if row['is_big']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big']:
                return 'short_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short'

class PTA8_LOBSTER(PTA8_LOBBY):
    def __call__(self, row, *args, **kwds):
        if row['over_bbu']:
            return 'close_long'
        if row['over_bbd']:
            return 'close_short'
        if not (row['high'] > row['bbu'] and row['low'] < row['bbd']):
            if row['high'] > row['bbu']:
                if row['is_big']:
                    return 'long_pw'
            if row['low'] < row['bbd']:
                if row['is_big']:
                    return 'short_pw'
            if row['low'] < row['sma']:
                if row['is_big']:
                    return 'close_long'
            if row['high'] > row['sma']:
                if row['is_big']:
                    return 'close_short' 
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
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big']:
                return 'short_pw'
        if row['low'] < row['sma']:
            if row['is_big']:
                return 'close_long_pw'
        if row['high'] > row['sma']:
            if row['is_big']:
                return 'close_short_pw'

class PTA8_OBBY_FREE(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price(df,get_price_bb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'long_pw'
        if row['low'] < row['bbd']:
            return 'short_pw'
        if row['low'] < row['sma']:
            return 'close_long_pw'
        if row['high'] > row['sma']:
            return 'close_short_pw'
        
class PTA8_OBBY_FREEr(PTA8_OBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price(df,get_price_reverse_bb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'long_pw'
        if row['low'] < row['bbd']:
            return 'short_pw'
        
class PTA8_OBBY_VOR(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_over_bb(df)
        df = add_enter_price(df,get_price_reverse_bb)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_pw'
        
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
    
# TODO
class PTA9_CRAB(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=5,multiplier=2,period_slow=20,slope=0.5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
        self.period_slow = period_slow
        self.slope = slope
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_donchan_channel(df,self.period_slow)
        df = add_vangerchik(df)
        df = add_simple_dynamics_ma(df,self.period_slow,'avarege')
        df['slope'] = self.slope
        df = add_enter_price(df,get_price_crab)
        max_period = max(self.period,self.period_slow)
        df = add_slice_df(df,period=max_period)
        return df

    def __call__(self, row, *args, **kwds):
        if row['sdm'] >= self.slope and row['sma'] > row['avarege']:
            if row['low'] <= row['sma'] and chep(row,row['long_price']):
                return 'long_pw'

        if row['sdm'] <= -self.slope and row['sma'] < row['avarege']:
            if row['high'] >= row['sma'] and chep(row,row['short_price']):
                return 'short_pw'

        if -self.slope < row['sdm'] < self.slope:
            if row['high'] > row['max_vg'] and chep(row,row['short_price']):
                return 'short_pw'
            if row['low'] < row['min_vg'] and chep(row,row['long_price']):
                return 'long_pw'
        if row['sdm'] >= self.slope and row['sma'] < row['avarege']:
            return 'close_long_mt'
        if row['sdm'] <= -self.slope and row['sma'] > row['avarege']:
            return 'close_short_mt'
        
class PTA9_RAB(PTA9_CRAB):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_donchan_channel(df,self.period_slow)
        df = add_vangerchik(df)
        df = add_simple_dynamics_ma(df,self.period_slow,'avarege')
        df['slope'] = self.slope
        df = add_enter_price(df,get_price_rab)
        max_period = max(self.period,self.period_slow)
        df = add_slice_df(df,period=max_period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['sdm'] >= self.slope and row['sma'] > row['avarege']:
            if row['low'] <= row['sma'] and chep(row,row['short_price']):
                return 'short_pw'

        if row['sdm'] <= -self.slope and row['sma'] < row['avarege']:
            if row['high'] >= row['sma'] and chep(row,row['long_price']):
                return 'long_pw'

        if -self.slope < row['sdm'] < self.slope:
            if row['high'] > row['max_vg'] and chep(row,row['short_price']):
                return 'long_pw'
            if row['low'] < row['min_vg'] and chep(row,row['long_price']):
                return 'short_pw'
        if row['sdm'] >= self.slope and row['sma'] < row['avarege']:
            return 'close_long_mt'
        if row['sdm'] <= -self.slope and row['sma'] > row['avarege']:
            return 'close_short_mt'