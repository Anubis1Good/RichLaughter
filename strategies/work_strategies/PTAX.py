import numpy as np
import pandas as pd
from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi,add_enter_price2close,add_macd,add_rsi_tw,add_adx,add_chop,add_kusuruken_channel,add_awesome_oscillator
from ForBots.Indicators.pva_indicators import add_benefit,add_velcro_indicator
from ForBots.Indicators.help_pva_indicators import get_all_enter_exit_DC,get_all_lup
from utils.help_trades import reverse_action,chep
from strategies.work_strategies.BaseTA import BaseTABitget


# BD
class PTA10_MAGIC(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=26, period2=12, period3=9):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
    def preprocessing(self, df):
        df = add_macd(df,self.period2,self.period,self.period3)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # Покупка
        df.loc[df['macd'] < df['signal_line'], 'signal'] = -1  # Продажа
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
class PTA10_WIZARD(BaseTABitget):
    'period=26, period2=12, period3=9,threshold=20,threshold_adx=20'
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=26, period2=12, period3=9,threshold=20,threshold_adx=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.threshold = threshold
        self.threshold_adx = threshold_adx
    def preprocessing(self, df):
        df = add_macd(df,self.period2,self.period,self.period3)
        df = add_adx(df,self.period2)
        df = add_rsi_tw(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # Покупка
        df.loc[df['macd'] < df['signal_line'], 'signal'] = -1  # Продажа
        return df
    def __call__(self, row, *args, **kwds):
        if row['adx'] > self.threshold_adx:
            if row['signal'] == 1 and row['rsi_tw'] < 100-self.threshold:
                return 'long_pw'
            if row['signal'] == -1 and row['rsi_tw'] > self.threshold:
                return 'short_pw'
        if row['rsi_tw'] < self.threshold:
            return 'close_short_pw'
        if row['rsi_tw'] > 100-self.threshold:
            return 'close_long_pw'
        
class PTA10_SORCERER(BaseTABitget):
    'period=26, period2=12, period3=9,threshold=20,period4=12,toffset=10'
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=26, period2=12, period3=9,threshold=20,period4=12,toffset=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.period4 = period4
        self.threshold = threshold
        self.toffset = toffset
    def preprocessing(self, df):
        df = add_macd(df,self.period,self.period2,self.period3)
        df = add_rsi(df,self.period3)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # Покупка
        df.loc[df['macd'] < df['signal_line'], 'signal'] = -1  # Продажа
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1 and row['rsi'] < self.threshold:
            return 'long_pw'
        if row['signal'] == -1 and row['rsi'] > 100-self.threshold:
            return 'short_pw'
        if row['rsi'] < 100-self.threshold-self.toffset:
            return 'close_short_pw'
        if row['rsi'] > self.threshold+self.toffset:
            return 'close_long_pw'
        
class PTA11_KUSURUKEN(BaseTABitget):
    """period=60, period2=10, period3=20,threshold=20, kind_enter='hl'
    kind_enter -> hl | c
    """
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60, period2=10, period3=20,threshold=20,kind_enter='hl'):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.threshold = threshold
        self.kind_enter_l = 'low' if kind_enter == 'hl' else 'close'
        self.kind_enter_s = 'high' if kind_enter == 'hl' else 'close'
    def preprocessing(self, df):
        df = add_kusuruken_channel(df,self.period2,self.period)
        df = add_rsi(df,self.period3)
        df = add_chop(df,self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        # trend_context
        if row['sma'] > row['sma2']: 
            # long_context
            if row["avarege"] > row['avarege2']:
                if row['rsi'] > 100-self.threshold+10:
                    return 'close_long_pw'
                if row[self.kind_enter_l] <= row['avarege2']:
                    return 'long_pw'
            # short_context
            else:
                if row['rsi'] < self.threshold-10:
                    return 'close_short_pw'
                if row[self.kind_enter_s] >= row['avarege2']:
                    return 'short_pw'
        # range_context
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
            if row['low'] <= row['min_hb']:
                if nearest_long:
                    if row['rsi'] < self.threshold:
                        return 'long_pw'
            if row['high'] >= row['max_hb']:
                if row['rsi'] > 100-self.threshold:
                    return 'short_pw'

class PTA12_SWDDCr(BaseTABitget):
    """period=20,threshold=30,stop=1,shift=10,rolling=10"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30,stop=1,shift=10,rolling=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.stop = stop
        self.shift = shift
        self.rolling = rolling
    def preprocessing(self, df:pd.DataFrame):
        df = add_donchan_channel(df,self.period)
        df['buffer'] = (df['max_hb'] - df['min_hb']) * self.stop
        df['stop_long'] = (df['min_hb'] - df['buffer']).shift(self.shift).rolling(self.rolling).mean().rolling(self.rolling).min()
        df['stop_short'] = (df['max_hb'] + df['buffer']).shift(self.shift).rolling(self.rolling).mean().rolling(self.rolling).max()
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['close'] < row['stop_long']:
            return 'close_all_pw'
        if row['close'] > row['stop_short']:
            return 'close_all_pw'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
#TODO переделать
class PTA13_DWDDCr(BaseTABitget):
    """period=60,threshold=30,period2=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,threshold=30,period2=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.period2 = period2
    def preprocessing(self, df:pd.DataFrame):
        df = add_donchan_channel(df,self.period2)
        df = add_awesome_oscillator(df,long_period=self.period)
        df = add_rsi(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    if row['ao'] > 0:
                        return 'long_pw'
                    else:
                        return 'close_short_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                if row['ao'] < 0:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
            
class PTA14_RWDDCr(BaseTABitget):
    """period=20,threshold=30,period2=10, period3=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30,period2=10, period3=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.period2 = period2
        self.period3 = period3
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_chop(df,self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['sma'] > row['sma2']: 
            return 'close_all_pw'
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
            if row['low'] <= row['min_hb']:
                if nearest_long:
                    if row['rsi'] < self.threshold:
                        return 'long_pw'
            if row['high'] >= row['max_hb']:
                if row['rsi'] > 100-self.threshold:
                    return 'short_pw'
                
class PTA15_NOVA(BaseTABitget):
    """period=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df:pd.DataFrame):
        # df = add_donchan_channel(df,self.period)
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)

        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if not np.isnan(row['end_up']):
            return 'short_pw'
        if not np.isnan(row['end_down']):
            return 'long_pw'
        
