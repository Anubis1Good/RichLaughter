import sys
from time import sleep,time
from datetime import date, timedelta
from collections import defaultdict
from Bots.TestBot1 import TestMarketBot1
from request_functions.download_moex import download_moex,create_df
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
from strategies.work_strategies.PTA import PTA2_DDCde,PTA2_LISICA,PTA8_LOBSTER,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA8_OBBY_FREEr,PTA9_RAB,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA10_MAGIC,PTA6_KAMA,PTA6_KAMA2,PTA6_KAMAZ2
# from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
# from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_APHOBO,LTA_BORSCH,LTA_KROSH,LTA_OKROSHKA
from strategies.work_strategies.OGTA import OGTA4_DOG

# bots1 = []
# bots5 = []
# bots15 = []
# bots30 = []

wss_sleep = [
    # (STAML1_ARIMAS1,(20,(2, 1, 2),10,0.05)),

]
wss1 = [
    # (LTA_BORSCH,(10,3)),
    # (LTA_APHOBO,(10,1)),
    (LTA_KROSH,(5,15)),
    (LTA_OKROSHKA,(10,15)),
    (OGTA4_DOG,(25,30)),
    (OGTA4_DOG,(15,30)),
    (PTA4_WDVCr,(11,)),
    (PTA4_WDDCr,(4,30)), #C
    (PTA4_WDDCr,(6,30)), #C
    (PTA4_WDDCr,(11,30)), #C
    # (PTA4_WDDCr,(12,25)), #C
    (PTA4_WDDCr,(10,20)), #C
    (PTA4_WDDCr,(21,30)), #C
    (PTA4_WDDCrE,(11,30)), #C
    # (PTA4_WDDCrE,(10,20)), #C
    # (PTA4_WDDCrE,(6,30)), #C
    (PTA4_WDDCrVG,(11,30)),
    (PTA4_WDDCde,(15,30)), #S
    (PTA4_WLISICA,(7,2,30)),
    (PTA2_LISICA,(7,2)),

    (PTA8_WDOBBY_FREEr,(11,0.5,30)),
    (PTA8_WDOBBY_FREEr,(6,0.5,30)),

]


max_period1 = (max(list(map(lambda x: x[1][0],wss1)))+1)*3
# max_period10 = (max(list(map(lambda x: x[1][0],wss10)))+1)*3
# max_period15 = (max(list(map(lambda x: x[1][0],wss15)))+1)*3
# max_period30 = (max(list(map(lambda x: x[1][0],wss30)))+1)*3
# print('Max period 15:',max_period15)
# print('Max period 30:',max_period30)
# symbol = "DOGEUSDT"
# granularity = "5m"
# productType = "usdt-futures"
# n_parts = 1
# limit = (max_period1+1)*3
# Получаем текущую дату
today = date.today()

# Вычитаем один день, чтобы получить вчерашнюю дату
yesterday = str(today - timedelta(days=3))

tickers = (
    ('CRH5',True),
    ('MMH5',True),
    ('GZH5',True),
    ('SRH5',True),
    ('SBER',False),
    ('GAZP',False),
    ('VTBR',False),
    ('LKOH',False),
    ('MTLR',False),
    ('TATN',False),
    ('ROSN',False),
    ('AFKS',False),
    ('ALRS',False),
    ('GMKN',False),
    ('MAGN',False),
    ('MOEX',False),
    ('NLMK',False),
    ('NVTK',False),
    ('RUAL',False),
    ('CHMF',False),
    ('SELG',False),
    ('YDEX',False),

)
print('Ботов 1:',len(wss1))
print('Тикеров 1:',len(tickers))
# print('Ботов 10:',len(wss10))
print('Всего ботов:',len(wss1)*len(tickers))
print('Max period 1:',max_period1)
# print('Max period 10:',max_period10)
# ticker = 'MMH5'
# ticker = 'SNGSP'
def trade_bots(granularity,bots,bots2,func):
    for ticker,fut in tickers:
        if fut:
            board = "RFUD"
            market = "forts"
            engine= "futures"
        else:
            board = "TQBR"
            market: str = "shares"
            engine: str = "stock"
        df = download_moex(ticker,granularity,yesterday,board=board,market=market,engine=engine)
        df = create_df(df)
        for bot in bots[ticker]:
            # print(bot)
            df_c = df.copy()
            func(bot,df_c)
        df = convert_chart1to5(df)
        for bot in bots2[ticker]:
            df_c = df.copy()
            func(bot,df_c)
        sleep(0.1)
def prepare_bots(folder,wss,granularity):
    bots = defaultdict(list)
    for ticker,fut in tickers:
        for WS,conf in wss:
            strategy = WS(ticker,granularity,fut,1,*conf)
            # bot = TestBot1("DOGEUSDT",strategy,conf)
            bot = TestMarketBot1(folder,ticker,strategy,conf)
            bots[ticker].append(bot)
    return bots
bots1 = prepare_bots('MOEX',wss1,1)
bots5 = prepare_bots('MOEX',wss1,5)
# bots10 = prepare_bots('MOEX',wss10,10)
# print(bots1)

while True:
    # start = time()
    try:
        trade_bots(1,bots1,bots5,lambda bot,df:bot.run(df))
        # trade_bots(10,bots10,lambda bot,df:bot.run(df))


    except KeyboardInterrupt:
        print('Close all position...')
        trade_bots(1,bots1,bots5,lambda bot,df:bot.cancel_trade(df))
        # trade_bots(10,bots10,lambda bot,df:bot.cancel_trade(df))
        print('Position closed!')
        sys.exit(0)
    except:
        print('Ошибка')

    # print('Time:',time()-start)
        # df.info()
        # sleep(3)