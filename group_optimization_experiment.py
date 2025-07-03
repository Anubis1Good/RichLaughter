import os
import traceback
from Optimiztion.Optimizator1 import Optimizator2
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.STA_ca import STA3,STA3_LITE,STA3_FORCE
# from strategies.work_strategies.STA_ml2 import STAML2_TRADITION,STAML2_CHAOS,STAML2_FLUX,STAML2_LEGACY
from strategies.work_strategies.LTA2 import LTA2_DRG
from strategies.work_strategies.PSTA0 import PSTA3_HADES
from strategies.work_strategies.OGTA import OGTA4_PUPPY
from strategies.work_strategies.PTA import PTA2_LISICA
from strategies.work_strategies.PTAX import PTA14_RANGER,PTA14_ANGER,PTA19_CASSIA,PTA19_IMPERIUS

def optimization_multi(ws,ts,params,test_folder,min_fee: float = 0.0004,
    max_fee: float = 0.0012):
    list_dir = os.listdir(test_folder)
    optim = Optimizator2(ws,ts,params,min_fee=min_fee,max_fee=max_fee,need_plot=True)
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
test_folder = 'DataForTests\DataFromMoexFast'
# test_folder = 'DataForTests\DataFromMOEXto5'
min_fee: float = 0.0004
max_fee: float = 0.0012
min_fee = 0.0002
max_fee = 0.0009

group = (
    # (PTA2_LISICA,[
    #     range(10,101,10),
    #     (0.5,1,1.5,2),
    # ]),

    # (PTA19_CASSIA,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,36,5),
    #     range(10,106,20),
    #     (30,40,50),
    #     (10,20,30,40),
    #     (0,1)
    # ]),
    # (PTA19_IMPERIUS,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,36,5),
    #     range(10,106,20),
    #     (30,40,50),
    #     (10,20,30,40),
    #     (0,1)
    # ]),
  
)


if __name__ == '__main__':
    for part in group:
        print(part[0])
        optimization_multi(part[0],ts,part[1],test_folder,min_fee,max_fee)