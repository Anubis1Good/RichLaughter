from single_optimization import optimization
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.STA_ml import STAML1_PROPHET1s,STAML1_PROPHET2s,STAML1_PROPHET3s
# from strategies.work_strategies.LTA import LTA_APHOBO,LTA_APHOGA
from strategies.work_strategies.PTA import PTA10_MAGIC,PTA6_KAMA,PTA6_KAMA2,PTA6_KAMAZ2,PTA6_KAMA3,PTA6_KAMA4


test_folder = 'DataForTests\DataFromBitget'
params1 = [
    [3,4] + list(range(5,26,5)),
    (0.5,1,2,3)
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

    (STAML1_PROPHET3s,[
        (20,),
        (5,10),
        (0.05,0.1,0.2,0.3)
    ]),

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