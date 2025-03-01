from Bots.TestBot1 import TestBot1
from strategies.work_strategies.PTA import PTA2_DDCde,PTA2_VOLCHARA,PTA2_LISICA,PTA8_LOBSTER,PTA2_BDVCr,PTA2_UDC,PTA2_AUDC,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_OBBY_PF,PTA8_DOBBY_FREE,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR3_User,STAML1_XGBR4,STAML1_XGBR5
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
    (STAML1_XGBR4,(5,5)),
    (STAML1_XGBR5,(60,5)),
    (STAML1_XGBR5,(5,5)),
    (PTA8_DOBBY,(5,0.5)),
    (PTA8_OBBY,(5,0.5)),
    (PTA8_LOBSTER,(4,0.5)),
    (PTA8_OBBY_PF,(5,0.5)),
    (PTA8_DOBBY_FREEr,(4,0.5)),
    (PTA8_DOBBY_FREE,(4,0.5)),
    (PTA2_BDVCr,(10,)),
    (PTA2_UDC,(3,5)),
    (PTA2_AUDC,(3,5)),
    (PTA2_VOLCHARA,(3,2)),
    (PTA2_LISICA,(3,2)),
    (LTA_LAKSAe,(40,3)),
    (LTA_LAKSA,(40,3)),
    (PTA2_DDCde,(5,)),
    (STA1_LITE,(30,1,0.5,15)),
    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA2_DDCrWork,(5,)),
    (PTA4_WDDCr,(60,30)),
    (PTA4_WDDCde,(20,40))
]
# wss = [
#     (STAML1_XGBR5,(60,5)),
#     (STAML1_XGBR5,(5,5))
# ]
print(len(wss))
for WS,conf in wss:
    strategy = WS("DOGEUSDT","5m","usdt-futures",1,*conf)
    bot = TestBot1("DOGEUSDT",strategy,conf)
    bots.append(bot)


while True:
    # print(strategy())
    for bot in bots:
        bot.run()
        sleep(0.1)