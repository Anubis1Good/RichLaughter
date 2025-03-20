import numpy as np
from request_functions.download_bitget import get_df
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_donchan_middle,add_donchan_prev,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi,add_enter_price2close,add_macd,add_rsi_tw,add_adx
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