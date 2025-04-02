import sys
from time import sleep,time
from datetime import date, timedelta
from collections import defaultdict
from Bots.TestBot3 import TestBot3
from request_functions.download_moex import download_moex,create_df
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
from Optimiztion.Optimizator1 import generate_combinations
from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDDCr2,PTA4_UNIVERSAL,PTA4_UNIVERSAL2,PTA2_LISICA
from strategies.work_strategies.PTAX import PTA10_WIZARD,PTA10_SORCERER,PTA11_KUSURUKEN,PTA12_SWDDCr,PTA14_RWDDCr,PTA15_NOVA,PTA15_KERRIGAN,PTA15_WIDOWMAKER
from strategies.work_strategies.MTA import MTA_LORD,MTA_LORD2
# from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
# from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.STA_ml2 import STAML2_CHAOS,STAML2_FLUX,STAML2_LEGACY,STAML2_TRADITION,STAML2_BALANCE,STAML2_NEWAVE
from strategies.work_strategies.LTA import LTA_KROSH,LTA_OKROSHKA,LTA_PIN
from strategies.work_strategies.LTA2 import LTA2_MONSTER,LTA2_OVERLORD
from strategies.work_strategies.OGTA import OGTA4_DOG

# bots1 = []
# bots5 = []
# bots15 = []
# bots30 = []


wss1 = [
    (LTA_KROSH,(10,20)),
    (LTA_PIN,(10,7,50,5)),
    (LTA_PIN,(10,9,45,3)),
    (LTA_OKROSHKA,(10,15)),
    (LTA_OKROSHKA,(10,30)),

    # (LTA2_MONSTER,(40,20,5,3,40)), #F
    # (LTA2_MONSTER,(40,40,5,2,50)), #A
    # (LTA2_OVERLORD,(30,55,50,2)), #A
    
    (OGTA4_DOG,(15,30)),
    (OGTA4_DOG,(25,30)),

    (STAML2_CHAOS,(60,2,200)),
    (STAML2_BALANCE,(60,2,200,30)),
    (STAML2_BALANCE,(60,2,30,30)),
    # (STAML2_BALANCE,(60,2,60,30)),
    (STAML2_TRADITION,(5,5,0.5)),
    (STAML2_NEWAVE,(5,5,0.5,30)),


    (PTA2_LISICA,(7,2)), 
    (PTA2_LISICA,(14,2)), 

    (PTA4_WDDCr,(6,20)), #C
    (PTA4_WDDCr,(6,30)), #C
    (PTA4_WDDCr,(11,30)), #C
    (PTA4_WDDCr,(12,25)), #C
    (PTA4_WDDCr,(10,20)), #C
    (PTA4_WDDCr,(21,30)), #C
    (PTA4_WDDCr,(30,30)), #C
    (PTA4_WDDCrE,(11,30)), #C
    (PTA4_WDDCrE,(10,20)), #C
    (PTA4_WDDCrE,(6,30)), #C
    (PTA4_WDDCr2,(11,30)), #C
    (PTA4_WDDCrVG,(11,30)),
    (PTA4_WDDCrVG,(21,30)),
    (PTA4_WDVCr,(11,30)),
    (PTA4_WDVCr,(21,30)),
    (PTA4_WLISICA,(7,2,30)),
    (PTA4_WLISICA,(14,2,30)),

    (PTA8_WDOBBY_FREEr,(11,2,30)),
    (PTA8_WDOBBY_FREEr,(11,0.5,30)),
    (PTA8_WDOBBY_FREEr,(6,0.5,30)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_SORCERER,(20,5,12,30,20,10)),
    (PTA10_SORCERER,(80,20,15,30,5,20)),
    (PTA10_SORCERER,(100,50,15,20,5,10)),

    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F
    (PTA11_KUSURUKEN,(70,3,10,40,'hl')), #F
    (PTA11_KUSURUKEN,(50,6,5,20,'c')), #A
    (PTA11_KUSURUKEN,(70,15,35,10,'c')), #A

    (PTA12_SWDDCr,(10,40,0.25,5,5)), #F
    (PTA12_SWDDCr,(10,30,1,5,15)), #A
    (PTA12_SWDDCr,(10,20,1,20,15)), #A
    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A

    (PTA14_RWDDCr,(15,30,35,45)), #F
    (PTA14_RWDDCr,(10,40,30,40)), #F
    (PTA14_RWDDCr,(10,30,35,35)), #A
    (PTA14_RWDDCr,(10,20,30,30)), #A
    
    (PTA15_KERRIGAN,(5,)), #A
    (PTA15_NOVA,(5,)), #A
    (PTA15_NOVA,(10,)), #A
    (PTA15_NOVA,(15,)), #A
    (PTA15_NOVA,(30,)), #A
    (PTA15_NOVA,(60,)), #A
    (PTA15_KERRIGAN,(60,)), #A
    (PTA15_WIDOWMAKER,(10,20)), 
    (PTA15_WIDOWMAKER,(5,30)), 
]


