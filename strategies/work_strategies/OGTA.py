from utils.help_trades import reverse_action
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.vsa_indicators import add_rails,add_rails_slice,add_allowance_rails,add_spred,add_OGTA2_rails_info
from ForBots.Indicators.classic_indicators import add_big_volume,add_slice_df,add_enter_price,add_delta_2v,add_sc_and_buffer,add_sma
from ForBots.Indicators.price_funcs import get_price_reverse_rails,get_universal_r

class OGTA1_Rails(BaseTABitget):
    def preprocessing(self, df):
        df = add_big_volume(df,self.period)
        df = add_rails(df)
        df = add_enter_price(df,get_price_reverse_rails)
        df = add_sc_and_buffer(df,'stop_short','short_price')
        df = df.rename(columns={'spred_channel':'spred_channel_short'})
        df = add_sc_and_buffer(df,'long_price','stop_long')
        df = df.rename(columns={'spred_channel':'spred_channel_long'})
        df = add_delta_2v(df,'short_price','long_price')
        df = add_allowance_rails(df)
        df = add_slice_df(df,self.period)
        df = add_rails_slice(df)
        return df

    def __call__(self, row, *args, **kwds):
        # if row['stop_short'] > row['high']:
        #     return 
        if row['allowance']:
            if row['stop_short'] > row['open'] > row['short_price']:
                return 'short_pw'
            if row['stop_long'] < row['open'] < row['long_price']:
                return 'long_pw'
        if row['low'] < row['stop_long']:
            return 'close_short_mt'
        if row['high'] > row['stop_short']:
            return 'close_long_mt'
        # if row['stop_short'] > row['high'] > row['short_price']:
        #     return 'short_pw'
        # if row['stop_long'] < row['low'] < row['long_price']:
        #     return 'long_pw'
        

# class OGTA2_Rails(BaseTABitget):
    def preprocessing(self, df):
        df = add_spred(df)
        df['mean_spred'] = df['spred'].mean()
        df = add_OGTA2_rails_info(df)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['info'] == 1:
            return 'long_ct'
        if row['info'] == -1:
            return 'short_ct'
        
class OGTA3_DS(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df):
        df['spread'] = df['high'] - df['low']

        # Вычисление среднего объема и спреда
        df['avg_volume'] = df['volume'].rolling(window=self.period).mean()
        df['avg_spread'] = df['spread'].rolling(window=self.period).mean()

        # Генерация сигналов
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['volume'] > df['avg_volume']) & (df['spread'] < 1 * df['avg_spread']) & (df['close'] > df['open']), 'signal'] = 1  # Покупка
        df.loc[(df['volume'] > df['avg_volume']) & (df['spread'] < 1 * df['avg_spread']) & (df['close'] < df['open']), 'signal'] = -1  # Продажа
        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'
        
def find_rails_pattern(data):
    data['rails_pattern'] = 0  # 0 = нет паттерна, 1 = рельсы вверх, -1 = рельсы вниз
    for i in range(1, len(data)):
        # Первая свеча: сильное движение вверх
        first_candle_up = (data['close'].iloc[i - 1] - data['open'].iloc[i - 1]) > 0
        # Вторая свеча: сильное движение вниз
        second_candle_down = (data['close'].iloc[i] - data['open'].iloc[i]) < 0
        # Свечи примерно одинакового размера
        size_similar = abs((data['close'].iloc[i - 1] - data['open'].iloc[i - 1]) - 
                          (data['close'].iloc[i] - data['open'].iloc[i])) < 0.1
        if first_candle_up and second_candle_down and size_similar:
            data.loc[data.index[i], 'rails_pattern'] = 1  # Рельсы вверх
        # Первая свеча: сильное движение вниз
        first_candle_down = (data['close'].iloc[i - 1] - data['open'].iloc[i - 1]) < 0
        # Вторая свеча: сильное движение вверх
        second_candle_up = (data['close'].iloc[i] - data['open'].iloc[i]) > 0
        if first_candle_down and second_candle_up and size_similar:
            data.loc[data.index[i], 'rails_pattern'] = -1  # Рельсы вниз
    return data

class OGTA3_Rails(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df):
        df = find_rails_pattern(df)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        for i in range(1, len(df)):
            if df['rails_pattern'].iloc[i - 1] == 1:  # Рельсы вверх
                if df['close'].iloc[i] > df['high'].iloc[i - 1]:  # Пробой максимума
                    df.loc[df.index[i], 'signal'] = 1  # Покупка
            elif df['rails_pattern'].iloc[i - 1] == -1:  # Рельсы вниз
                if df['close'].iloc[i] < df['low'].iloc[i - 1]:  # Пробой минимума
                    df.loc[df.index[i], 'signal'] = -1  # Продажа

        df = add_enter_price(df,lambda row: get_universal_r(row,'close','close'))
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == -1:
            return 'short_pw'