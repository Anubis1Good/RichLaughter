from utils.help_trades import reverse_action
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.vsa_indicators import add_rails,add_rails_slice
from ForBots.Indicators.classic_indicators import add_big_volume,add_slice_df,add_enter_price
from ForBots.Indicators.price_funcs import get_price_reverse_rails

class OGTA1_Rails(BaseTABitget):
    def preprocessing(self, df):
        df = add_big_volume(df,self.period)
        df = add_rails(df)
        df = add_enter_price(df,get_price_reverse_rails)
        df = add_slice_df(df,self.period)
        df = add_rails_slice(df)
        return df

    def __call__(self, row, *args, **kwds):
        if row['stop_short'] > row['high'] > row['short_price']:
            return 'short_r'
        if row['stop_long'] < row['low'] < row['long_price']:
            return 'long_r'
        