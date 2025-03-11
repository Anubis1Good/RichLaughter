import sys
from time import sleep,time
from datetime import date, timedelta
from collections import defaultdict
from Bots.TestBot1 import TestBot1,TestMarketBot1
from request_functions.download_moex import download_moex,create_df
from strategies.work_strategies.PTA import PTA2_DDCde,PTA2_LISICA,PTA8_LOBSTER,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA8_OBBY_FREEr,PTA9_RAB,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA10_MAGIC,PTA6_KAMA,PTA6_KAMA2,PTA6_KAMAZ2
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_APHOBO,LTA_APHOGA,LTA_BORSCH,LTA_MISO,LTA_RAMEN,LTA_TOMYAM

# bots1 = []
# bots5 = []
# bots15 = []
# bots30 = []

wss_sleep = [
    # (STAML1_ARIMAS1,(20,(2, 1, 2),10,0.05)),

]
wss1 = [
    # (LTA_BORSCH,(10,3)),

    # (STA1_LITE,(20,2,0.5,10)),
    (PTA4_WDVCr,(11,)),
    (PTA4_WDDCr,(6,30)), #C
    (PTA4_WDDCr,(11,30)), #C
    (PTA4_WDDCrE,(11,30)), #C
    (PTA4_WDDCrVG,(11,30)),
    (PTA4_WDDCde,(15,30)), #S
    (PTA4_WDDCde,(30,30)), #S
    (PTA4_WDDCde,(60,30)), #S
    (PTA4_WLISICA,(7,2,30)),

    (PTA8_WDOBBY_FREEr,(11,0.5,30)),
    (STAML1_XGBR2,(6,6)), #S

]

wss10 = [

    (PTA4_WDVCr,(5,)),
    (PTA4_WDDCr,(5,30)), #C
    (PTA4_WDDCrE,(5,30)), #C
    (PTA4_WDDCde,(10,30)), #S

    (PTA8_WDOBBY_FREEr,(8,0.5,30)),

    (STAML1_XGBR2,(5,5)), #S
    (STAML1_PROPHET1,(60,20)), #fee problem
    (STAML1_PROPHET2,(5,20)),
    (STAML1_PROPHET3,(20,20,0.03)),

    (STAML1_XGBR2_DC,(5,5)), #S
    (STAML1_XGBR2_DCh,(5,5)), #S
]

# wss60 = [
#     (LTA_RAMEN,(50,3)),
#     (LTA_APHOBO,(10,1)),

#     (PTA2_LISICA,(7,2)),
#     (PTA2_DDCrWork,(5,)),

#     (PTA4_WDDCr,(5,30)), #C
#     (PTA4_WDDCrVG,(9,30)),
#     (PTA4_WDVCr,(9,)),


#     (PTA8_LOBSTER,(7,0.5)), #S
#     (PTA8_OBBY_FREEr,(7,0.5)), #S
#     (PTA8_OBBY,(4,0.5)), #S

#     (PTA9_CRAB,(10,0.5,5,0.5)),
#     (PTA9_RAB,(10,2,5,0.5)),


#     (STAML1_PROPHET2s,(5,20)),
#     (STAML1_PROPHET3s,(20,20,0.03)),
#     (STAML1_XGBR2,(60,5)), #S
#     (STAML1_XGBR2e,(5,5)), #S
#     (STAML1_XGBR2he,(5,5)), #S
#     (STAML1_XGBR4,(60,5)),
#     (STAML1_XGBR5,(60,5)),
#     (STAML1_XGBR6,(60,5)),
#     (STAML1_XGBR7,(60,5)),
#     (STAML1_XGBR8,(60,5)),
#     (PTA4_WDDCr,(4,30)), #C

#     (PTA6_KAMA,(5,20)),
#     (PTA6_KAMA2,(5,5,21,30)),
#     (PTA6_KAMAZ2,(5,20,21,30)),

#     (PTA8_LOBSTER,(3,0.5)), #S
#     (PTA8_WDOBBY_FREEr,(4,0.5,30)),
#     (PTA8_DOBBY_FREEr,(4,0.5)),
#     (PTA8_DOBBY,(4,0.5)),

#     (PTA10_MAGIC,(95,20,4)),

#     (STAML1_XGBR2h,(5,5)), #S
#     (STAML1_PROPHET1,(60,20)), #fee problem
#     (STAML1_PROPHET1s,(60,20)), #fee problem
# ]

max_period1 = (max(list(map(lambda x: x[1][0],wss1)))+1)*3
max_period10 = (max(list(map(lambda x: x[1][0],wss10)))+1)*3
# max_period15 = (max(list(map(lambda x: x[1][0],wss15)))+1)*3
# max_period30 = (max(list(map(lambda x: x[1][0],wss30)))+1)*3
print('Ботов 1:',len(wss1))
print('Ботов 10:',len(wss10))
# print('Ботов 15:',len(wss15))
# print('Ботов 30:',len(wss30))
print('Max period 1:',max_period1)
print('Max period 10:',max_period10)
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
    ('SBER',False),
    ('GAZP',False),
    ('VTBR',False),
    ('LKOH',False),
    ('MTLR',False),
    ('TATN',False),
    ('ROSN',False)
)
# ticker = 'MMH5'
# ticker = 'SNGSP'
def trade_bots(granularity,max_period,bots,func):
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
        # print(len(df.index),max_period)
        # period = min(max_period,len(df.index)-1)
        # df = df.iloc[-period:]
        for bot in bots[ticker]:
            # print(bot)
            df_c = df.copy()
            func(bot,df_c)
        sleep(0.5)
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
bots10 = prepare_bots('MOEX',wss10,10)
# print(bots1)

while True:
    # start = time()
    try:
        trade_bots(1,max_period1,bots1,lambda bot,df:bot.run(df))
        trade_bots(10,max_period10,bots10,lambda bot,df:bot.run(df))


    except KeyboardInterrupt:
        print('Close all position...')
        trade_bots(1,max_period1,bots1,lambda bot,df:bot.cancel_trade(df))
        trade_bots(10,max_period10,bots10,lambda bot,df:bot.cancel_trade(df))
        print('Position closed!')
        sys.exit(0)
    except:
        print('Ошибка')

    # print('Time:',time()-start)
        # df.info()
        # sleep(3)