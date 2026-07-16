import pandas as pd
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close, add_adx, add_chop, add_macd
from strategies.work_strategies.BaseTA import BaseTABitget

class PTA30_LILI(BaseTABitget):
    """period=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40,work_trend=True,large_open='12',large_close='12',n_large='2'"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40,work_trend=True,large_open='12',large_close='12',n_large='2'):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period_chop = period_chop
        self.period_sma_l = period_sma_l
        self.period_sma_s = period_sma_s
        self.thr_adx = thr_adx
        self.thr_chop = thr_chop
        self.work_trend = work_trend
        self.large_open = large_open
        self.large_close = large_close
        self.n_large = n_large
        self.large_config = 'large_o'+large_open+'_c'+large_close+'_'+n_large
    def preprocessing(self,df):
        df = add_adx(df,self.period)
        df = add_chop(df,self.period_chop)
        df['sma_s'] = df['close'].rolling(self.period_sma_s).mean()
        df['sma_l'] = df['close'].rolling(self.period_sma_l).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    
    def __call__(self,row, *args, **kwds):
        # range
        # pos = args[0]
        # print(self.symbol)
        if row['adx'] < self.thr_adx and row['chop'] > self.thr_chop:
            # print('range')
            return 'all_'+self.large_config
        # trend
        else:
            if self.work_trend:
                # long
                if row['sma_s'] > row['sma_l']:
                    # print('long')
                    return 'spred_long_'+self.large_config
                # short
                else:
                    # print('short')
                    return 'spred_short_'+self.large_config
            else:
                return 'close_all_pw'
            
class PTA30_RAYNOR(BaseTABitget):
    """period=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40,work_trend=True,large_open='12',large_close='12',n_large='2',min_profit=None,max_loss=None"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40,work_trend=True,large_open='12',large_close='12',n_large='2',min_profit=None,max_loss=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period_chop = period_chop
        self.period_sma_l = period_sma_l
        self.period_sma_s = period_sma_s
        self.thr_adx = thr_adx
        self.thr_chop = thr_chop
        self.work_trend = work_trend
        self.large_open = large_open
        self.large_close = large_close
        self.n_large = n_large
        self.large_config = 'large_o'+large_open+'_c'+large_close+'_'+n_large
        self.VT_need = ('pos','ybests','profit','loss','price_step')
        self.min_profit = min_profit
        self.max_loss = max_loss
    def preprocessing(self,df):
        df = add_adx(df,self.period)
        df = add_chop(df,self.period_chop)
        df['sma_s'] = df['close'].rolling(self.period_sma_s).mean()
        df['sma_l'] = df['close'].rolling(self.period_sma_l).mean()
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    
    def check_close(self,params):
        ps = params['price_step']
        if params['pos'] != 0:
            p_points,l_points = 0, 0
            if params['pos'] == 1:
                if params['p_max'] != -1:
                    delta1 = params['p_max'] - params['p_min']
                    delta2 = params['p_max'] - params['y_bask']
                    p_points = max(delta1,delta2)/ ps
                if params['l_max'] != -1:
                    delta1 = params['l_max'] - params['l_min']
                    delta2 = params['l_max'] - params['y_bask']
                    l_points = max(delta1,delta2)/ ps
            elif params['pos'] == -1:
                if params['p_max'] != -1:
                    delta1 = params['p_max'] - params['p_min']
                    delta2 = params['p_max'] - params['y_bbid']
                    p_points = max(delta1,delta2)/ ps
                if params['l_max'] != -1:
                    delta1 = params['l_max'] - params['l_min']
                    delta2 = params['l_max'] - params['y_bbid']
                    l_points = max(delta1,delta2)/ ps
            if self.min_profit is not None:
                # print(self.symbol,p_points)
                if p_points >= self.min_profit:
                    return 'close_all_pw'
            if self.max_loss is not None:
                # print(self.symbol,l_points)
                if l_points >= self.max_loss:
                    return 'close_all_pw'
        return None

    def __call__(self,row, *args, **kwds):
        params = args[0]
        need_close = self.check_close(params)
        if need_close is not None:
            return need_close
        # range
        if row['adx'] < self.thr_adx and row['chop'] > self.thr_chop:
            # print('range')
            return 'all_'+self.large_config
        # trend
        else:
            if self.work_trend:
                # long
                if row['sma_s'] > row['sma_l']:
                    # print('long')
                    return 'spred_long_'+self.large_config
                # short
                else:
                    # print('short')
                    return 'spred_short_'+self.large_config
            else:
                return 'close_all_pw'
