import os
import json
from datetime import datetime
import numpy as np
import pandas as pd
from strategies.work_strategies.BaseTA import BaseTABitget
from strategies.test_strategies.universal import universal_test_strategy_fast as TS
from startKing import allDC,prepare_tickers,tickersExchange,exchages

class MTA_KING(BaseTABitget):
    """
    period=100,pick_file:str='1_1_test_MOEX_FUT',mode='' \n
    Управляемый Skynet
    """

    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,pick_file:str='1_1_test_MOEX_FUT',mode='',alias=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.pick_file = os.path.join('Screening/strat_picks',mode+pick_file+'.json')
        self.mode = mode
        self.tas = (BaseTABitget,(self.period,))
        self.tas_king = (BaseTABitget,(self.period,))
        self.strategy_king = self.tas_king[0](self.symbol,self.granularity,self.productType,1,*self.tas_king[1])
        index_ex = exchages.index("_".join(pick_file.split('_')[-2:]))
        self.dc_king = allDC[index_ex]
        need_log = True
        if need_log:
            folder = 'logs/work_logs_king/'
            filename = f'{self.symbol}_{self.granularity}_MTA_KING_{pick_file}.txt' 
            if not os.path.exists(folder):
                os.makedirs(folder)
            self.filename = os.path.join(folder,filename)
        if not symbol in prepare_tickers(tickersExchange[index_ex]):
            self.symbol = 'Other'
        self.name_bot_king = 'Base'
        self.need_change = False
        if alias:
            self.work_symbol = alias
        else:
            self.work_symbol = self.symbol

    def write_log(self):
        with open(self.filename,mode='a+') as f:
            log = f'{datetime.now()} : {self.name_bot_king}\n'
            f.write(log)
            f.seek(0)  # Перемещаем указатель в начало файла
            lines = f.readlines()
        if len(lines) > 500:
            lines = lines[-200:]
            with open(self.filename,'w') as f:
                f.writelines(lines)

    def choice_ws_king(self):
        if os.path.exists(self.pick_file):
            with open(self.pick_file) as f:
                ks = json.load(f)
                if self.work_symbol in ks:
                    name_bot = ks[self.work_symbol]
                    self.need_change = name_bot != self.name_bot_king
                    if self.need_change:
                        self.name_bot_king = name_bot
                        self.write_log()
                    else:
                        return
                    if name_bot in self.dc_king:
                        self.tas_king = self.dc_king[name_bot]
                        return
        self.tas_king = (BaseTABitget,(self.period,))

    def preprocessing(self, df):
        self.choice_ws_king()
        if self.need_change:
            if 'SKYNET' in self.name_bot_king:
                param = list(self.tas_king[1])
                param[1] = self.mode + param[1]
                param.append(False)
            else:
                param = self.tas_king[1]
            self.strategy_king = self.tas_king[0](self.work_symbol,self.granularity,self.productType,1,*param)
            self.need_change = False
        df = self.strategy_king.preprocessing(df)
        return df

    def __call__(self, row, *args, **kwds):
        return self.strategy_king.__call__(row)