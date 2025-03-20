from single_optimization import optimization
from strategies.test_strategies.universal import universal_test_strategy as ts

# from strategies.work_strategies.STA_ml import STAML1_PROPHET1s,STAML1_PROPHET2s,STAML1_PROPHET3s
from strategies.work_strategies.LTA import LTA_EJIK,LTA_KARYCH,LTA_SAVUNIA,LTA_NUSHA,LTA_KOPATYCH,LTA_LOSYASH,LTA_BARASH,LTA_PIN
# from strategies.work_strategies.OGTA import OGTA4_DOG
from strategies.work_strategies.PTA import PTA4_WDDCr2,PTA4_WDDCr2E
from strategies.work_strategies.PTAX import PTA10_WIZARD


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

    (LTA_EJIK,[
        range(10,66,5),
        range(3,10,1),
        range(5,31,5),
    ]),
    (PTA4_WDDCr2,[
        range(5,66,5),
        range(5,36,5),
    ]),
    (PTA4_WDDCr2E,[
        range(5,66,5),
        range(5,36,5),
    ]),
    (LTA_KARYCH,[
        range(5,66,5),
        range(5,36,5),
    ]),
    (LTA_SAVUNIA,[
        range(5,66,5),
        range(5,36,5),
    ]),
    (LTA_NUSHA,[
        range(5,66,5),
        range(5,36,5),
    ]),
    (LTA_KOPATYCH,[
        range(5,66,5),
        range(30,66,5),
    ]),
    (LTA_LOSYASH,[
        range(5,66,5),
        range(30,66,5),
    ]),
    (LTA_BARASH,[
        range(5,66,5),
        range(10,66,5),
    ]),
    (LTA_PIN,[
        range(10,66,10),
        range(3,10,2),
        range(5,56,5),
        range(3,8,2),
    ]),

    (PTA10_WIZARD,[
        range(10,61,10),
        range(5,66,10),
        range(3,13,3),
        range(5,31,5),
        range(10,41,10),
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