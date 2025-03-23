import sys
from time import sleep,time
from datetime import date, timedelta
from collections import defaultdict
from Bots.TestBot1 import TestMarketBot1
from request_functions.download_moex import download_moex,create_df
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
from Optimiztion.Optimizator1 import generate_combinations
from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDDCr2,PTA4_WDDCr2E,PTA4_WDDC,PTA4_UNIVERSAL
from strategies.work_strategies.PTAX import PTA10_WIZARD
from strategies.work_strategies.MTA import MTA_LORD
# from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
# from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_KROSH,LTA_OKROSHKA,LTA_BARASH,LTA_EJIK,LTA_KARYCH,LTA_KOPATYCH,LTA_LOSYASH,LTA_NUSHA,LTA_PIN,LTA_SAVUNIA
from strategies.work_strategies.OGTA import OGTA4_DOG

# bots1 = []
# bots5 = []
# bots15 = []
# bots30 = []


wss1 = [
    (LTA_KROSH,(5,15)),
    (LTA_KROSH,(10,20)),
    (LTA_KARYCH,(5,20)),
    (LTA_KOPATYCH,(10,40)),
    (LTA_LOSYASH,(10,45)),
    (LTA_BARASH,(35,35)),
    (LTA_NUSHA,(10,20)),
    (LTA_SAVUNIA,(30,25)),
    (LTA_EJIK,(10,5,10)),
    (LTA_PIN,(10,7,50,5)),
    (LTA_PIN,(10,9,45,3)),
    (LTA_OKROSHKA,(10,15)),
    (LTA_OKROSHKA,(10,30)),
    
    (OGTA4_DOG,(25,30)),
    (OGTA4_DOG,(20,40)),

    (PTA4_WDDC,(15,30)), #C
    (PTA4_WDDC,(30,30)),
      #C
    (PTA4_WDDCr,(6,30)), #C
    (PTA4_WDDCr2,(6,20)), #C
    (PTA4_WDDCr2E,(6,20)), #C
    (PTA4_WDDCr,(11,30)), #C
    (PTA4_WDDCr2,(11,30)), #C
    (PTA4_WDDCr2E,(11,30)), #C
    (PTA4_WDDCr,(10,20)), #C
    (PTA4_WDDCr,(21,30)), #C
    (PTA4_WDDCrE,(11,30)), #C
    (PTA4_WDDCrE,(10,20)), #C
    (PTA4_WDDCrE,(6,30)), #C
    (PTA4_WDDCrVG,(11,30)),
    (PTA4_WDVCr,(11,30)),
    (PTA4_WLISICA,(7,2,30)),

    (PTA8_WDOBBY_FREEr,(11,2,30)),
    (PTA8_WDOBBY_FREEr,(11,0.5,30)),
    (PTA8_WDOBBY_FREEr,(6,0.5,30)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_WIZARD,(30,55,3,15,20)),

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
    ('CRM5',True),
    ('MMM5',True),
    ('GZM5',True),
    ('SRM5',True),
    ('RIM5',True),
    ('SBER',False),
    ('GAZP',False),
    ('LKOH',False),
    ('ROSN',False),
    ('MTLR',False),
    ('MGNT',False),
    ('NVTK',False),
    ('GMKN',False),
    ('VTBR',False),
    ('TATN',False),
    ('TRNFP',False),
    ('AFKS',False),
    ('PIKK',False),
    ('MOEX',False),
    ('AFLT',False),
    ('CHMF',False),
    ('NLMK',False),
    ('SIBN',False),
    ('SNGSP',False),
    ('SNGS',False),
    ('ALRS',False),
    ('MAGN',False),
    ('MTSS',False),
    ('RUAL',False),
    ('FESH',False),
    ('IRAO',False),
    ('RTKM',False),
    ('UPRO',False),
    ('FEES',False),
    ('BANEP',False),
    ('TRMK',False),
    ('LSRG',False),
    ('CBOM',False),
    ('NMTP',False),
    ('HYDR',False),
    ('SELG',False),
    ('YDEX',False),
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

def append_mta_bot(folder,ws,bots,wss_str,granularity,wss_f):
    for ticker,fut in tickers:
        if fut:
            fee=0.00001
        else:
            fee=0.0002
        conf  = (100,wss_f,fee,4)
        strategy = ws(ticker,granularity,fut,1,*conf)
        bot = TestMarketBot1(folder,ticker,strategy,(wss_str,))
        bots[ticker].append(bot)

bots1 = prepare_bots('MOEX',wss1,1)
bots5 = prepare_bots('MOEX',wss1,5)

append_mta_bot('MOEX',MTA_LORD,bots1,'bots1',1,wss1)
append_mta_bot('MOEX',MTA_LORD,bots5,'bots5',5,wss1)

wss_u = []
configs = generate_combinations((
    (5,10,20),
    (5,10,20),
    (30,50),
    (30,50),
    ('DC',),
    ("rsi",),
    (0,1),
    (0,1)
))
for conf in configs:
    wss_u.append((PTA4_UNIVERSAL,conf))
append_mta_bot('MOEX',MTA_LORD,bots1,'u1',1,wss_u)
append_mta_bot('MOEX',MTA_LORD,bots5,'u5',5,wss_u)


print('Всего ботов:',len(bots1)*len(bots5))
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