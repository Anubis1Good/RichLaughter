import numpy as np
from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_donchan_middle,add_donchan_prev,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi,add_enter_price2close,add_macd,add_rsi_tw
from ForBots.Indicators.price_funcs import get_price_dbb,get_price_reverse_dbb,get_price_bb,get_price_reverse_bb, get_price_bddc,get_price_ddc,get_price_rbddc,get_price_rddc,get_price_rddc_prev,get_price_ddc_prev,get_price_rddc_prev_ba,get_price_bb_buff,get_price_crab,get_price_rab,get_price_rddc_prev_ba_test,get_universal_r,get_universal
from utils.help_trades import reverse_action,chep
from strategies.work_strategies.BaseTA import BaseTABitget

# trend
# BD
class PTA2_BDDC(BaseTABitget):
    def preprocessing(self,df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_middle(df)
        df = add_enter_price2close(df)
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
            
#BD 
class PTA2_BDDCde(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_middle(df)
        df = add_enter_price2close(df)
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
#BD 
class PTA2_BDDCr(BaseTABitget):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] == row['max_hb']:
            return 'long_pw'
        elif row['low'] == row['min_hb']:
            return 'short_pw'
# conter-trend
#D         
class PTA2_DDCr(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
#D      
class PTA2_DDCrWork(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                return 'long_pw'
        if row['high'] == row['max_hb']:
            return 'short_pw'
#D         
class PTA4_WDDCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class PTA4_WDDCr2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi_tw'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb']:
            if row['rsi_tw'] > 100-self.threshold:
                return 'short_pw'
#D         
class PTA4_WDDCr2E(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi_tw'] < self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
        if row['high'] == row['max_hb']:
            if row['rsi_tw'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
#D         
class PTA4_WDDCrE(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
#D             
class PTA4_WDDCde(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
        if row['high'] < row['avarege']:
            return "close_long_pw"
        if row['low'] > row['avarege']:
            return "close_short_pw"
#D        
class PTA2_DDCrVG(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['min_vg']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['max_vg']:
            return 'short_pw'
#D        
class PTA4_WDDCrVG(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['min_vg']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['max_vg']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
#D  
class PTA2_DVCr(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_mean']:
            return 'short_pw'
#D  
class PTA4_WDVCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['top_mean']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

#BD    
class PTA2_BDVCr(PTA2_BDDCr):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                return 'short_pw'
        if row['high'] > row['top_mean']:
            return 'long_pw'

# TODO
# class PTA2_ALKASH(PTA2_BDDCr):
#     def preprocessing(self, df):
#         df = add_vodka_channel(df,self.period)
#         df = add_enter_price2close(df)
#         df = add_slice_df(df,period=self.period)
#         return df
#     def __call__(self, row, *args, **kwds):
#         nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
#         if row['low'] < row['bottom_mean']:
#             if nearest_long:
#                 return 'short_pw'
#         if row['high'] > row['top_mean']:
#             return 'long_pw'
#D        
class PTA2_VOLCHARA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,divider=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.divider = divider
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
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
#D  
class PTA2_LISICA(PTA2_VOLCHARA):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                return 'long_pw'
        if row['high'] > row['top_buff']:
            return 'short_pw'
#D  
class PTA4_WLISICA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,divider=1,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.divider = divider
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['top_buff']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

#BD revers volchara
class PTA2_ZAYAC(PTA2_VOLCHARA):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
#BD revers lisica
class PTA2_KOLOBOK(PTA2_LISICA):
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action
#D          
class PTA2_DDCde(PTA2_BDDCde):
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_donchan_prev(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        action = super().__call__(row, *args, **kwds)
        action = reverse_action(action)
        return action


# универсальный
#U
class PTA2_UDC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,slope=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.slope = slope
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_dynamics_ma(df,self.period//2,'avarege')
        df = add_enter_price2close(df)
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
# U
class PTA2_AUDC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,slope=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.slope = slope
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_dynamics_ma(df,self.period//2,'avarege')
        df = add_enter_price2close(df)
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

class PTA6_KAMA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=30, fast_ema=2):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fast_ema = fast_ema
        self.slow_ema = period

    def calculate_kama(self, df):
        """
        Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом KAMA
        """
        change = abs(df['close'] - df['close'].shift(self.period))
        volatility = df['close'].diff().abs().rolling(window=self.period).sum()
        efficiency_ratio = change / volatility

        fast_sc = 2 / (self.fast_ema + 1)
        slow_sc = 2 / (self.slow_ema + 1)
        smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

        df['kama'] = 0.0
        for i in range(self.period, len(df)):
            df.loc[df.index[i], 'kama'] = (
                df.loc[df.index[i - 1], 'kama'] +
                smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], 'kama'])
            )
        return df

    def preprocessing(self, df):
        """
        Предобработка данных: расчет KAMA и генерация сигналов.
        :param df: DataFrame с данными
        :return: DataFrame с добавленными сигналами
        """
        df = self.calculate_kama(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['close'] > df['kama'], 'signal'] = 1  # Покупка
        df.loc[df['close'] < df['kama'], 'signal'] = -1  # Продажа
        return df

    def __call__(self, row, *args, **kwds):
        """
        Генерация торговых сигналов.
        :param row: Строка данных
        :return: Сигнал для торговли
        """
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'

class PTA6_KAMA2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=10, fast_ema=2,  adx_period=14, adx_threshold=50):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fast_ema = fast_ema
        self.slow_ema = period
        self.adx_period = adx_period  # Период для расчета ADX
        self.adx_threshold = adx_threshold  # Порог силы тренда

    def calculate_kama(self, df):
        """
        Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом KAMA
        """
        change = abs(df['close'] - df['close'].shift(self.period))
        volatility = df['close'].diff().abs().rolling(window=self.period).sum()
        efficiency_ratio = change / volatility

        fast_sc = 2 / (self.fast_ema + 1)
        slow_sc = 2 / (self.slow_ema + 1)
        smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

        df['kama'] = 0.0
        for i in range(self.period, len(df)):
            df.loc[df.index[i], 'kama'] = (
                df.loc[df.index[i - 1], 'kama'] +
                smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], 'kama'])
            )
        return df

    def calculate_adx(self, df):
        """
        Расчет индикатора ADX (Average Directional Index).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом ADX
        """
        # Расчет True Range (TR)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )

        # Расчет Positive Directional Movement (+DM) и Negative Directional Movement (-DM)
        df['plus_dm'] = np.where(
            (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
            np.maximum(df['high'] - df['high'].shift(1), 0),
            0
        )
        df['minus_dm'] = np.where(
            (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
            np.maximum(df['low'].shift(1) - df['low'], 0),
            0
        )

        # Сглаживание TR, +DM, -DM
        df['tr_smooth'] = df['tr'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['plus_dm_smooth'] = df['plus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['minus_dm_smooth'] = df['minus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()

        # Расчет +DI и -DI
        df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
        df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100

        # Расчет ADX
        df['dx'] = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
        df['adx'] = df['dx'].rolling(window=self.adx_period, min_periods=self.adx_period).mean()

        return df

    def preprocessing(self, df):
        """
        Предобработка данных: расчет KAMA, ADX и генерация сигналов.
        :param df: DataFrame с данными
        :return: DataFrame с добавленными сигналами
        """
        df = self.calculate_kama(df)
        df = self.calculate_adx(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Фильтрация сигналов по ADX
        df.loc[(df['close'] > df['kama']) & (df['adx'] > self.adx_threshold), 'signal'] = 1  # Покупка
        df.loc[(df['close'] < df['kama']) & (df['adx'] > self.adx_threshold), 'signal'] = -1  # Продажа
        return df

    def __call__(self, row, *args, **kwds):
        """
        Генерация торговых сигналов.
        :param row: Строка данных
        :return: Сигнал для торговли
        """
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class PTA6_KAMAZ2(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=10, fast_ema=2,  adx_period=14, adx_threshold=25):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fast_ema = fast_ema
        self.slow_ema = period
        self.adx_period = adx_period  # Период для расчета ADX
        self.adx_threshold = adx_threshold  # Порог силы тренда

    def calculate_kama(self, df):
        """
        Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом KAMA
        """
        change = abs(df['close'] - df['close'].shift(self.period))
        volatility = df['close'].diff().abs().rolling(window=self.period).sum()
        efficiency_ratio = change / volatility

        fast_sc = 2 / (self.fast_ema + 1)
        slow_sc = 2 / (self.slow_ema + 1)
        smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

        df['kama'] = 0.0
        for i in range(self.period, len(df)):
            df.loc[df.index[i], 'kama'] = (
                df.loc[df.index[i - 1], 'kama'] +
                smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], 'kama'])
            )
        return df

    def calculate_adx(self, df):
        """
        Расчет индикатора ADX (Average Directional Index).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом ADX
        """
        # Расчет True Range (TR)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )

        # Расчет Positive Directional Movement (+DM) и Negative Directional Movement (-DM)
        df['plus_dm'] = np.where(
            (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
            np.maximum(df['high'] - df['high'].shift(1), 0),
            0
        )
        df['minus_dm'] = np.where(
            (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
            np.maximum(df['low'].shift(1) - df['low'], 0),
            0
        )

        # Сглаживание TR, +DM, -DM
        df['tr_smooth'] = df['tr'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['plus_dm_smooth'] = df['plus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['minus_dm_smooth'] = df['minus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()

        # Расчет +DI и -DI
        df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
        df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100

        # Расчет ADX
        df['dx'] = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
        df['adx'] = df['dx'].rolling(window=self.adx_period, min_periods=self.adx_period).mean()

        return df

    def preprocessing(self, df):
        """
        Предобработка данных: расчет KAMA, ADX и генерация сигналов.
        :param df: DataFrame с данными
        :return: DataFrame с добавленными сигналами
        """
        df = self.calculate_kama(df)
        df = self.calculate_adx(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Фильтрация сигналов по ADX
        df.loc[(df['close'] > df['kama']) & (df['adx'] < self.adx_threshold), 'signal'] = 1  # Покупка
        df.loc[(df['close'] < df['kama']) & (df['adx'] < self.adx_threshold), 'signal'] = -1  # Продажа
        return df

    def __call__(self, row, *args, **kwds):
        """
        Генерация торговых сигналов.
        :param row: Строка данных
        :return: Сигнал для торговли
        """
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class PTA6_KAMA3(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=10, fast_ema=2, slow_ema=30, adx_period=14, adx_threshold=25, slow_kama_multiplier=3):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema
        self.adx_period = adx_period  # Период для расчета ADX
        self.adx_threshold = adx_threshold  # Порог силы тренда
        self.slow_kama_multiplier = slow_kama_multiplier  # Множитель для медленной KAMA

    def calculate_kama(self, df, period):
        """
        Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
        :param df: DataFrame с данными
        :param period: Период для расчета KAMA
        :return: DataFrame с добавленным столбцом KAMA
        """
        change = abs(df['close'] - df['close'].shift(period))
        volatility = df['close'].diff().abs().rolling(window=period).sum()
        efficiency_ratio = change / volatility

        fast_sc = 2 / (self.fast_ema + 1)
        slow_sc = 2 / (self.slow_ema + 1)
        smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

        df[f'kama_{period}'] = 0.0
        for i in range(period, len(df)):
            df.loc[df.index[i], f'kama_{period}'] = (
                df.loc[df.index[i - 1], f'kama_{period}'] +
                smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], f'kama_{period}'])
            )
        return df

    def calculate_adx(self, df):
        """
        Расчет индикатора ADX (Average Directional Index).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом ADX
        """
        # Расчет True Range (TR)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )

        # Расчет Positive Directional Movement (+DM) и Negative Directional Movement (-DM)
        df['plus_dm'] = np.where(
            (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
            np.maximum(df['high'] - df['high'].shift(1), 0),
            0
        )
        df['minus_dm'] = np.where(
            (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
            np.maximum(df['low'].shift(1) - df['low'], 0),
            0
        )

        # Сглаживание TR, +DM, -DM
        df['tr_smooth'] = df['tr'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['plus_dm_smooth'] = df['plus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['minus_dm_smooth'] = df['minus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()

        # Расчет +DI и -DI
        df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
        df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100

        # Расчет ADX
        df['dx'] = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
        df['adx'] = df['dx'].rolling(window=self.adx_period, min_periods=self.adx_period).mean()

        return df

    def preprocessing(self, df):
        """
        Предобработка данных: расчет KAMA (быстрой и медленной), ADX и генерация сигналов.
        :param df: DataFrame с данными
        :return: DataFrame с добавленными сигналами
        """
        # Расчет быстрой KAMA
        df = self.calculate_kama(df, self.period)
        # Расчет медленной KAMA
        slow_kama_period = self.period * self.slow_kama_multiplier
        df = self.calculate_kama(df, slow_kama_period)
        # Расчет ADX
        df = self.calculate_adx(df)
        # Добавление вспомогательных столбцов
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Фильтрация сигналов по ADX и медленной KAMA
        df.loc[
            (df['close'] > df['kama_10']) &  # Цена выше быстрой KAMA
            (df['close'] > df[f'kama_{slow_kama_period}']) &  # Цена выше медленной KAMA
            (df['adx'] > self.adx_threshold),  # ADX выше порога
            'signal'
        ] = 1  # Покупка

        df.loc[
            (df['close'] < df['kama_10']) &  # Цена ниже быстрой KAMA
            (df['close'] < df[f'kama_{slow_kama_period}']) &  # Цена ниже медленной KAMA
            (df['adx'] > self.adx_threshold),  # ADX выше порога
            'signal'
        ] = -1  # Продажа

        return df

    def __call__(self, row, *args, **kwds):
        """
        Генерация торговых сигналов.
        :param row: Строка данных
        :return: Сигнал для торговли
        """
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class PTA6_KAMA4(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=30, fast_ema=2, slow_ema=30, adx_period=14, adx_threshold=25, slow_kama_multiplier=3, chop_period=14, chop_threshold=40):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema
        self.adx_period = adx_period  # Период для расчета ADX
        self.adx_threshold = adx_threshold  # Порог силы тренда
        self.slow_kama_multiplier = slow_kama_multiplier  # Множитель для медленной KAMA
        self.chop_period = chop_period  # Период для расчета CHOP
        self.chop_threshold = chop_threshold  # Порог для фильтрации CHOP

    def calculate_kama(self, df, period):
        """
        Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
        :param df: DataFrame с данными
        :param period: Период для расчета KAMA
        :return: DataFrame с добавленным столбцом KAMA
        """
        change = abs(df['close'] - df['close'].shift(period))
        volatility = df['close'].diff().abs().rolling(window=period).sum()
        efficiency_ratio = change / volatility

        fast_sc = 2 / (self.fast_ema + 1)
        slow_sc = 2 / (self.slow_ema + 1)
        smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

        df[f'kama_{period}'] = 0.0
        for i in range(period, len(df)):
            df.loc[df.index[i], f'kama_{period}'] = (
                df.loc[df.index[i - 1], f'kama_{period}'] +
                smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], f'kama_{period}'])
            )
        return df

    def calculate_adx(self, df):
        """
        Расчет индикатора ADX (Average Directional Index).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом ADX
        """
        # Расчет True Range (TR)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )

        # Расчет Positive Directional Movement (+DM) и Negative Directional Movement (-DM)
        df['plus_dm'] = np.where(
            (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
            np.maximum(df['high'] - df['high'].shift(1), 0),
            0
        )
        df['minus_dm'] = np.where(
            (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
            np.maximum(df['low'].shift(1) - df['low'], 0),
            0
        )

        # Сглаживание TR, +DM, -DM
        df['tr_smooth'] = df['tr'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['plus_dm_smooth'] = df['plus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['minus_dm_smooth'] = df['minus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()

        # Расчет +DI и -DI
        df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
        df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100

        # Расчет ADX
        df['dx'] = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
        df['adx'] = df['dx'].rolling(window=self.adx_period, min_periods=self.adx_period).mean()

        return df

    def calculate_chop(self, df):
        """
        Расчет индикатора CHOP (Choppiness Index).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом CHOP
        """
        # Расчет True Range (TR)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )

        # Сумма TR за период
        df['tr_sum'] = df['tr'].rolling(window=self.chop_period).sum()

        # Максимальная и минимальная цена за период
        df['high_max'] = df['high'].rolling(window=self.chop_period).max()
        df['low_min'] = df['low'].rolling(window=self.chop_period).min()

        # Расчет CHOP
        df['chop'] = 100 * np.log10(df['tr_sum'] / (df['high_max'] - df['low_min'])) / np.log10(self.chop_period)
        return df

    def preprocessing(self, df):
        """
        Предобработка данных: расчет KAMA (быстрой и медленной), ADX, CHOP и генерация сигналов.
        :param df: DataFrame с данными
        :return: DataFrame с добавленными сигналами
        """
        # Расчет быстрой KAMA
        df = self.calculate_kama(df, self.period)
        # Расчет медленной KAMA
        slow_kama_period = self.period * self.slow_kama_multiplier
        df = self.calculate_kama(df, slow_kama_period)
        # Расчет ADX
        df = self.calculate_adx(df)
        # Расчет CHOP
        df = self.calculate_chop(df)
        # Добавление вспомогательных столбцов
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Фильтрация сигналов по ADX, медленной KAMA и CHOP
        df.loc[
            (df['close'] > df['kama_10']) &  # Цена выше быстрой KAMA
            (df['close'] > df[f'kama_{slow_kama_period}']) &  # Цена выше медленной KAMA
            (df['adx'] > self.adx_threshold) &  # ADX выше порога
            (df['chop'] < self.chop_threshold),  # CHOP ниже порога (рынок в тренде)
            'signal'
        ] = 1  # Покупка

        df.loc[
            (df['close'] < df['kama_10']) &  # Цена ниже быстрой KAMA
            (df['close'] < df[f'kama_{slow_kama_period}']) &  # Цена ниже медленной KAMA
            (df['adx'] > self.adx_threshold) &  # ADX выше порога
            (df['chop'] < self.chop_threshold),  # CHOP ниже порога (рынок в тренде)
            'signal'
        ] = -1  # Продажа

        return df

    def __call__(self, row, *args, **kwds):
        """
        Генерация торговых сигналов.
        :param row: Строка данных
        :return: Сигнал для торговли
        """
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'

# TODO
class PTA6_KAMA5(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=10, fast_ema=2, slow_ema=30, adx_period=14, adx_threshold=25, slow_kama_multiplier=3, chop_period=14, chop_threshold=40, bb_period=20, bb_std=2, bbw_threshold=2):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema
        self.adx_period = adx_period  # Период для расчета ADX
        self.adx_threshold = adx_threshold  # Порог силы тренда
        self.slow_kama_multiplier = slow_kama_multiplier  # Множитель для медленной KAMA
        self.chop_period = chop_period  # Период для расчета CHOP
        self.chop_threshold = chop_threshold  # Порог для фильтрации CHOP
        self.bb_period = bb_period  # Период для расчета Bollinger Bands
        self.bb_std = bb_std  # Количество стандартных отклонений для Bollinger Bands
        self.bbw_threshold = bbw_threshold  # Порог для фильтрации BBW

    def calculate_kama(self, df, period):
        """
        Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
        :param df: DataFrame с данными
        :param period: Период для расчета KAMA
        :return: DataFrame с добавленным столбцом KAMA
        """
        change = abs(df['close'] - df['close'].shift(period))
        volatility = df['close'].diff().abs().rolling(window=period).sum()
        efficiency_ratio = change / volatility

        fast_sc = 2 / (self.fast_ema + 1)
        slow_sc = 2 / (self.slow_ema + 1)
        smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

        df[f'kama_{period}'] = 0.0
        for i in range(period, len(df)):
            df.loc[df.index[i], f'kama_{period}'] = (
                df.loc[df.index[i - 1], f'kama_{period}'] +
                smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], f'kama_{period}'])
            )
        return df

    def calculate_adx(self, df):
        """
        Расчет индикатора ADX (Average Directional Index).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом ADX
        """
        # Расчет True Range (TR)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )

        # Расчет Positive Directional Movement (+DM) и Negative Directional Movement (-DM)
        df['plus_dm'] = np.where(
            (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
            np.maximum(df['high'] - df['high'].shift(1), 0),
            0
        )
        df['minus_dm'] = np.where(
            (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
            np.maximum(df['low'].shift(1) - df['low'], 0),
            0
        )

        # Сглаживание TR, +DM, -DM
        df['tr_smooth'] = df['tr'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['plus_dm_smooth'] = df['plus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()
        df['minus_dm_smooth'] = df['minus_dm'].rolling(window=self.adx_period, min_periods=self.adx_period).sum()

        # Расчет +DI и -DI
        df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
        df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100

        # Расчет ADX
        df['dx'] = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
        df['adx'] = df['dx'].rolling(window=self.adx_period, min_periods=self.adx_period).mean()

        return df

    def calculate_chop(self, df):
        """
        Расчет индикатора CHOP (Choppiness Index).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом CHOP
        """
        # Расчет True Range (TR)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )

        # Сумма TR за период
        df['tr_sum'] = df['tr'].rolling(window=self.chop_period).sum()

        # Максимальная и минимальная цена за период
        df['high_max'] = df['high'].rolling(window=self.chop_period).max()
        df['low_min'] = df['low'].rolling(window=self.chop_period).min()

        # Расчет CHOP
        df['chop'] = 100 * np.log10(df['tr_sum'] / (df['high_max'] - df['low_min'])) / np.log10(self.chop_period)
        return df

    def calculate_bbw(self, df):
        """
        Расчет индикатора BBW (Bollinger Bands Width).
        :param df: DataFrame с данными
        :return: DataFrame с добавленным столбцом BBW
        """
        # Расчет скользящей средней и стандартного отклонения
        df['sma'] = df['close'].rolling(window=self.bb_period).mean()
        df['std'] = df['close'].rolling(window=self.bb_period).std()

        # Расчет верхней и нижней полосы Боллинджера
        df['upper_band'] = df['sma'] + (df['std'] * self.bb_std)
        df['lower_band'] = df['sma'] - (df['std'] * self.bb_std)

        # Расчет BBW
        df['bbw'] = ((df['upper_band'] - df['lower_band']) / df['sma'])*100
        return df

    def preprocessing(self, df):
        """
        Предобработка данных: расчет KAMA (быстрой и медленной), ADX, CHOP, BBW и генерация сигналов.
        :param df: DataFrame с данными
        :return: DataFrame с добавленными сигналами
        """
        # Расчет быстрой KAMA
        df = self.calculate_kama(df, self.period)
        # Расчет медленной KAMA
        slow_kama_period = self.period * self.slow_kama_multiplier
        df = self.calculate_kama(df, slow_kama_period)
        # Расчет ADX
        df = self.calculate_adx(df)
        # Расчет CHOP
        df = self.calculate_chop(df)
        # Расчет BBW
        df = self.calculate_bbw(df)
        # Добавление вспомогательных столбцов
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа

        # Фильтрация сигналов по ADX, медленной KAMA, CHOP и BBW
        df.loc[
            (df['close'] > df['kama_10']) &  # Цена выше быстрой KAMA
            (df['close'] > df[f'kama_{slow_kama_period}']) &  # Цена выше медленной KAMA
            (df['adx'] > self.adx_threshold) &  # ADX выше порога
            (df['chop'] < self.chop_threshold) &  # CHOP ниже порога (рынок в тренде)
            (df['bbw'] < self.bbw_threshold),  # BBW выше порога (высокая волатильность)
            'signal'
        ] = 1  # Покупка

        df.loc[
            (df['close'] < df['kama_10']) &  # Цена ниже быстрой KAMA
            (df['close'] < df[f'kama_{slow_kama_period}']) &  # Цена ниже медленной KAMA
            (df['adx'] > self.adx_threshold) &  # ADX выше порога
            (df['chop'] < self.chop_threshold) &  # CHOP ниже порога (рынок в тренде)
            (df['bbw'] < self.bbw_threshold),  # BBW выше порога (высокая волатильность)
            'signal'
        ] = -1  # Продажа

        return df

    def __call__(self, row, *args, **kwds):
        """
        Генерация торговых сигналов.
        :param row: Строка данных
        :return: Сигнал для торговли
        """
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'  
# D 
class PTA8_DOBBY(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
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
            

#D      
class PTA8_DOBBY_FREE(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
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
#D  
class PTA8_DOBBY_FREEr(PTA8_DOBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'short_pw'
        if row['low'] < row['bbd']:
            return 'long_pw'
#D  
class PTA8_WDOBBY_FREEr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bbd']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['bbu']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

# trend
# BD
class PTA8_OBBY(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
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
#BD        
class PTA8_OBBY_PF(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
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
#BD 
class PTA8_LOBBY(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
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
#BD 
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
#BD 
class PTA8_FOBBY(PTA8_DOBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_enter_price2close(df)
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
#BD 
class PTA8_OBBY_FREE(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
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
#BD           
class PTA8_OBBY_FREEr(PTA8_OBBY_FREE):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            return 'long_pw'
        if row['low'] < row['bbd']:
            return 'short_pw'
#BD               
class PTA8_OBBY_VOR(PTA8_OBBY):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_big_volume(df,self.period)
        df = add_over_bb(df)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'long_pw'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'short_pw'
        

# TODO
# D
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
        df = add_enter_price2close(df)
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
            return 'close_long_pw'
        if row['sdm'] <= -self.slope and row['sma'] > row['avarege']:
            return 'close_short_pw'
# BD
class PTA9_RAB(PTA9_CRAB):
    def preprocessing(self, df):
        df = add_bollinger(df,self.period_slow,multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df,self.period_slow)
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_simple_dynamics_ma(df,self.period,'avarege')
        df['slope'] = self.slope
        df = add_enter_price2close(df)
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
            return 'close_long_pw'
        if row['sdm'] <= -self.slope and row['sma'] > row['avarege']:
            return 'close_short_pw'
