import numpy as np
import pandas as pd
from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi,add_enter_price2close,add_macd,add_rsi_tw,add_adx,add_chop,add_kusuruken_channel,add_awesome_oscillator
from ForBots.Indicators.pva_indicators import add_benefit,add_velcro_indicator,add_pc_stair_fast,add_integrity_index,add_cascade_channel,add_assessment_motion_index,add_hope_channel
from ForBots.Indicators.help_pva_indicators import get_all_enter_exit_DC,get_all_lup
from utils.help_trades import reverse_action,chep
from strategies.work_strategies.BaseTA import BaseTABitget

class PTA20_HANZO(BaseTABitget):
    """period=100,period2=5,mult_big=2,mult_small=0.5"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,period2=5,mult_big=2,mult_small=0.5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.mult_big = mult_big
        self.mult_small =mult_small
    def preprocessing(self, df):
        df['smab'] = df['middle'].rolling(window=self.period).mean()
        std_dev = df['middle'].rolling(window=self.period).std()
        # Вычисляем верхнюю и нижнюю полосы Боллинджера
        df['bbub'] = df['smab'] + (self.mult_big * std_dev)
        df['bbdb'] = df['smab'] - (self.mult_big * std_dev)
        df['mub'] = (df['bbub'] + df['smab']) / 2
        df['mdb'] = (df['bbdb'] + df['smab']) / 2
        df = add_bollinger(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        # long
        if row['low'] > row['smab']:
            if row['close'] >= row['mub']:
                if row['high'] >= row['bbu'] and row['close'] < row['bbub']:
                    return 'close_long_pw'
            else:
                if row['low'] <= row['bbd'] and nearest_long:
                    return 'long_pw'
            if row['sma'] > row['smab']:
                return 'close_short_pw'
        # short
        if row['high'] < row['smab']:
            if row['close'] <= row['mdb']:
                if row['low'] <= row['bbd'] and row['close'] > row['bbdb']:
                    return 'close_short_pw'
                if row['high'] >= row['bbu'] and not nearest_long:
                    return 'short_pw'
            if row['sma'] < row['smab']:
                return 'close_long_pw'
            
class PTA20_HOGGER(BaseTABitget):
    """period=100,period2=5,mult_big=2,mult_small=0.5,threshold_enter=40,threshold_exit=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,period2=5,mult_big=2,mult_small=0.5,threshold_enter=40,threshold_exit=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.mult_big = mult_big
        self.mult_small = mult_small
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
    def preprocessing(self, df):
        df['smab'] = df['middle'].rolling(window=self.period).mean()
        std_dev = df['middle'].rolling(window=self.period).std()
        # Вычисляем верхнюю и нижнюю полосы Боллинджера
        df['bbub'] = df['smab'] + (self.mult_big * std_dev)
        df['bbdb'] = df['smab'] - (self.mult_big * std_dev)
        df['mub'] = (df['bbub'] + df['smab']) / 2
        df['mdb'] = (df['bbdb'] + df['smab']) / 2
        df = add_bollinger(df,self.period2)
        df = add_rsi(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        # nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        # long
        if row['low'] > row['smab']:
            if row['close'] >= row['mub']:
                if row['high'] >= row['bbu'] and row['close'] < row['bbub'] and row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long_pw'
            else:
                if row['low'] <= row['bbd'] and row['rsi'] < self.threshold_enter:
                    return 'long_pw'
            if row['sma'] > row['smab']:
                return 'close_short_pw'
        # short
        if row['high'] < row['smab']:
            if row['close'] <= row['mdb']:
                if row['low'] <= row['bbd'] and row['close'] > row['bbdb'] and row['rsi'] < self.threshold_exit:
                    return 'close_short_pw'
                if row['high'] >= row['bbu'] and row['rsi'] > 100 - self.threshold_enter:
                    return 'short_pw'
            if row['sma'] < row['smab']:
                return 'close_long_pw'
