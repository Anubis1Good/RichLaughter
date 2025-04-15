import sys
from time import sleep,time
import traceback
from datetime import date, timedelta
from collections import defaultdict
from tqdm import tqdm
from Bots.TestBot3 import TestBot3
from Loader.BitgetLoader import bitget_loader
from Optimiztion.Optimizator1 import generate_combinations
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
# from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDDCr2,PTA4_WDDCr2E,PTA4_WDDC,PTA2_DDCrWork,PTA2_BDDC,PTA4_UNIVERSAL
# from strategies.work_strategies.PTAX import PTA16_ARTANIS,PTA16_CHEN,PTA16_LEORIC
# from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
# from strategies.work_strategies.STA_ca import STA1_LITE
# from strategies.work_strategies.STA_ml2 import STAML2_SID as WS
from strategies.work_strategies.STA_ml2 import STAML2_BALANCE,STAML2_GOLDENMEAN 
# from strategies.work_strategies.LTA import LTA_KROSH,LTA_OKROSHKA,LTA_BARASH,LTA_EJIK,LTA_KARYCH,LTA_KOPATYCH,LTA_LOSYASH,LTA_NUSHA,LTA_PIN,LTA_SAVUNIA
# from strategies.work_strategies.OGTA import OGTA4_DOG
# from strategies.work_strategies.MTA import MTA_LORD2 as WS
# from strategies.work_strategies.experiments import ExpBot as WS
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_15m_1739873596.csv'
raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1744615735.csv'
df = bitget_loader(raw_file)


# sys.exit(0)
tickers = (
    ('MXI',True,STAML2_BALANCE,(60,2,30,30)),
    ('MXI',True,STAML2_GOLDENMEAN,(60,2,30,30)),
    # ('MXI',True,STAML2_FLUX,(60,0.2,2,100)),
    # ('MXI',True,WS,(200,10,5,30,0.2)),
    # ('MXI',True,WS,(200,10,5,30,0.05)),
    # ('MXI',True,WS,(200,20,10)),
)
print('Тикеров 1:',len(tickers))
# print('Ботов 10:',len(wss10))
print('Всего ботов:',len(tickers))
max_period1 = 300
# print('Max period 10:',max_period10)
# ticker = 'MMH5'
# ticker = 'SNGSP'

def trade_bots(df,bots,func):
    for ticker,fut,ws,conf in tickers:
        for bot in bots[ticker]:
            df_c = df.copy()
            func(bot,df_c)

def prepare_bots(granularity):
    bots = defaultdict(list)
    for ticker,fut,ws,conf in tickers:
        if fut:
            fee=0.00001
        else:
            # fee=0.0002
            fee=0.0012
        # conf  = (60,wss,fee)
        strategy = ws(ticker,granularity,fut,1,*conf)
        print(strategy.period)
        # bot = TestMarketBot1(folder,ticker,strategy,conf,'LogsOffTest')
        bot = TestBot3('dbs/test_offline.db',fee,'MMH5',granularity,strategy,conf)
        bots[ticker].append(bot)
    return bots
bots1 = prepare_bots(1)

length_df = len(df.index)
for i in tqdm(range(max_period1,length_df)):
    df_w = df.iloc[i-max_period1:i]
    try:
        trade_bots(df_w,bots1,lambda bot,df:bot.run(df))
    except KeyboardInterrupt:
        print('Close all position...')
        trade_bots(df_w,bots1,lambda bot,df:bot.cancel_trade(df))
        print('Position closed!')
        break
    except Exception as err:
        traceback.print_exc()
        break

print('Close all position...')
trade_bots(df_w,bots1,lambda bot,df:bot.cancel_trade(df))
print('Position closed!')