class PTA15_KERRIGAN(BaseTABitget):
    """period=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df:pd.DataFrame):
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)

        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['low'] < row['min_hb']:
            return 'close_long_pw'
        if row['high'] > row['max_hb']:
            return 'close_short_pw'
        if not np.isnan(row['end_up']):
            return 'short_pw'
        if not np.isnan(row['end_down']):
            return 'long_pw'

class PTA15_WIDOWMAKER(BaseTABitget):
    """period=20,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df:pd.DataFrame):
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df = add_rsi(df,self.period)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if not np.isnan(row['end_down']):
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if not np.isnan(row['end_up']):
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class PTA15_SILVANA(BaseTABitget):
    """period=20,threshold=30,period2=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30,period2=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.period2 = period2
    def preprocessing(self, df:pd.DataFrame):
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df = add_rsi(df,self.period2)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['low'] < row['min_hb']:
            return 'close_long_pw'
        if row['high'] > row['max_hb']:
            return 'close_short_pw'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if not np.isnan(row['end_down']):
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
        if not np.isnan(row['end_up']):
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
            
class PTA15_TRACER(BaseTABitget):
    """period=20,mode=0"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,mode=0):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.mode = mode
    def preprocessing(self, df:pd.DataFrame):
        # df = add_donchan_channel(df,self.period)
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)

        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if not np.isnan(row['end_up']):
            if self.mode != 1:
                return 'short_pw'
            else:
                return 'close_long_pw'
        if not np.isnan(row['end_down']):
            if self.mode != -1:
                return 'long_pw'
            else:
                return 'close_short_pw'
            
