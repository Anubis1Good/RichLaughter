from utils.help_trades import reverse_action
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.vsa_indicators import add_rails,add_rails_slice,add_allowance_rails
from ForBots.Indicators.classic_indicators import add_big_volume,add_slice_df,add_enter_price,add_delta_2v,add_sc_and_buffer
from ForBots.Indicators.price_funcs import get_price_reverse_rails

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
        