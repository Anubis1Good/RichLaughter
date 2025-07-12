import numpy as np
import  matplotlib.pyplot as plt
import pandas as pd
import os
import json
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_ema,add_enter_price2close,add_rsi,add_chop,add_rsi_tw,add_cci,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_adx,add_donchan_channel,add_sma,add_bollinger,add_vodka_channel,add_buffer_add
from ForBots.Indicators.pva_indicators import add_velcro_indicator,add_pc_stair_fast,add_static_channel

def get_action(action):
    if action == 1:
        return 'long_pw'
    if action == -1:
        return 'short_pw'
    return 'close_all_pw'

def get_action6(action):
    actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
    return actions[action]
def get_action5(action):
    actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw')
    return actions[action]

class GLTA_ALPHA(BaseTABitget):
    """period=20,policy=None"""
    flags = [
            'C_sma',
            'C_sma2',
            'sma_sma2'
        ]
    n_features = len(flags)
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period2=10,policy:str|dict|None=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        if policy:
            if isinstance(policy,str):
                try:
                    with open(os.path.join('modelML/Policies',policy)) as f:
                        self.policy = json.load(f)
                except:
                    print('err')
                    self.policy = None
            if isinstance(policy,dict):
                self.policy = policy
        else:
            self.policy = None

    def preprocessing(self, df):
        df = add_sma(df,self.period)
        df['sma2'] = df['close'].rolling(self.period2).mean()
        df['C_sma'] = df['close'] > df['sma']
        df['C_sma2'] = df['close'] > df['sma2']
        df['sma_sma2'] = df['sma'] > df['sma2']
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        s = row.loc[self.flags].to_numpy()
        if self.policy:
            S = self.policy['S']
            A = self.policy['A']
            try:
                index_state = np.where((S == s).all(axis=1))[0][0]
                a = get_action(A[index_state])
                # print(a)
                return a
            except:
                return None
            
class GLTA_BETA(BaseTABitget):
    """period=20,period2=10,threshold=30,policy:str|dict|None=None"""
    flags = [
        'C_sma',
        'C_sma2',
        'sma_sma2',
        'H_bbu',
        'L_bbd',
        'rsi_UT',
        'rsi_DT'
    ]
    n_features = len(flags)
    
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period2=10,threshold=30,policy:str|dict|None=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.threshold = threshold
        if policy:
            if isinstance(policy,str):
                try:
                    with open(os.path.join('modelML/Policies',policy)) as f:
                        self.policy = json.load(f)
                except:
                    print('err')
                    self.policy = None
            if isinstance(policy,dict):
                self.policy = policy
        else:
            self.policy = None

    def preprocessing(self, df):
        df = add_bollinger(df,self.period)
        df = add_rsi(df,self.period2)
        df['sma2'] = df['close'].rolling(self.period2).mean()
        df['C_sma'] = df['close'] > df['sma']
        df['C_sma2'] = df['close'] > df['sma2']
        df['sma_sma2'] = df['sma'] > df['sma2']
        df['H_bbu'] = df['high'] >= df['bbu']
        df['L_bbd'] = df['low'] <= df['bbd']
        df['rsi_UT'] = df['rsi'] > 100-self.threshold
        df['rsi_DT'] = df['rsi'] < self.threshold
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        s = row.loc[self.flags].to_numpy()
        if self.policy:
            S = self.policy['S']
            A = self.policy['A']
            try:
                index_state = np.where((S == s).all(axis=1))[0][0]
                a = get_action(A[index_state])
                # print(a)
                return a
            except:
                return None

class GLTA_GAMMA(BaseTABitget):
    """period=20,period2=100,threshold=30,period3=60,threshold_adx=30,threshold_chop=50,policy"""
    flags = [
        'C_avarege',
        'avarege_sma2',
        'H_top',
        'L_bottom',
        'rsi_UT',
        'rsi_DT',
        'adx_T',
        'adx_sma',
        'chop_T',
        'chop_sma' 
    ]
    n_features = len(flags)
    
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,period2=100,threshold=30,period3=60,threshold_adx=30,threshold_chop=50,policy:str|dict|None=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.threshold_adx = threshold_adx
        self.threshold_chop = threshold_chop
        self.threshold = threshold
        if policy:
            if isinstance(policy,str):
                try:
                    with open(os.path.join('modelML/Policies',policy)) as f:
                        self.policy = json.load(f)
                except:
                    print('err')
                    self.policy = None
            if isinstance(policy,dict):
                self.policy = policy
        else:
            self.policy = None

    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_adx(df,self.period3)
        df = add_chop(df,self.period3)
        df['sma2'] = df['close'].rolling(self.period2).mean()
        df['sma_adx'] = df['adx'].rolling(self.period).mean()
        df['sma_chop'] = df['chop'].rolling(self.period).mean()

        df['C_avarege'] = df['close'] > df['avarege']
        df['avarege_sma2'] = df['avarege'] > df['sma2']
        df['H_top'] = df['high'] >= df['max_hb']
        df['L_bottom'] = df['low'] <= df['min_hb']
        df['rsi_UT'] = df['rsi'] > 100-self.threshold
        df['rsi_DT'] = df['rsi'] < self.threshold
        df['adx_T'] = df['adx'] > self.threshold_adx
        df['adx_sma'] = df['adx'] > df['sma_adx']
        df['chop_T'] = df['chop'] > self.threshold_chop
        df['chop_sma'] = df['chop'] > df['sma_chop']

        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        s = row.loc[self.flags].to_numpy()
        if self.policy:
            S = self.policy['S']
            A = self.policy['A']
            try:
                index_state = np.where((S == s).all(axis=1))[0][0]
                a = get_action(A[index_state])
                return a
            except:
                return None
    

class GLTA2_BETA(GLTA_BETA):
    def __call__(self, row, *args, **kwds):
        s = row.loc[self.flags].to_numpy()
        if self.policy:
            S = self.policy['S']
            A = self.policy['A']
            try:
                index_state = np.where((S == s).all(axis=1))[0][0]
                a = get_action5(A[index_state])
                # print(a)
                return a
            except:
                return None
            
class GLTA2_GAMMA(GLTA_GAMMA):
    def __call__(self, row, *args, **kwds):
        s = row.loc[self.flags].to_numpy()
        if self.policy:
            S = self.policy['S']
            A = self.policy['A']
            try:
                index_state = np.where((S == s).all(axis=1))[0][0]
                a = get_action5(A[index_state])
                # print(a)
                return a
            except:
                return None