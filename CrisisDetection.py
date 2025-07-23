import pandas as pd
import os
import traceback
from time import sleep
from datetime import date,timedelta
from Loader.BitgetLoader import bitget_loader
from request_functions.download_bitget import get_df
from request_functions.download_moex import download_moex,create_df
from Screening.robots.CrisisDetection.groups_CD import tickersMoexStockCD
from strategies.work_strategies.LTA import LTA_CC

today = date.today()
interval = 60
mult_days = 1 if interval <= 10 else 5
if today.weekday() == 0:
    delta = timedelta(days=4*mult_days)
else:
    delta = timedelta(days=2*mult_days)
yesterday = yesterday = str(today - delta)
bot = LTA_CC('MMVB',interval,'stock',1,96,10,2,7,2,2,0,0)
res = {}
while True:
    for ticker,fut in tickersMoexStockCD:
        try:
            if fut:
                board = "RFUD"
                market = "forts"
                engine= "futures"
            else:
                board = "TQBR"
                market: str = "shares"
                engine: str = "stock"
            df = download_moex(ticker,10,yesterday,board=board,market=market,engine=engine)
            df = create_df(df)
            if len(df.index) > 400:
                df = df.iloc[-400:]
            df = bot.preprocessing(df)
            res[ticker] = {}
            res[ticker]['10m'] = df.iloc[-1]['overbought'] - df.iloc[-1]['oversold']
            df = download_moex(ticker,60,yesterday,board=board,market=market,engine=engine)
            df = create_df(df)
            if len(df.index) > 400:
                df = df.iloc[-400:]
            df = bot.preprocessing(df)
            res[ticker]['60m'] = df.iloc[-1]['overbought'] - df.iloc[-1]['oversold']

        except Exception:
            print(traceback.print_exc())
    # res_df = pd.Series(res)
    res_df = pd.DataFrame(res).T
    res_df = res_df.sort_values('60m',axis=0)
    os.system('cls')
    print('-----------long recomendation-----------')
    print(res_df.head(10))
    print('-----------short recomendation-----------')
    print(res_df.tail(10))
    sleep(60*5)
