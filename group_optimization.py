from single_optimization import optimization
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCde
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
    (3,4,5,10,15,20,30,60,100),
    (10,20,30,40)
]
group = (
    (PTA4_WDDCde,params4),
    (PTA4_WDDCr,params4),
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