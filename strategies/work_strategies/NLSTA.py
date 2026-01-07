import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Optional, Union
import json
import os
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_ema,add_enter_price2close,add_rsi,add_chop,add_rsi_tw,add_cci,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_adx,add_donchan_channel,add_sma,add_bollinger,add_vodka_channel,add_buffer_add
from Optimiztion.models_nn.linear_models import NLSNN1
from Optimiztion.models_nn.utils import load_neural_weights
from ForBots.help_func.help_nlsta1 import nlsta1_settings

def get_action5(action):
    actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw')
    return actions[action]



class NLSTA1_UNION(BaseTABitget):
    """period=20,name_settings:str='first_test',policy_model:str|nn.Module|None=None,cparams:dict={}"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,name_settings:str='first_test',policy_model:str|nn.Module|None=None,cparams:dict={}):
        super().__init__(symbol, granularity, productType, n_parts, period)
        settings = nlsta1_settings.get(name_settings,nlsta1_settings['default']).copy()
        self.flags = settings['flags'].copy()
        self.func = settings['func']
        self.params = settings['need_params'].copy()
        self.params.update(cparams)
        self.n_features = len(self.flags)
        if policy_model:
            if isinstance(policy_model,str):
                self.policy_model,_ = load_neural_weights(policy_model,NLSNN1)
            else:
                self.policy_model = policy_model
        else:
            self.polipolicy_model = None

    def preprocessing(self, df):
        df = self.func(df,self.params)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if self.policy_model is None:
            return None
        try:
            s = row.loc[self.flags].to_numpy(dtype=np.float32)
            s = torch.tensor(s, dtype=torch.float32)
            action_idx, _ = self.policy_model.predict_action(s)
            a = get_action5(action_idx)
            # print(a,action_idx)
            return a
        except:
            return None