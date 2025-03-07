from Bots.TestBot1 import TestBot1,TestMarketBot1
from request_functions.download_bitget import get_df
from strategies.work_strategies.PTA import PTA2_BDDC,PTA2_BDDCde,PTA2_BDDCr,PTA2_DDCde,PTA2_VOLCHARA,PTA2_LISICA,PTA8_LOBSTER,PTA2_BDVCr,PTA2_UDC,PTA2_AUDC,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_OBBY_PF,PTA8_DOBBY_FREE,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_FOBBY,PTA8_LOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA8_OBBY_VOR,PTA9_RAB,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA10_MAGIC,PTA6_KAMA,PTA6_KAMA2,PTA6_KAMAZ2
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_PROPHET1,STAML1_XGBR2_DC,STAML1_XGBR2_DCh,STAML1_XGBR2e,STAML1_XGBR2h,STAML1_XGBR2he,STAML1_ARIMAS1,STAML1_PROPHET2s,STAML1_PROPHET3s,STAML1_PROPHET1s,STAML1_PROPHET2,STAML1_PROPHET3
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_LAKSA,LTA_LAKSAe,LTA_APHOBO,LTA_APHOGA,LTA_BORSCH,LTA_MISO,LTA_PHOBO,LTA_PHOGA,LTA_RAMEN,LTA_TOMYAM
from time import sleep,time

bots = []
wss = [

    (STA1_LITE,(10,2,0.5,20)),

    (PTA2_DVCr,(10,)),
    (PTA2_DDCde,(20,)),
    (PTA2_DDCrWork,(10,)),
    (PTA2_DDCrVG,(10,)),
    (PTA2_ZAYAC,(7,2)), #A
    (PTA2_LISICA,(7,2)),

    (PTA4_WDVCr,(10,)),
    (PTA4_WDDCde,(20,30)), #S
    (PTA4_WDDCr,(10,30)), #C
    (PTA4_WDDCrE,(10,30)), #C
    (PTA4_WDDCrVG,(10,30)),
    (PTA4_WLISICA,(7,2,30)),

    (PTA6_KAMA,(5,20)),
    (PTA6_KAMA2,(5,5,21,50)),
    (PTA6_KAMAZ2,(5,20,21,50)),

    (PTA8_DOBBY,(7,0.5)),
    (PTA8_OBBY,(7,0.5)), #S
    (PTA8_DOBBY_FREEr,(7,0.5)),
    (PTA8_WDOBBY_FREEr,(7,0.5,30)),
    (PTA8_OBBY_FREEr,(7,0.5)), #S
    (PTA8_LOBSTER,(15,0.5)), #S

    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA9_RAB,(10,2,5,0.5)),
    (PTA10_MAGIC,(95,20,4)),

    (LTA_APHOBO,(10,1)),
    (LTA_APHOGA,(10,1)),
    (LTA_BORSCH,(3,3)),
    (LTA_MISO,(52,9,26,52,14,12,26,9)),
    (LTA_PHOBO,(3,2)),
    (LTA_PHOGA,(4,2)),
    (LTA_RAMEN,(50,3)),
    (LTA_TOMYAM,(50,)),

    (STAML1_XGBR2,(100,5)), #S
    (STAML1_XGBR2,(5,5)), #S
    (STAML1_XGBR2e,(5,5)), #S
    (STAML1_XGBR2he,(5,5)), #S
    (STAML1_XGBR2h,(5,5)), #S
    (STAML1_XGBR2_DC,(5,5)), #S
    (STAML1_XGBR2_DCh,(5,5)), #S
    (STAML1_XGBR4,(100,5)),
    (STAML1_XGBR5,(100,5)),
    (STAML1_XGBR6,(100,5)),
    (STAML1_XGBR7,(100,5)),
    (STAML1_XGBR8,(100,5)),
    (STAML1_PROPHET1,(60,20)),
    (STAML1_PROPHET1s,(60,20)),
    (STAML1_PROPHET2,(5,20)),
    (STAML1_PROPHET2s,(5,20)),
    (STAML1_PROPHET3,(20,20,0.05)),
    (STAML1_PROPHET3s,(20,20,0.05)),
    (STAML1_ARIMAS1,(20,(2, 1, 2),10,0.1)),

]
# wss = [
#     (STAML1_LR1,(60,5)),
# ]
max_period = max(list(map(lambda x: x[1][0],wss)))
print('Ботов:',len(wss))
print('Max period:',max_period)
symbol = "DOGEUSDT"
granularity = "5m"
productType = "usdt-futures"
n_parts = 1
limit = (max_period+1)*3
for WS,conf in wss:
    strategy = WS(symbol,granularity,productType,n_parts,*conf)
    # bot = TestBot1("DOGEUSDT",strategy,conf)
    bot = TestMarketBot1("DOGEUSDT",strategy,conf)
    bots.append(bot)


while True:
    # start = time()
    # print(strategy())
    df = get_df(symbol,granularity,productType,limit)
    for bot in bots:
        df_c = df.copy()
        bot.run(df_c)
    # print('Time:',time()-start)
        # df.info()
        # sleep(3)