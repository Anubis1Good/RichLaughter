import os
import traceback
from Optimiztion.Optimizator1 import Optimizator2
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.STA_ca import STA2,STA2_FAST,STA2_SLOW,STA2_ULTRA
# from strategies.work_strategies.STA_ml2 import STAML2_TRADITION,STAML2_CHAOS,STAML2_FLUX,STAML2_LEGACY
# from strategies.work_strategies.LTA import LTA_EJIK,LTA_KARYCH,LTA_SAVUNIA,LTA_NUSHA,LTA_KOPATYCH,LTA_LOSYASH,LTA_BARASH,LTA_PIN
# # from strategies.work_strategies.OGTA import OGTA4_DOG
# from strategies.work_strategies.PTA import PTA4_WDDCr2,PTA4_WDDCr2E,PTA1_FEMA,PTA1_FSMA,PTA1_CEMA,PTA1_CSMA
from strategies.work_strategies.PTAX import PTA18_CHOGALL,PTA18_GULDAN,PTA18_ARTAS,PTA18_DEHAKA,PTA18_DIABLO,PTA18_KELTHUZAD,PTA18_REXXAR,PTA18_VARIAN

def optimization_multi(ws,ts,params,test_folder,min_fee: float = 0.0004,
    max_fee: float = 0.0012):
    list_dir = os.listdir(test_folder)
    optim = Optimizator2(ws,ts,params,min_fee=min_fee,max_fee=max_fee)
    for rw in list_dir:
        raw_file = os.path.join(test_folder,rw)
        print(rw)
        try:
            optim.run(raw_file)
        except Exception as err:
            traceback.print_exc()
            print(rw,'not stocks')

test_folder = 'DataForTests\DataFromBitget'
test_folder = 'DataForTests\DataFromMOEX'
# test_folder = 'DataForTests\DataFromMOEXto5'
min_fee: float = 0.0004
max_fee: float = 0.0012
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
    # (PTA18_KELTHUZAD,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_ARTAS,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_CHOGALL,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_DEHAKA,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_DIABLO,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_GULDAN,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    (PTA18_REXXAR,[
        (50,100,200),
        (3,5,7,10),
        range(5,56,5),
        (30,40,50),
        (10,20,30,40),
    ]),
    (PTA18_VARIAN,[
        (50,100,200),
        (3,5,7,10),
        range(5,56,5),
        (10,20,30,40),
        range(10,41,5),
    ]),
    # (STA2,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    # ]),
    # (STA2_FAST,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     range(10,41,5),
    # ]),
    # (STA2_SLOW,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     range(10,41,5),
    # ]),
    # (STA2_ULTRA,[
    #     (50,100,200),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     range(10,41,5),
    # ]),

)

# group = (
#     (PTA2_BDDC,params),
#     (PTA2_BDDCde,params),
#     (PTA2_BDDCr,params),
#     (PTA2_DDCr,params),
#     (PTA2_DDCde,params),
# )
if __name__ == '__main__':
    for part in group:
        print(part[0])
        optimization_multi(part[0],ts,part[1],test_folder,min_fee,max_fee)