import os
from datetime import datetime
import numpy as np
import pandas as pd
from multiprocessing import Pool
from strategies.work_strategies.BaseTA import BaseTABitget
from strategies.work_strategies.LTA import LTA_PIN
from strategies.work_strategies.PTA import PTA4_WDDCr

from strategies.test_strategies.check import check_strategy_fast
from strategies.test_strategies.universal import universal_test_strategy_fast as TS

from ForBots.Indicators.classic_indicators import add_enter_price2close, add_slice_df
PHYSICAL_CORES = os.cpu_count() // 2

class MTA_SKYNET(BaseTABitget):
    '''
    Анализирует по шагам с историей, как otBot
    '''
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,wss=((PTA4_WDDCr,(11,30)),),fut=False):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fut = fut
        self.start_ta = wss[0]
        self.tas = wss
        self.filename = f'{self.symbol}_{self.granularity}_MTA_SKYNET.txt' 

    def prepare_bots(self,folder,wss):
        for WS,conf in wss:
            strategy = WS(self.symbol,self.granularity,self.productType,1,*conf)
        #     bot = TestMarketBot1(folder,ticker,strategy,conf)
        #     bots[ticker].append(bot)
        # return bots
    def preprocessing(self, df):
        # df = add_cci(df,self.period)
        # df = add_enter_price2close(df)  
        # df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        pass
        # if row['cci'] < -200+self.threshold:  
        #     return 'long_pw'
        # if row['cci'] > 200-self.threshold:  
        #     return 'short_pw'

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
    
# class MTA_MAJESTY(BaseTABitget):
#     '''
#     period=100,wss=((BaseTABitget,(11,)),),fee=0.0002,lenth_history=3,need_log=True
#     Анализирует на истории, как WorkBitget
#     '''
#     def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,wss=((BaseTABitget,(11,)),),fee=0.0002,lenth_history=3,need_log=True):
#         super().__init__(symbol, granularity, productType, n_parts, period)
#         self.fee = fee
#         self.tas = {}
#         self.prepare_bots(wss)
#         self.period = (max(list(map(lambda x: x[1][0],wss)))+1)*lenth_history
#         self.cur_strategy = ''
#         self.need_log = need_log
#         if self.need_log:
#             folder = 'logs/work_logs/'
#             if not os.path.exists(folder):
#                 os.makedirs(folder)
#             filename = f'{self.symbol}_{self.granularity}_MTA_LORD.txt' 
#             self.filename = os.path.join(folder,filename)

#     def prepare_bots(self,wss):
#         for WS,conf in wss:
#             strategy = WS(self.symbol,self.granularity,self.productType,1,*conf)
#             name = self.symbol + '_' + str(self.granularity) + '_' + str(strategy).split(' ')[0].split('.')[-1] + "_" + "_".join(list(map(str,conf)))
#             self.tas[name] = strategy

#     def write_log(self):
#         with open(self.filename,mode='a+') as f:
#             log = f'{datetime.now()} : {self.cur_strategy}\n'
#             f.write(log)
#             f.seek(0)  # Перемещаем указатель в начало файла
#             lines = f.readlines()
#         if len(lines) > 500:
#             lines = lines[-200:]
#             with open(self.filename,'w') as f:
#                 f.writelines(lines)

#     def process_ta(self,args):
#         i, ta, df, TS, fee = args
#         df_c = df.copy()
#         df_c = ta.get_test_df(df_c)
#         trades = check_strategy_fast(df_c, TS, ta)
#         if trades['count'] > 0 and trades['total'] > 0:
#             trades['total'] -= trades['count'] * (trades['open_price'] * fee)
#             return (i, (trades['total'], trades['signal']))
#         return None
    
#     def multiprocessing_tas(self, df, TS):
#         results = {}
#         # Подготовка аргументов для каждого процесса
#         args_list = [(i, ta, df, TS, self.fee) for i, ta in self.tas.items()]
        
#         # Создание пула процессов и обработка
#         with Pool(processes=PHYSICAL_CORES) as pool:
#             processed_results = pool.map(self.process_ta, args_list)
        
#         # Сбор результатов
#         for result in processed_results:
#             if result is not None:
#                 i, res = result
#                 results[i] = res
#         return results
#     def preprocessing(self, df:pd.DataFrame):
#         if len(df.index) > self.period:
#             df = df.iloc[-self.period:]
#         df = df.copy()
#         results = self.multiprocessing_tas(df,TS)
#         df['signal'] = ''
#         if results:
#             results = dict(sorted(results.items(), key=lambda item: item[1][0], reverse=True))
#             signal = tuple(results.values())[0][1]
#             if self.need_log:
#                 cur_strategy = tuple(results.keys())[0]
#                 if self.cur_strategy != cur_strategy:
#                     self.cur_strategy = cur_strategy
#                     self.write_log()
#             df['signal'] = signal

#         df = add_enter_price2close(df)
#         return df

#     def __call__(self, row, *args, **kwds):
#         return row['signal']


class MTA_VLAD(BaseTABitget):
    '''
    Бот, который берет стратегию из файла в сети, который изменяется оператором-человеком
    '''
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=100,wss=((PTA4_WDDCr,(11,30)),),fut=False):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.fut = fut
        self.start_ta = wss[0]
        self.tas = wss

    def prepare_bots(self,folder,wss):
        for WS,conf in wss:
            strategy = WS(self.symbol,self.granularity,self.productType,1,*conf)
        #     bot = TestMarketBot1(folder,ticker,strategy,conf)
        #     bots[ticker].append(bot)
        # return bots
    def preprocessing(self, df):
        # df = add_cci(df,self.period)
        # df = add_enter_price2close(df)  
        # df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        pass
        # if row['cci'] < -200+self.threshold:  
        #     return 'long_pw'
        # if row['cci'] > 200-self.threshold:  
        #     return 'short_pw'