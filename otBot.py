from Bots.TestBot1 import TestBot1,TestMarketBot1
from request_functions.download_bitget import get_df
from strategies.work_strategies.PTA import PTA2_BDDC,PTA2_BDDCde,PTA2_BDDCr,PTA2_DDCde,PTA2_VOLCHARA,PTA2_LISICA,PTA8_LOBSTER,PTA2_BDVCr,PTA2_UDC,PTA2_AUDC,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_OBBY_PF,PTA8_DOBBY_FREE,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_FOBBY,PTA8_LOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA8_OBBY_VOR,PTA9_RAB
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR3_User,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_AXGBR2,STAML1_PROPHET1
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_LAKSA,LTA_LAKSAe,LTA_APHOBO,LTA_APHOGA,LTA_BORSCH,LTA_MISO,LTA_PHOBO,LTA_PHOGA,LTA_RAMEN,LTA_TOMYAM
from time import sleep

bots = []
wss = [

    (STA1_LITE,(10,2,0.5,20)),

    (PTA2_BDVCr,(4,)), #S
    (PTA2_DVCr,(4,)),
    (PTA2_BDDC,(10,)),
    (PTA2_BDDCde,(5,)),
    (PTA2_DDCde,(5,)),
    (PTA4_WDDCde,(30,40)), #S
    (PTA2_BDDCr,(5,)),
    (PTA2_DDCrWork,(5,)),
    (PTA4_WDDCr,(5,30)), #C
    (PTA2_DDCrVG,(5,)),
    (PTA2_UDC,(15,40)),
    (PTA2_AUDC,(15,40)),
    (PTA2_VOLCHARA,(3,2)),
    (PTA2_ZAYAC,(3,2)), #A
    (PTA2_LISICA,(3,2)),
    (PTA2_KOLOBOK,(3,2)), #A

    (PTA8_DOBBY,(4,0.5)),
    (PTA8_OBBY,(4,0.5)), #S
    (PTA8_DOBBY_FREEr,(4,0.5)),
    (PTA8_OBBY_FREEr,(4,0.5)), #S
    (PTA8_LOBSTER,(3,0.5)), #S
    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA9_RAB,(10,2,5,0.5)),

    (LTA_LAKSAe,(40,3)),
    (LTA_LAKSA,(7,3)),
    (LTA_APHOBO,(3,2)),
    (LTA_APHOGA,(10,1)),
    (LTA_BORSCH,(3,3)),
    (LTA_MISO,(52,9,26,52,14,12,26,9)),
    (LTA_PHOBO,(3,2)),
    (LTA_PHOGA,(4,2)),
    (LTA_RAMEN,(50,3)),
    (LTA_TOMYAM,(50,)),

    (STAML1_XGBR2,(60,5)), #S
    (STAML1_XGBR2,(5,5)), #S
    (STAML1_AXGBR2,(5,5)),
    (STAML1_AXGBR2,(60,5)),
    (STAML1_XGBR4,(60,5)),
    (STAML1_XGBR5,(60,5)),
    (STAML1_XGBR6,(60,5)),
    (STAML1_XGBR7,(60,5)),
    (STAML1_XGBR8,(60,5)),
    (STAML1_PROPHET1,(60,5)),

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
    # print(strategy())
    df = get_df(symbol,granularity,productType,limit)
    for bot in bots:
        bot.run(df)
        # sleep(0.1)