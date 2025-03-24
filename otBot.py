import sys
from time import sleep,time
from Bots.TestBot1 import TestMarketBot1
from request_functions.download_bitget import get_df
from Optimiztion.Optimizator1 import generate_combinations
from strategies.work_strategies.PTA import PTA2_LISICA,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_DOBBY_FREEr,PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDDCr2,PTA4_WDDCr2E,PTA4_WDDC,PTA4_UNIVERSAL
from strategies.work_strategies.PTAX import PTA10_WIZARD
# from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
# from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.OGTA import OGTA4_DOG
from strategies.work_strategies.LTA import LTA_APHOBO,LTA_KROSH,LTA_OKROSHKA,LTA_OKROSHKA2,LTA_PIN,LTA_KOPATYCH,LTA_LOSYASH,LTA_KARYCH,LTA_EJIK,LTA_BARASH,LTA_SAVUNIA,LTA_NUSHA
from strategies.work_strategies.MTA import MTA_LORD

# bots1 = []
# bots5 = []
# bots15 = []
# bots30 = []

wss_sleep = [
    # (STAML1_ARIMAS1,(20,(2, 1, 2),10,0.05)),
    # (LTA_MISO,(52,9,26,52,14,12,26,9)),

]
wss1 = [
    (LTA_PIN,(60,3,25,5)),
    (LTA_KOPATYCH,(50,45)),
    (LTA_LOSYASH,(25,55)),
    (LTA_EJIK,(65,9,5)),
    (LTA_KROSH,(45,20)),
    (LTA_OKROSHKA,(15,10)),
    (LTA_OKROSHKA2,(15,10)),
    (OGTA4_DOG,(45,15)),
    (OGTA4_DOG,(35,20)),

    (PTA4_WDDC,(30,30)), #C
    (PTA4_WDDC,(60,30)), #C
    (PTA4_WDDCr,(30,30)), #C
    (PTA4_WDDCr,(21,20)), #C

    (PTA10_WIZARD,(30,35,12,10,40)), #S
]

wss5 = [
    (LTA_PIN,(20,7,5,1)),
    (LTA_KROSH,(20,30)),
    (LTA_EJIK,(35,6,5)),
    (LTA_EJIK,(20,6,5)),
    (LTA_KARYCH,(30,35)),
    (LTA_OKROSHKA,(20,65)),
    (LTA_OKROSHKA2,(20,65)),
    (OGTA4_DOG,(10,15)),



    (PTA4_WDDC,(15,30)), #C
    (PTA4_WDDCr,(6,20)), #C
    (PTA4_WDDCr,(10,20)), #C
    (PTA4_WDDCr,(21,30)), #C
    (PTA4_WDDCr2,(20,35)), #C



]
wss15 = [
    (LTA_APHOBO,(10,1)),
    (LTA_KOPATYCH,(20,45)),
    (LTA_EJIK,(25,7,10)),
    (LTA_KROSH,(10,35)),
    (LTA_KARYCH,(5,15)),
    (LTA_BARASH,(25,45)),
    (LTA_NUSHA,(20,35)),
    (LTA_SAVUNIA,(65,35)),
    (LTA_OKROSHKA2,(5,60)),
    (OGTA4_DOG,(5,20)),
    (OGTA4_DOG,(15,25)),

    (PTA2_LISICA,(7,1)),
    (PTA2_LISICA,(14,2)),
    (PTA4_WLISICA,(7,2,20)),
    (PTA2_DDCrWork,(5,)),


    (PTA4_WDDC,(10,30)), #C
    (PTA4_WDDCr2,(5,15)), #C
    (PTA4_WDDCr2E,(5,20)), #C
    (PTA4_WDDCr,(3,40)), #C
    (PTA4_WDDCr,(3,20)), #C
    (PTA4_WDDCrE,(5,20)), #C
    (PTA4_WDDCrVG,(9,20)),
    (PTA4_WDVCr,(9,20)),

    (PTA8_OBBY,(4,0.5)), #S
    (PTA10_WIZARD,(30,35,6,10,20)), #S



]
wss30 = [
    (PTA8_WDOBBY_FREEr,(4,2,20)),
    (PTA8_WDOBBY_FREEr,(4,0.5,20)),
    (PTA8_DOBBY_FREEr,(4,0.5)),
    (PTA8_DOBBY,(4,0.5)),
    (PTA8_DOBBY,(8,2)),

]
# wss = [
#     (STAML1_LR1,(60,5)),
# ]
max_period1 = (max(list(map(lambda x: max(x[1]),wss1)))+1)*3
max_period5 = (max(list(map(lambda x: max(x[1]),wss5)))+1)*3
max_period15 = (max(list(map(lambda x: max(x[1]),wss15)))+1)*3
max_period30 = (max(list(map(lambda x: max(x[1]),wss30)))+1)*3
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
    # sleep(0.1)
