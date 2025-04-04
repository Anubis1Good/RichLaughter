import numpy as np
from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_bollinger,add_big_volume,add_attached_bb,add_over_bb,add_dynamics_ma,add_slice_df,add_simple_dynamics_ma,add_sma,add_enter_price,add_enter_price2close,add_awesome_oscillator,add_rsi,add_ema,add_adx, add_atr
from ForBots.Indicators.price_funcs import get_universal_r,get_universal
from strategies.work_strategies.BaseTA import BaseTABitget

# class STA1e:
#     def __init__(self,symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=1,period=20,multiplier=2,slope=5):
#         self.period = period
#         self.multiplier = multiplier
#         self.symbol = symbol
#         self.granularity = granularity
#         self.productType = productType
#         self.n_parts = n_parts
#         self.bbu_attached = False
#         self.bbd_attached = False
#         self.slope = slope

#     def preprocessing(self,df):
#         df = add_bollinger(df,self.period,multiplier=self.multiplier)
#         df = add_big_volume(df,self.period)
#         df = add_over_bb(df)
#         df = add_attached_bb(df)
#         df = add_dynamics_ma(df,period=self.period//2)
#         df = add_slice_df(df,period=self.period)
#         return df
    
#     def get_test_df(self,df):
#         df = self.preprocessing(df)
#         return df
    
#     def get_row(self):
#         limit = self.period*2
#         df = get_df(self.symbol,self.granularity,self.productType,limit)
#         df = self.preprocessing(df)
#         return df.iloc[-1]
    
#     def __call__(self, row, *args, **kwds):
#         if row['attached_change']:
#             if row['bbu_attached'] != self.bbu_attached:
#                 return 'close_long'
#             if row['bbd_attached'] != self.bbd_attached:
#                 return 'close_short'
#         self.bbu_attached = row['bbu_attached']
#         self.bbd_attached = row['bbd_attached']
#         if row['dynamics_ma'] > self.slope:
#             if row['low'] < row['sma']:
#                 return 'long'
#         if row['dynamics_ma'] < -self.slope:
#             if row['high'] > row['sma']:
#                 return 'short'
#         if row['is_big']:
#             if row['bbu_attached']:
#                 return 'close_long'
#             if row['bbd_attached']:
#                 return 'close_short'
#         if row['over_bbu']:
#             return 'close_long'
#         if row['over_bbd']:
#             return 'close_short'

class STA1_LITE(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2,slope=0.5,period2=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
        self.slope = slope
        self.period2 = period2
    def preprocessing(self, df):
        df = add_sma(df,self.period2)
        df= df.rename(columns={'sma':'sma2'})
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_over_bb(df)
        df = add_simple_dynamics_ma(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['sdm'] >= self.slope:
            if row['high'] > row['bbu'] and row['is_big']:
                return 'close_long_pw'
            if row['over_bbu']:
                return 'close_long_pw'
            if row['low'] < row['sma'] and row['sma2'] > row['sma']:
                return 'long_pw'
        elif row['sdm'] <= -self.slope:
            if row['over_bbd']:
                return 'close_short_pw'
            if row['low'] < row['bbd'] and row['is_big']:
                return 'close_short_pw'
            if row['high'] > row['sma'] and row['sma2'] < row['sma']:
                return 'short_pw'
        else:
            pass

class STA2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=30,multiplier=2,slope=0.5,period2=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
        self.slope = slope
        self.period2 = period2
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_over_bb(df)
        df = add_adx(df,self.period2)
        df = add_rsi(df,self.period2)
        df = add_ema(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        pass
        # if row['sdm'] >= self.slope:
        #     if row['high'] > row['bbu'] and row['is_big']:
        #         return 'close_long_pw'
        #     if row['over_bbu']:
        #         return 'close_long_pw'
        #     if row['low'] < row['sma'] and row['sma2'] > row['sma']:
        #         return 'long_pw'
        # elif row['sdm'] <= -self.slope:
        #     if row['over_bbd']:
        #         return 'close_short_pw'
        #     if row['low'] < row['bbd'] and row['is_big']:
        #         return 'close_short_pw'
        #     if row['high'] > row['sma'] and row['sma2'] < row['sma']:
        #         return 'short_pw'
        # else:
        #     pass

class STA_mini(BaseTABitget):
    """period=20,go_long=True"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,go_long=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.go_long = go_long
    def preprocessing(self, df):
        df = add_bollinger(df,self.period)
        df = add_big_volume(df,self.period,3)
        df = add_over_bb(df)
        df = add_rsi(df,self.period)
        df['sma_delta'] = df['sma'].pct_change()
        df['dynamic_sma'] = df['sma_delta'].rolling(self.period).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if self.go_long and row['dynamic_sma'] < -0.00001:
            return 'close_long_pw'
        if not self.go_long and row['dynamic_sma'] > 0.00001:
            return 'close_short_pw'
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu'] or row['rsi'] > 85:
                return 'close_long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd'] or row['rsi'] < 15:
                return 'close_short_pw'
        if row['low'] < row['sma'] and self.go_long and row['dynamic_sma'] > 0:
            return 'long_pw'
        if row['high'] > row['sma']and not self.go_long and row['dynamic_sma'] < 0:
            return 'short_pw'

# TODO есть идея нормализовать значения delta sma и по ним вычислять тренд
class STA_FAST(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", 
                 n_parts=1, period=50, trend_period=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.trend_period = trend_period  # Период для определения тренда
    
    def preprocessing(self, df):
        # Базовые индикаторы
        df = add_bollinger(df, period=self.period, multiplier=2)
        df = add_ema(df, period=self.period//2)
        
        # Улучшенное определение тренда
        df['ma_fast'] = df['close'].rolling(3).mean()
        df['ma_slow'] = df['close'].rolling(self.trend_period).mean()
        df['fast_up'] = df['ma_fast'] > df['ma_slow']  # Быстрая MA выше медленной
        
        # Альтернативный вариант - наклон скользящей средней
        df['ema_angle'] = df['ema'].diff(3)  # Изменение EMA за 3 бара
        df['trend_up'] = df['ema_angle'] > 0  # EMA растет
        
        # Комбинированный тренд (можно использовать любой вариант)
        df['trend'] = df['fast_up'] | df['trend_up']
        
        # Детекция открепления
        df['bbu_detach'] = (df['high'] < df['bbu']) & (df['high'].shift(1) < df['bbu'].shift(1))
        df['bbd_detach'] = (df['low'] > df['bbd']) & (df['low'].shift(1) > df['bbd'].shift(1))
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        # Условия входа
        if row['low'] < row['ema'] and row['trend']:
            return 'long_pw'
            
        if row['high'] > row['ema'] and not row['trend']:
            return 'short_pw'
            
        # Условия выхода
        if row['bbu_detach'] and row['trend']:
            return 'close_long_pw'
            
        if row['bbd_detach'] and not row['trend']:
            return 'close_short_pw'
        
        return None