class PTA15_VALLA(BaseTABitget):
    """period=20,mode=0"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,mode=0):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.mode = mode
    def preprocessing(self, df:pd.DataFrame):
        # df = add_donchan_channel(df,self.period)
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)

        df['end_up'] = np.where(
            (df['high'].shift(2) >= df['max_hb'].shift(2)) &  # i-2 бар обновил экстремум
            (df['high'].shift(1) < df['max_hb'].shift(1)) &   # i-1 бар НЕ обновил экстремум
            (df['high'] < df['max_hb']),                      # текущий бар тоже не обновляет
            df['high'], 
            np.nan
        )

        df['end_down'] = np.where(
            (df['low'].shift(2) <= df['min_hb'].shift(2)) &   # i-2 бар обновил экстремум
            (df['low'].shift(1) > df['min_hb'].shift(1)) &    # i-1 бар НЕ обновил экстремум
            (df['low'] > df['min_hb']),                       # текущий бар тоже не обновляет
            df['low'], 
            np.nan
        )

        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if not np.isnan(row['end_up']):
            if self.mode != 1:
                return 'short_pw'
            else:
                return 'close_long_pw'
        if not np.isnan(row['end_down']):
            if self.mode != -1:
                return 'long_pw'
            else:
                return 'close_short_pw'
            
class PTA16_LEORIC(BaseTABitget):
    """period=30,period2=10"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=30,period2=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period2)
        all_starts,all_ends = get_all_enter_exit_DC(df,'max_hb','min_hb')
        df = add_benefit(df,all_starts,all_ends,'DCr',self.period)
        all_starts,all_ends = get_all_enter_exit_DC(df,'max_hb','avarege')
        df = add_benefit(df,all_starts,all_ends,'DCmaxa',self.period)
        all_starts,all_ends = get_all_enter_exit_DC(df,'avarege','min_hb')
        df = add_benefit(df,all_starts,all_ends,'DCmina',self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def get_bests(self,row):
        target_indices_long = ['bl_DCr','bl_DCmaxa', 'bl_DCmina']
        target_indices_short = ['bs_DCr','bs_DCmaxa', 'bs_DCmina']
        filtered_l = row[target_indices_long]
        filtered_s = row[target_indices_short]
        best_l = filtered_l.idxmax()
        best_s = filtered_s.idxmax()
        if best_l == 'bl_DCr':
            kind_l = 'min_hb'
            kind_cl = 'max_hb'
        if best_l == 'bl_DCmaxa':
            kind_l = 'avarege'
            kind_cl = 'max_hb'
        if best_l == 'bl_DCmina':
            kind_l = 'min_hb'
            kind_cl = 'avarege'
        if best_s == 'bs_DCr':
            kind_s = 'max_hb'
            kind_cs = 'min_hb'
        if best_s == 'bs_DCmaxa':
            kind_s = 'max_hb'
            kind_cs = 'avarege'
        if best_s == 'bs_DCmina':
            kind_s = 'avarege'
            kind_cs = 'min_hb'
        return best_l,best_s,kind_l,kind_s,kind_cl,kind_cs
    
    def __call__(self, row, *args, **kwds):
        best_l,best_s,kind_l,kind_s,kind_cl,kind_cs = self.get_bests(row)
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row[best_l] > 0:
            if row['low'] <= row[kind_l] and nearest_long:
                    return 'long_pw'
        if row[best_s] > 0 and not nearest_long:
            if row['high'] >= row[kind_s]:
                    return 'short_pw'
        if row['low'] <= row[kind_cs] and not nearest_long:
            return 'close_short_pw'
        if row['high'] >= row[kind_cl] and nearest_long:
            return 'close_long_pw'
        # if row[best_l] < 0:
        #     return 'close_long_pw'
        # if row[best_s] < 0:
        #     return 'close_short_pw'

class PTA16_CHEN(BaseTABitget):
    """period=30,period2=10"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=30,period2=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period2)
        all_starts,all_ends = get_all_enter_exit_DC(df,'max_hb','min_hb')
        df = add_benefit(df,all_starts,all_ends,'DCr',self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        best_l = 'bl_DCr'
        best_s = 'bs_DCr'
        kind_l = 'min_hb'
        kind_s = 'max_hb'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row[best_l] > 0:
            if row['low'] <= row[kind_l] and nearest_long:
                    return 'long_pw'
        if row[best_s] > 0 and not nearest_long:
            if row['high'] >= row[kind_s]:
                    return 'short_pw'
        if row['low'] <= row[kind_l] and nearest_long:
            return 'close_short_pw'
        if row['high'] >= row[kind_s] and not nearest_long:
            return 'close_long_pw'
        if row[best_l] < 0:
            return 'close_long_pw'
        if row[best_s] < 0:
            return 'close_short_pw'
        
class PTA16_ARTANIS(BaseTABitget):
    """period=30,period2=10"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=30,period2=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
    def preprocessing(self, df):
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        all_starts,all_ends = get_all_lup(df,'max_hb','min_hb')
        df = add_benefit(df,all_starts,all_ends,'EDCr',self.period)
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1))&(df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1))&(df['low'] > df['min_hb']), df['low'], np.nan)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df

    def __call__(self, row, *args, **kwds):
        best_l = 'bl_EDCr'
        best_s = 'bs_EDCr'
        kind_l = 'min_hb'
        kind_s = 'max_hb'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if not np.isnan(row['end_up']):
            if row[best_s] > 0:
                return 'short_pw'
            else:
                return 'close_long_pw'
        if not np.isnan(row['end_down']):
            if row[best_l] > 0:
                return 'long_pw'
            else:
                return 'close_short_pw'
        if row[best_l] < 0:
            return 'close_long_pw'
        if row[best_s] < 0:
            return 'close_short_pw'

# TODO
class PTA17_PHOENIX(BaseTABitget):
    """period=60,threshold=30,period2=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,threshold=30,period2=20,threshold_velcro=50,rsi_mode=0):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.threshold_velcro = threshold_velcro
        self.period2 = period2
        self.rsi_mode = rsi_mode
    def preprocessing(self, df:pd.DataFrame):
        df = add_donchan_channel(df,self.period)
        df = add_velcro_indicator(df,self.period)
        df = add_rsi(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    if row['ao'] > 0:
                        return 'long_pw'
                    else:
                        return 'close_short_pw'
        if row['high'] >= row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                if row['ao'] < 0:
                    return 'short_pw'
                else:
                    return 'close_long_pw'