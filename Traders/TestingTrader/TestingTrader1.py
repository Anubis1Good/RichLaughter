import os
import sys
from datetime import date, timedelta,datetime
from time import sleep,time
from collections import defaultdict
from Bots.TestBot3 import TestBot3
from request_functions.download_bitget import get_df
from request_functions.download_moex import download_moex,create_df
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5

class TestingTrader1:
    def __init__(self,exchange:str,spec:str,db_path:str,tickers:tuple[tuple],wss_map:dict[list]):
        self.exchange = exchange
        self.spec = spec
        self.tickers = tickers
        self.wss_map = wss_map
        self.db_path = db_path
        self.fee = 0
        folder_output = 'logs/test_trader_logs'
        if not os.path.exists(folder_output):
            os.makedirs(folder_output)
        self.filename = os.path.join(folder_output,exchange + '_' + spec + '.txt')
        self.init_ex_spec()
        self.map_bots = defaultdict(lambda :defaultdict(list))
        self.prepare_bots_outer()
        self.yesterday = str(date.today() - timedelta(days=3))
        self.check_time = False
        self.check_time2 = False
        self.count_bars = 300
        self.start_info()

    def start_info(self):
        self.output('-----------------------')
        self.output('Count_req_bars:',self.count_bars)
        self.output('Check_time:',self.check_time)
        self.output('Check_time2:',self.check_time2)
        len_tick = len(self.tickers)
        self.output('Len_tickers:',len_tick)
        for mb in self.map_bots:
            i = len(list(self.map_bots[mb].values())[0])
            self.output('Len_bots',mb,i)
            self.output('All_bots',mb,i*len_tick)
        
    def trade_base(self,func):
        pass

    def trade_bots_moex(self,func):
        for ticker,fut in self.tickers:
            df = download_moex(ticker,1,self.yesterday,board=self.board,market=self.market,engine=self.engine)
            df = create_df(df)
            for bot in self.map_bots[1][ticker]:
                # print(bot)
                df_c = df.copy()
                if self.check_time:
                    start2 = time()
                func(bot,df_c)
                if self.check_time:
                    self.output(time()-start2,bot)
            df = convert_chart1to5(df)
            for bot in self.map_bots[5][ticker]:
                df_c = df.copy()
                func(bot,df_c)

    def trade_bots_bitget(self,func):
        for ticker,fut in self.tickers:
            for granularity in self.wss_map:
                df = get_df(ticker,granularity,"usdt-futures",self.count_bars)
                for bot in self.map_bots[granularity][ticker]:
                    df_c = df.copy()
                    func(bot,df_c)
    
    def output(self,*text):
        f = open(self.filename, "a", encoding="utf-8")
        t = str(datetime.now()) + ' '.join(list(map(str,text))) + '\n'
        f.write(t)
        f.close()
    
    def init_ex_spec(self):
        if self.exchange == 'MOEX':
            if self.spec == 'FUT':
                self.fee = 0.00001
                self.board = "RFUD"
                self.market = "forts"
                self.engine= "futures"
            else:
                self.fee = 0.0002
                self.board = "TQBR"
                self.market: str = "shares"
                self.engine: str = "stock"
            self.trade_base = self.trade_bots_moex
        if self.exchange == 'Bitget':
            self.fee = 0.0004
            self.trade_base = self.trade_bots_bitget
        
    
    def prepare_bots_inner(self,wss,granularity,bots):
        for ticker,fut in self.tickers:
            for WS,conf in wss:
                strategy = WS(ticker,granularity,fut,1,*conf)
                bot = TestBot3(self.db_path,self.fee,ticker,granularity,strategy,conf)
                bots[ticker].append(bot)
        return bots
    
    def prepare_bots_outer(self):
        for granularity in self.wss_map:
            self.prepare_bots_inner(self.wss_map[granularity],granularity,self.map_bots[granularity])
        
    def run(self):
        while True:
            if self.check_time2:
                start = time()
            try:
                self.trade_base(lambda bot,df:bot.run(df))

            except KeyboardInterrupt:
                self.close_all_pos()
                break
            except:
                self.output('Ошибка')
            if self.check_time2:
                self.output('Time:',time()-start)

    def close_all_pos(self):
        self.output('Close all position...')
        self.trade_base(lambda bot,df:bot.cancel_trade(df))
        self.output('Position closed!')