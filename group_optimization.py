from single_optimization import optimization
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.PTA import PTA2_KOLOBOK,PTA2_UDC,PTA2_ALKASH,PTA8_OBBY,PTA8_FOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA8_OBBY_PF,PTA8_OBBY_VOR,PTA8_OOBBY,PTA8_OOBBY_FREE,PTA8_OOBBY_FREEr
from strategies.work_strategies.LTA import LTA_LAKSA,LTA_LAKSAe
from strategies.work_strategies.OGTA import OGTA3_DS,OGTA3_Rails
from strategies.work_strategies.STA_ca import STA1_LITE
# from strategies.work_strategies.PTA import PTA8_OBBY,PTA8_OBBY_VOR, PTA8_LOBBY,PTA8_OBBY_PF, PTA8_FOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr

test_folder = 'DataForTests\DataFromBitget'
params1 = [
    [3,4] + list(range(5,56,5)),
    (0.5,1,2)
]
params2 = [
    (3,4,5,7,10,15,20,30,40,50,60,80,100)
]
params3 = [
    (3,4,5,6,7,8,9,10,15,20,30,40,50,60,80,100),
    (3,4,5,6,7,8,9,10,15,20,30,40,50,60,80,100)
]
params4 = [
    (3,4,5,10,15,20),
    (0.5,1,2),
    (0.5,),
    (3,4,5,10,15,20)
]
group = (
    (STA1_LITE,params4),
    (PTA2_KOLOBOK,params1),
    (PTA2_UDC,[
        [3,4] + list(range(5,56,5)),
        range(5,50,5)
    ]),
    (PTA2_ALKASH,params2),
    (PTA8_OBBY,params1),
    (PTA8_FOBBY,params1),
    (PTA8_OBBY_FREE,params1),
    (PTA8_OBBY_FREEr,params1),
    (PTA8_OBBY_PF,params1),
    (PTA8_OBBY_VOR,params1),
    (PTA8_OOBBY,params1),
    (PTA8_OOBBY_FREE,params1),
    (PTA8_OOBBY_FREEr,params1),

    

)
# group = (
#     (PTA2_BDDC,params),
#     (PTA2_BDDCde,params),
#     (PTA2_BDDCr,params),
#     (PTA2_DDCr,params),
#     (PTA2_DDCde,params),
# )

for part in group:
    print(part[0])
    optimization(part[0],ts,part[1],test_folder)