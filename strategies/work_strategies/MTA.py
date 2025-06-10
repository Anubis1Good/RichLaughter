import os
import json
from datetime import datetime
import numpy as np
import pandas as pd
from strategies.work_strategies.BaseTA import BaseTABitget
from strategies.test_strategies.check import check_strategy_fast
from strategies.test_strategies.universal import universal_test_strategy_fast as TS
from ForBots.Indicators.classic_indicators import add_enter_price2close
from Screening.utils.keys_strategies import allDC


class MTA_SKYNET(BaseTABitget):
    """
    period=100,pick_file:str='1_1_test_MOEX_FUT' \n
    Анализирует по шагам с историей, как otBot
    """

    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,pick_file:str='1_1_test_MOEX_FUT',need_log=True,alias=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.pick_file = os.path.join('Screening/strat_picks',pick_file+'.json')
        self.tas = (BaseTABitget,(self.period,))
        self.strategy = self.tas[0](self.symbol,self.granularity,self.productType,1,*self.tas[1])
        key_name_dc = "_".join(pick_file.split('_')[-2:])
        self.dc = allDC[key_name_dc]
        self.need_log = need_log
        if self.need_log:
            folder = 'logs/work_logs/'
            filename = f'{self.symbol}_{self.granularity}_MTA_SKYNET_{pick_file}.txt' 
            if not os.path.exists(folder):
                os.makedirs(folder)
            self.filename = os.path.join(folder,filename)
        self.name_bot = 'Base'
        self.need_change = False
        if alias:
            self.work_symbol = alias
        else:
            self.work_symbol = self.symbol

    def write_log(self):
        with open(self.filename,mode='a+') as f:
            log = f'{datetime.now()} : {self.name_bot}\n'
            f.write(log)
            f.seek(0)  # Перемещаем указатель в начало файла
            lines = f.readlines()
        if len(lines) > 500:
            lines = lines[-200:]
            with open(self.filename,'w') as f:
                f.writelines(lines)

    def choice_ws(self):
        if os.path.exists(self.pick_file):
            with open(self.pick_file) as f:
                ks = json.load(f)
                if self.work_symbol in ks:
                    name_bot = ks[self.work_symbol]
                    self.need_change = name_bot != self.name_bot
                    if self.need_change:
                        self.name_bot = name_bot
                        if self.need_log:
                            self.write_log()
                    else:
                        return
                    if name_bot in self.dc:
                        self.tas = self.dc[name_bot]
                        return
        self.tas = (BaseTABitget,(self.period,))

    def preprocessing(self, df):
        self.choice_ws()
        if self.need_change:
            self.strategy = self.tas[0](self.work_symbol,self.granularity,self.productType,1,*self.tas[1])
            self.need_change = False
        df = self.strategy.preprocessing(df)
        return df

    def __call__(self, row, *args, **kwds):
        return self.strategy.__call__(row)


