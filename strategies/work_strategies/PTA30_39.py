import pandas as pd
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close, add_adx, add_chop, add_macd
from strategies.work_strategies.BaseTA import BaseTABitget

class PTA30_(BaseTABitget):
    """period=30,period_chop=30,shw=15,lw=30,siw=10,thr_adx=25,thr_chop=40,work_trend=True,large_open='12',large_close='12',n_large='2'"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=14,period_chop=14,shw=12,lw=26,siw=9,thr_adx=25,thr_chop=40,work_trend=True,large_open='12',large_close='12',n_large='2'):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period_chop = period_chop
        self.shw = shw
        self.lw = lw
        self.siw = siw
        self.thr_adx = thr_adx
        self.thr_chop = thr_chop
        self.work_trend = work_trend
        self.large_open = large_open
        self.large_close = large_close
        self.n_large = n_large
    def preprocessing(self,df):
        df = add_adx(df,self.period)
        df = add_chop(df,self.period_chop)
        df = add_macd(df,self.shw,self.lw,self.siw)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    
    def __call__(self,row, *args, **kwds):
        # range
        pos = args[0]
        print(self.symbol)
        if row['adx'] > self.thr_adx and row['chop'] < self.thr_chop:
            print('range')
            if pos == 0:
                return 'all_large'+self.large_open+'_'+self.n_large
            else:
                return 'all_large'+self.large_close+'_'+self.n_large
        # trend
        else:
            if self.work_trend:
                # long
                print('long')
                if row['macd'] > row['signal_line']:
                    if pos == 1:
                        return 'spred_long_large'+self.large_close +'_'+self.n_large
                    else:
                        return 'spred_long_large'+self.large_open +'_'+self.n_large
                # short
                else:
                    print('short')
                    if pos == -1:
                        return 'spred_short_large'+self.large_close +'_'+self.n_large
                    else:
                        return 'spred_short_large'+self.large_open +'_'+self.n_large
