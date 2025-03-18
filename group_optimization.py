from single_optimization import optimization
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.STA_ml import STAML1_PROPHET1s,STAML1_PROPHET2s,STAML1_PROPHET3s
from strategies.work_strategies.LTA import LTA_OKROSHKA,LTA_KROSH
from strategies.work_strategies.OGTA import OGTA4_DOG
from strategies.work_strategies.PTA import PTA4_WDDCde,PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr


# test_folder = 'DataForTests\DataFromBitget'
test_folder = 'DataForTests\DataFromMOEX'
# min_fee: float = 0.0004
# max_fee: float = 0.0012
min_fee = 0.0002
max_fee = 0.0009
# params1 = [
#     [3,4] + list(range(5,26,5)),
#     (0.5,1,2,3)
# ]
# params2 = [
#     (3,4,5,7,10,15,20,30,40,50,60,80,100)
# ]
# params3 = [
#     (3,4,5,6,7,8,9,10,15,20,30,40,50,60,80,100),
#     (3,4,5,6,7,8,9,10,15,20,30,40,50,60,80,100)
# ]
# params4 = [
#     (3,4,5,10,15,20,30,60,100),
#     (10,20,30,40)
# ]
group = (

    (LTA_KROSH,[
        range(5,66,5),
        range(5,41,5),
    ]),
    (LTA_OKROSHKA,[
        range(5,66,5),
        range(5,66,5),
    ]),
    (OGTA4_DOG,[
        range(5,66,5),
        range(5,41,5),
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
    optimization(part[0],ts,part[1],test_folder,min_fee,max_fee)