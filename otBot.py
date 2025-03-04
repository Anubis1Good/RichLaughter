from Bots.TestBot1 import TestBot1
from strategies.work_strategies.PTA import PTA2_BDDC,PTA2_BDDCde,PTA2_BDDCr,PTA2_DDCde,PTA2_VOLCHARA,PTA2_LISICA,PTA8_LOBSTER,PTA2_BDVCr,PTA2_UDC,PTA2_AUDC,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_OBBY_PF,PTA8_DOBBY_FREE,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_FOBBY,PTA8_LOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA8_OBBY_VOR,PTA9_RAB
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR3_User,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_AXGBR2,STAML1_PROPHET1
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_LAKSA,LTA_LAKSAe,LTA_APHOBO,LTA_APHOGA,LTA_BORSCH,LTA_MISO,LTA_PHOBO,LTA_PHOGA,LTA_RAMEN,LTA_TOMYAM
from time import sleep

bots = []
wss = [
    (STAML1_XGBR2,(60,5)),
    (STAML1_XGBR2,(5,5)),
    (STAML1_AXGBR2,(5,5)),
    (STAML1_AXGBR2,(60,5)),
    (STAML1_XGBR4,(60,5)),
    (STAML1_XGBR5,(60,5)),
    (STAML1_XGBR6,(60,5)),
    (STAML1_XGBR7,(60,5)),
    (STAML1_XGBR8,(60,5)),
    (STAML1_PROPHET1,(60,5)),

    (STA1_LITE,(10,2,0.5,20)),

    (PTA2_BDVCr,(4,)),
    (PTA2_BDDC,(10,)),
    (PTA2_BDDCde,(10,)),
    (PTA2_BDDCr,(5,)),
    (PTA2_UDC,(15,40)),
    (PTA2_AUDC,(15,40)),
    (PTA2_VOLCHARA,(20,1.5)),
    (PTA2_ZAYAC,(40,0.5)),
    (PTA2_LISICA,(20,2)),
    (PTA2_KOLOBOK,(5,0.5)),
    (PTA2_DDCde,(4,)),
    (PTA2_DDCrVG,(30,)),
    (PTA2_DVCr,(15,)),
    (PTA2_DDCrWork,(5,)),
    (PTA4_WDDCr,(20,20)),
    (PTA4_WDDCde,(30,40)),

    (PTA8_DOBBY,(5,1)),
    (PTA8_DOBBY_FREEr,(5,2.5)),
    (PTA8_OBBY,(10,0.5)),
    (PTA8_OBBY_FREEr,(50,0.5)),
    (PTA8_LOBSTER,(3,0.5)),
    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA9_RAB,(10,2,5,0.5)),

    (LTA_LAKSAe,(15,6)),
    (LTA_LAKSA,(20,6)),
    (LTA_APHOBO,(15,1)),
    (LTA_APHOGA,(15,1)),
    (LTA_BORSCH,(10,10)),
    (LTA_MISO,(52,9,26,52,14,12,26,9)),
    (LTA_PHOBO,(15,1)),
    (LTA_PHOGA,(15,1)),
    (LTA_RAMEN,(50,3)),
    (LTA_TOMYAM,(50,)),


]
# wss = [
#     (STAML1_LR1,(60,5)),
# ]
print(len(wss))
for WS,conf in wss:
    strategy = WS("DOGEUSDT","1m","usdt-futures",1,*conf)
    bot = TestBot1("DOGEUSDT",strategy,conf)
    bots.append(bot)


while True:
    # print(strategy())
    for bot in bots:
        bot.run()
        sleep(0.1)