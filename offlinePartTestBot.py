import sys
from time import sleep,time
from datetime import date, timedelta
from collections import defaultdict
from tqdm import tqdm
from Bots.TestBot1 import TestMarketBot1
from Loader.BitgetLoader import bitget_loader
from Optimiztion.Optimizator1 import generate_combinations
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDDCr2,PTA4_WDDCr2E,PTA4_WDDC,PTA2_DDCrWork,PTA2_BDDC,PTA4_UNIVERSAL
from strategies.work_strategies.PTAX import PTA10_WIZARD
# from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
# from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_KROSH,LTA_OKROSHKA,LTA_BARASH,LTA_EJIK,LTA_KARYCH,LTA_KOPATYCH,LTA_LOSYASH,LTA_NUSHA,LTA_PIN,LTA_SAVUNIA
from strategies.work_strategies.OGTA import OGTA4_DOG
from strategies.work_strategies.MTA import MTA_LORD as WS
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_15m_1739873596.csv'
raw_file = 'DataForTests\DataFromMOEX\MMH5_1_1739993452.csv'
df = bitget_loader(raw_file)

wss_f = (
    (PTA2_DDCrWork,(5,)),
    (PTA2_BDDC,(5,)),

)

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

lenght_history = 4
max_period1 = (max(list(map(lambda x: x[1][0],wss1)))+1)*lenght_history

wss = []
configs = generate_combinations((
    (7,),
    (7,),
    (30,50),
    (30,50),
    ('DC',),
    ("rsi",),
    (0,1),
    (0,1)
))
for conf in configs:
    wss.append((PTA4_UNIVERSAL,conf))
print(len(wss))
# sys.exit(0)
tickers = (
    ('MXI',True),
)
print('Ботов 1:',len(wss1))
print('Тикеров 1:',len(tickers))
# print('Ботов 10:',len(wss10))
print('Всего ботов:',len(wss1)*len(tickers))
print('Max period 1:',max_period1)
# print('Max period 10:',max_period10)
# ticker = 'MMH5'
# ticker = 'SNGSP'

def trade_bots(df,bots,func):
    for ticker,fut in tickers:
        for bot in bots[ticker]:
            df_c = df.copy()
            func(bot,df_c)

def prepare_bots(folder,granularity):
    bots = defaultdict(list)
    for ticker,fut in tickers:
        if fut:
            fee=0.00001
        else:
            # fee=0.0002
            fee=0.0012
        conf  = (100,wss,fee,4)
        strategy = WS(ticker,granularity,fut,1,*conf)
        print(strategy.period)
        bot = TestMarketBot1(folder,ticker,strategy,('u1h4',),'LogsOffTest')
        bots[ticker].append(bot)
    return bots
bots1 = prepare_bots('OPTB',1)

length_df = len(df.index)
for i in tqdm(range(max_period1,length_df)):
    df_w = df.iloc[i-max_period1:i]
    try:
        trade_bots(df_w,bots1,lambda bot,df:bot.run(df))
    except:
        break

print('Close all position...')
trade_bots(df_w,bots1,lambda bot,df:bot.cancel_trade(df))
print('Position closed!')