max_period1 = (max(list(map(lambda x: x[1][0],wss1)))+1)*3
today = date.today()

# Вычитаем один день, чтобы получить вчерашнюю дату
yesterday = str(today - timedelta(days=3))

tickers = (
    ('CRM5',True),
    ('MMM5',True),
    ('GZM5',True),
    ('SRM5',True),
    ('RIM5',True),
)
print('Ботов 1:',len(wss1))
print('Тикеров 1:',len(tickers))
# print('Ботов 10:',len(wss10))
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
            if check_time:
                start2 = time()
            func(bot,df_c)
            if check_time:
                print(time()-start2,bot)
        df = convert_chart1to5(df)
        for bot in bots2[ticker]:
            df_c = df.copy()
            func(bot,df_c)
        sleep(0.1)

def prepare_bots(wss,granularity):
    bots = defaultdict(list)
    for ticker,fut in tickers:
        for WS,conf in wss:
            strategy = WS(ticker,granularity,fut,1,*conf)
            # bot = TestBot1("DOGEUSDT",strategy,conf)
            bot = TestBot3('dbs/moex_fut.db',0.00001,ticker,granularity,strategy,conf)
            bots[ticker].append(bot)
    return bots

def append_mta_bot(ws,bots,wss_str,granularity,wss_f):
    for ticker,fut in tickers:
        if fut:
            fee=0.00001
        else:
            fee=0.0002
        conf  = (100,wss_f,fee,3)
        strategy = ws(ticker,granularity,fut,1,*conf)
        bot = TestBot3('dbs/moex_fut.db',0.00001,ticker,granularity,strategy,(wss_str,))
        bots[ticker].append(bot)

def append_lord2_bot(ws,bots,wss_str,granularity,wss,period):
    for ticker,fut in tickers:
        if fut:
            fee=0.00001
        else:
            fee=0.0002
        conf  = (period,fee)
        strategy = ws(ticker,granularity,fut,1,*conf,wss)
        bot = TestBot3('dbs/moex_fut.db',0.00001,ticker,granularity,strategy,(conf[0],wss_str))
        bots[ticker].append(bot)

bots1 = prepare_bots(wss1,1)
bots5 = prepare_bots(wss1,5)

wss_u2 = []
configs2 = generate_combinations((
    (10,),
    (10,),
    (30,60),
    (30,60),
    ('DC',),
    ("rsi",),
    (0,1),
    (0,1)
))
print(len(configs2))
for conf in configs2:
    wss_u2.append((PTA4_UNIVERSAL,conf))

append_mta_bot(MTA_LORD,bots1,'u12',1,wss_u2)
append_mta_bot(MTA_LORD,bots5,'u52',5,wss_u2)
append_lord2_bot(MTA_LORD2,bots1,'wss_u2',1,wss_u2,60)
append_lord2_bot(MTA_LORD2,bots5,'wss_u2',5,wss_u2,60)
append_lord2_bot(MTA_LORD2,bots1,'wss_u2',1,wss_u2,30)
append_lord2_bot(MTA_LORD2,bots5,'wss_u2',5,wss_u2,30)



print('Всего ботов:',len(bots1)*len(bots5))
# bots10 = prepare_bots('MOEX',wss10,10)
# print(bots1)

check_time = True
check_time2 = True
check_time = False
check_time2 = False

while True:
    if check_time2:
        start = time()
    try:
        trade_bots(1,bots1,bots5,lambda bot,df:bot.run(df))
        # trade_bots(10,bots10,lambda bot,df:bot.run(df))


    except KeyboardInterrupt:
        print('Close all position...')
        trade_bots(1,bots1,bots5,lambda bot,df:bot.cancel_trade(df))
        # trade_bots(10,bots10,lambda bot,df:bot.cancel_trade(df))
        print('Position closed!')
        break
        # sys.exit(0)
    except:
        print('Ошибка')
    if check_time2:
        print('Time:',time()-start)
        # df.info()
        # sleep(3)
print('Close all position...')
trade_bots(1,bots1,bots5,lambda bot,df:bot.cancel_trade(df))
# trade_bots(10,bots10,lambda bot,df:bot.cancel_trade(df))
print('Position closed!')