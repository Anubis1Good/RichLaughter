import sys
from time import sleep,time
from Bots.TestBot1 import TestBot1,TestMarketBot1
from request_functions.download_bitget import get_df
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
    (LTA_MISO,(52,9,26,52,14,12,26,9)),
    (LTA_BORSCH,(10,3)),

    (STA1_LITE,(20,2,0.5,20)),

]

wss5 = [
    (LTA_BORSCH,(3,3)),
    (LTA_APHOGA,(10,1)),
    (LTA_TOMYAM,(50,)),

    (PTA2_DVCr,(10,)),
    (PTA2_DDCde,(20,)),
    (PTA2_DDCrVG,(10,)),

    (PTA4_WDVCr,(10,)),
    (PTA4_WDDCr,(10,30)), #C
    (PTA4_WDDCrE,(10,30)), #C
    (PTA4_WDDCrVG,(10,30)),

    (PTA8_WDOBBY_FREEr,(8,0.5,30)),

    (STAML1_XGBR2_DC,(5,5)), #S
    (STAML1_XGBR2_DCh,(5,5)), #S

]
wss15 = [
    (LTA_RAMEN,(50,3)),
    (LTA_APHOBO,(10,1)),

    (PTA2_LISICA,(7,2)),
    (PTA2_DDCrWork,(5,)),

    (PTA4_WDDCde,(20,30)), #S
    (PTA4_WLISICA,(7,2,30)),
    (PTA4_WDDCr,(5,30)), #C
    (PTA4_WDDCrVG,(9,30)),
    (PTA4_WDVCr,(9,)),


    (PTA8_LOBSTER,(7,0.5)), #S
    (PTA8_OBBY_FREEr,(7,0.5)), #S
    (PTA8_OBBY,(4,0.5)), #S

    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA9_RAB,(10,2,5,0.5)),


    (STAML1_PROPHET2,(5,20)),
    (STAML1_PROPHET2s,(5,20)),
    (STAML1_PROPHET3,(20,20,0.03)),
    (STAML1_PROPHET3s,(20,20,0.03)),
    (STAML1_XGBR2,(60,5)), #S
    (STAML1_XGBR2,(5,5)), #S
    (STAML1_XGBR2e,(5,5)), #S
    (STAML1_XGBR2he,(5,5)), #S
    (STAML1_XGBR4,(60,5)),
    (STAML1_XGBR5,(60,5)),
    (STAML1_XGBR6,(60,5)),
    (STAML1_XGBR7,(60,5)),
    (STAML1_XGBR8,(60,5)),

]
wss30 = [
    (PTA4_WDDCr,(4,30)), #C

    (PTA6_KAMA,(5,20)),
    (PTA6_KAMA2,(5,5,21,30)),
    (PTA6_KAMAZ2,(5,20,21,30)),

    (PTA8_LOBSTER,(3,0.5)), #S
    (PTA8_WDOBBY_FREEr,(4,0.5,30)),
    (PTA8_DOBBY_FREEr,(4,0.5)),
    (PTA8_DOBBY,(4,0.5)),

    (PTA10_MAGIC,(95,20,4)),

    (STAML1_XGBR2h,(5,5)), #S
    (STAML1_PROPHET1,(60,20)), #fee problem
    (STAML1_PROPHET1s,(60,20)), #fee problem

]
# wss = [
#     (STAML1_LR1,(60,5)),
# ]
max_period1 = (max(list(map(lambda x: x[1][0],wss1)))+1)*3
max_period5 = (max(list(map(lambda x: x[1][0],wss5)))+1)*3
max_period15 = (max(list(map(lambda x: x[1][0],wss15)))+1)*3
max_period30 = (max(list(map(lambda x: x[1][0],wss30)))+1)*3
print('Ботов 1:',len(wss1))
print('Ботов 5:',len(wss5))
print('Ботов 15:',len(wss15))
print('Ботов 30:',len(wss30))
print('Max period 1:',max_period1)
print('Max period 5:',max_period5)
print('Max period 15:',max_period15)
print('Max period 30:',max_period30)
symbol = "DOGEUSDT"
granularity = "5m"
productType = "usdt-futures"
n_parts = 1
# limit = (max_period1+1)*3
def trade_bots(symbol,granularity,max_period,bots,func):
    df = get_df(symbol,granularity,productType,max_period)
    for bot in bots:
        df_c = df.copy()
        func(bot,df_c)