class MTA_LORD(BaseTABitget):
    '''
    period=100,wss=((BaseTABitget,(11,)),),fee=0.0002,lenth_history=3,need_log=True
    Анализирует на истории, как WorkBitget
    '''
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,wss=((BaseTABitget,(11,)),),fee=0.0002,lenth_history=3,need_log=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fee = fee
        self.tas = {}
        self.prepare_bots(wss)
        self.period = (max(list(map(lambda x: x[1][0],wss)))+1)*lenth_history
        self.cur_strategy = ''
        self.need_log = need_log
        if self.need_log:
            folder = 'logs/work_logs/'
            if not os.path.exists(folder):
                os.makedirs(folder)
            filename = f'{self.symbol}_{self.granularity}_MTA_LORD.txt' 
            self.filename = os.path.join(folder,filename)

    def prepare_bots(self,wss):
        for WS,conf in wss:
            strategy = WS(self.symbol,self.granularity,self.productType,1,*conf)
            name = self.symbol + '_' + str(self.granularity) + '_' + str(strategy).split(' ')[0].split('.')[-1] + "_" + "_".join(list(map(str,conf)))
            self.tas[name] = strategy

    def write_log(self):
        with open(self.filename,mode='a+') as f:
            log = f'{datetime.now()} : {self.cur_strategy}\n'
            f.write(log)
            f.seek(0)  # Перемещаем указатель в начало файла
            lines = f.readlines()
        if len(lines) > 500:
            lines = lines[-200:]
            with open(self.filename,'w') as f:
                f.writelines(lines)

    def preprocessing(self, df:pd.DataFrame):
        if len(df.index) > self.period:
            df = df.iloc[-self.period:]
        df = df.copy()
        results = {}
        for i,ta in self.tas.items():
            df_c = df.copy()
            df_c = ta.get_test_df(df_c)
            trades = check_strategy_fast(df_c,TS,ta)
            if trades['count'] > 0 and trades['total'] > 0:
                trades['total'] -= trades['count'] * (trades['open_price'] * self.fee)
                results[i] = (trades['total'],trades['signal'])

        df['signal'] = ''
        if results:
            results = dict(sorted(results.items(), key=lambda item: item[1][0], reverse=True))
            signal = tuple(results.values())[0][1]
            if self.need_log:
                cur_strategy = tuple(results.keys())[0]
                if self.cur_strategy != cur_strategy:
                    self.cur_strategy = cur_strategy
                    self.write_log()
            df['signal'] = signal

        df = add_enter_price2close(df)
        return df

    def __call__(self, row, *args, **kwds):
        return row['signal']
    
class MTA_LORD2(BaseTABitget):
    '''
    period=100,fee=0.0002,wss=((BaseTABitget,(11,)),),need_log=True
    Анализирует на истории, как WorkBitget
    '''
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,fee=0.0002,wss=((BaseTABitget,(11,)),),need_log=True):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fee = fee
        self.tas = {}
        self.prepare_bots(wss)
        self.cur_strategy = ''
        self.need_log = need_log
        if self.need_log:
            folder = 'logs/work_logs/'
            if not os.path.exists(folder):
                os.makedirs(folder)
            filename = f'{self.symbol}_{self.granularity}_MTA_LORD2.txt' 
            self.filename = os.path.join(folder,filename)

    def prepare_bots(self,wss):
        for WS,conf in wss:
            strategy = WS(self.symbol,self.granularity,self.productType,1,*conf)
            name = self.symbol + '_' + str(self.granularity) + '_' + str(strategy).split(' ')[0].split('.')[-1] + "_" + "_".join(list(map(str,conf)))
            self.tas[name] = strategy

    def write_log(self):
        with open(self.filename,mode='a+') as f:
            log = f'{datetime.now()} : {self.cur_strategy}\n'
            f.write(log)
            f.seek(0)  # Перемещаем указатель в начало файла
            lines = f.readlines()
        if len(lines) > 500:
            lines = lines[-200:]
            with open(self.filename,'w') as f:
                f.writelines(lines)

    def preprocessing(self, df:pd.DataFrame):
        if len(df.index) > self.period:
            df = df.iloc[-self.period:]
        df = df.copy()
        results = {}
        for i,ta in self.tas.items():
            df_c = df.copy()
            df_c = ta.get_test_df(df_c)
            trades = check_strategy_fast(df_c,TS,ta)
            if trades['count'] > 0 and trades['total'] > 0:
                trades['total'] -= trades['count'] * (trades['open_price'] * self.fee)
                results[i] = (trades['total'],trades['signal'])

        df['signal'] = ''
        if results:
            results = dict(sorted(results.items(), key=lambda item: item[1][0], reverse=True))
            signal = tuple(results.values())[0][1]
            if self.need_log:
                cur_strategy = tuple(results.keys())[0]
                if self.cur_strategy != cur_strategy:
                    self.cur_strategy = cur_strategy
                    self.write_log()
            df['signal'] = signal

        df = add_enter_price2close(df)
        return df

    def __call__(self, row, *args, **kwds):
        return row['signal']
    