def prepare_bots(folder,wss,granularity):
    bots = []
    for WS,conf in wss:
        strategy = WS(symbol,granularity,productType,n_parts,*conf)
        # bot = TestBot1("DOGEUSDT",strategy,conf)
        bot = TestMarketBot1(folder,symbol,strategy,conf)
        bots.append(bot)
    return bots

def append_mta_bot(folder,ws,bots,wss_str):
    strategy = ws[0](symbol,granularity,productType,n_parts,*ws[1])
    bot = TestMarketBot1(folder,symbol,strategy,(wss_str,))
    bots.append(bot)

bots1 = prepare_bots('bitget',wss1,"1m")
bots5 = prepare_bots('bitget',wss5,"5m")
bots15 = prepare_bots('bitget',wss15,"15m")
bots30 = prepare_bots('bitget',wss30,"30m")
wss_u = []
configs = generate_combinations((
    (5,10),
    (5,10),
    (30,50),
    (30,50),
    ('DC',),
    ("rsi",),
    (0,1),
    (0,1)
))
for conf in configs:
    wss_u.append((PTA4_UNIVERSAL,conf))
fee = 0.0012
granularity = "1m"
append_mta_bot('bitget',(MTA_LORD,(100,wss1,fee)),bots1,'wss1')
append_mta_bot('bitget',(MTA_LORD,(100,wss1,fee,2)),bots1,'wss1s')
append_mta_bot('bitget',(MTA_LORD,(100,wss_u,fee)),bots1,'u1')
granularity = "5m"
append_mta_bot('bitget',(MTA_LORD,(100,wss5,fee)),bots5,'wss5')
append_mta_bot('bitget',(MTA_LORD,(100,wss5,fee,2)),bots5,'wss5s')
append_mta_bot('bitget',(MTA_LORD,(100,wss_u,fee)),bots5,'u5')
granularity = "15m"
append_mta_bot('bitget',(MTA_LORD,(100,wss15,fee)),bots15,'wss15')
append_mta_bot('bitget',(MTA_LORD,(100,wss15,fee,2)),bots15,'wss15s')
append_mta_bot('bitget',(MTA_LORD,(100,wss_u,fee)),bots15,'u15')
granularity = "30m"
append_mta_bot('bitget',(MTA_LORD,(100,wss30,fee)),bots30,'wss30')
append_mta_bot('bitget',(MTA_LORD,(100,wss30,fee,2)),bots30,'wss30s')
append_mta_bot('bitget',(MTA_LORD,(100,wss_u,fee)),bots30,'u30')



print('Ботов 1:',len(bots1))
print('Ботов 5:',len(bots5))
print('Ботов 15:',len(bots15))
print('Ботов 30:',len(bots30))

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

    except KeyboardInterrupt:
        print('Close all position...')
        trade_bots(symbol,'1m',max_period1,bots1,lambda bot,df:bot.cancel_trade(df))
        trade_bots(symbol,'5m',max_period5,bots5,lambda bot,df:bot.cancel_trade(df))
        trade_bots(symbol,'15m',max_period15,bots15,lambda bot,df:bot.cancel_trade(df))
        trade_bots(symbol,'30m',max_period30,bots30,lambda bot,df:bot.cancel_trade(df))

        print('Position closed!')
        sys.exit(0)
    except:
        print('Some Error')
    # print('Time:',time()-start)
        # df.info()
        # sleep(3)