def prepare_bots(folder,wss,granularity):
    bots = []
    for WS,conf in wss:
        strategy = WS(symbol,granularity,productType,n_parts,*conf)
        # bot = TestBot1("DOGEUSDT",strategy,conf)
        bot = TestMarketBot1(folder,symbol,strategy,conf)
        bots.append(bot)
    return bots
bots1 = prepare_bots('bitget',wss1,"1m")
bots5 = prepare_bots('bitget',wss5,"5m")
bots15 = prepare_bots('bitget',wss15,"15m")
bots30 = prepare_bots('bitget',wss30,"30m")
# for WS,conf in wss1:
#     strategy = WS(symbol,'1m',productType,n_parts,*conf)
#     # bot = TestBot1("DOGEUSDT",strategy,conf)
#     bot = TestMarketBot1("DOGEUSDT",strategy,conf)
#     bots1.append(bot)
# for WS,conf in wss5:
#     strategy = WS(symbol,'5m',productType,n_parts,*conf)
#     # bot = TestBot1("DOGEUSDT",strategy,conf)
#     bot = TestMarketBot1("DOGEUSDT",strategy,conf)
#     bots5.append(bot)
# for WS,conf in wss15:
#     strategy = WS(symbol,'15m',productType,n_parts,*conf)
#     # bot = TestBot1("DOGEUSDT",strategy,conf)
#     bot = TestMarketBot1("DOGEUSDT",strategy,conf)
#     bots15.append(bot)
# for WS,conf in wss30:
#     strategy = WS(symbol,'30m',productType,n_parts,*conf)
#     # bot = TestBot1("DOGEUSDT",strategy,conf)
#     bot = TestMarketBot1("DOGEUSDT",strategy,conf)
#     bots30.append(bot)

while True:
    # start = time()
    # print(strategy())
    try:
        trade_bots(symbol,'1m',max_period1,bots1,lambda bot,df:bot.run(df))
        trade_bots(symbol,'5m',max_period5,bots5,lambda bot,df:bot.run(df))
        trade_bots(symbol,'15m',max_period15,bots15,lambda bot,df:bot.run(df))
        trade_bots(symbol,'30m',max_period30,bots30,lambda bot,df:bot.run(df))
        # df = get_df(symbol,'1m',productType,(max_period1+1)*3)
        # for bot in bots1:
        #     df_c = df.copy()
        #     bot.run(df_c)
        # df = get_df(symbol,'5m',productType,(max_period5+1)*3)
        # for bot in bots5:
        #     df_c = df.copy()
        #     bot.run(df_c)
        # df = get_df(symbol,'15m',productType,(max_period15+1)*3)
        # for bot in bots15:
        #     df_c = df.copy()
        #     bot.run(df_c)
        # df = get_df(symbol,'30m',productType,(max_period30+1)*3)
        # for bot in bots30:
        #     df_c = df.copy()
        #     bot.run(df_c)
    except KeyboardInterrupt:
        print('Close all position...')
        trade_bots(symbol,'1m',max_period1,bots1,lambda bot,df:bot.cancel_trade(df))
        trade_bots(symbol,'5m',max_period5,bots5,lambda bot,df:bot.cancel_trade(df))
        trade_bots(symbol,'15m',max_period15,bots15,lambda bot,df:bot.cancel_trade(df))
        trade_bots(symbol,'30m',max_period30,bots30,lambda bot,df:bot.cancel_trade(df))
        # df = get_df(symbol,'1m',productType,(max_period1+1)*3)
        # for bot in bots1:
        #     df_c = df.copy()
        #     bot.cancel_trade(df_c)
        # df = get_df(symbol,'5m',productType,(max_period5+1)*3)
        # for bot in bots5:
        #     df_c = df.copy()
        #     bot.cancel_trade(df_c)
        # df = get_df(symbol,'15m',productType,(max_period15+1)*3)
        # for bot in bots15:
        #     df_c = df.copy()
        #     bot.cancel_trade(df_c)
        # df = get_df(symbol,'30m',productType,(max_period30+1)*3)
        # for bot in bots30:
        #     df_c = df.copy()
        #     bot.cancel_trade(df_c)
        print('Position closed!')
        sys.exit(0)
    except:
        print('Some Error')
    # print('Time:',time()-start)
        # df.info()
        # sleep(3)