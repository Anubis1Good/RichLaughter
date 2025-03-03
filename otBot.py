from Bots.TestBot1 import TestBot1
from strategies.work_strategies.PTA import PTA2_BDDC,PTA2_BDDCde,PTA2_BDDCr,PTA2_DDCde,PTA2_VOLCHARA,PTA2_LISICA,PTA8_LOBSTER,PTA2_BDVCr,PTA2_UDC,PTA2_AUDC,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_OBBY_PF,PTA8_DOBBY_FREE,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_FOBBY,PTA8_LOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA8_OBBY_VOR,PTA9_RAB
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR3_User,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_LAKSA,LTA_LAKSAe
from time import sleep

bots = []
wss = [
    (STAML1_XGBR2,(60,5)),
    (STAML1_XGBR2,(5,5)),
    (STAML1_XGBR3_User,(60,5)),
    (STAML1_XGBR3_User,(5,5)),
    (STAML1_XGBR4,(60,5)),
    (STAML1_XGBR5,(60,5)),
    (STAML1_XGBR6,(60,5)),
    (STAML1_XGBR7,(60,5)),
    (STAML1_XGBR8,(60,5)),
    (PTA8_DOBBY,(5,1)),
    (PTA8_DOBBY_FREEr,(15,0.5)),
    (PTA8_DOBBY_FREE,(15,1)),
    (PTA8_OBBY,(5,1)),
    (PTA8_OBBY_FREE,(5,1)),
    (PTA8_OBBY_FREEr,(5,1)),
    (PTA8_OBBY_PF,(5,0.5)),
    (PTA8_OBBY_VOR,(10,1)),
    (PTA8_FOBBY,(10,0.5)),
    (PTA8_LOBBY,(10,0.5)),
    (PTA8_LOBSTER,(10,0.5)),
    (PTA2_BDVCr,(10,)),
    (PTA2_BDDC,(10,)),
    (PTA2_BDDCde,(10,)),
    (PTA2_BDDCr,(5,)),
    (PTA2_UDC,(15,20)),
    (PTA2_AUDC,(15,20)),
    (PTA2_VOLCHARA,(3,1.5)),
    (PTA2_ZAYAC,(3,1.5)),
    (PTA2_LISICA,(3,2)),
    (PTA2_KOLOBOK,(3,2)),
    (LTA_LAKSAe,(40,3)),
    (LTA_LAKSA,(40,3)),
    (STA1_LITE,(60,1,0.5,15)),
    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA9_RAB,(5,2,20,0.5)),
    (PTA2_DDCde,(15,)),
    (PTA2_DDCrVG,(15,)),
    (PTA2_DVCr,(15,)),
    (PTA2_DDCrWork,(10,)),
    (PTA4_WDDCr,(10,40)),
    (PTA4_WDDCde,(20,40))
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