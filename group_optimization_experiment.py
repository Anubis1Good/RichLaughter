import os
import traceback
from Optimiztion.Optimizator1 import Optimizator2,Optimizator3
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.STA_ca import *
# from strategies.work_strategies.STA_ml2 import STAML2_TRADITION,STAML2_CHAOS,STAML2_FLUX,STAML2_LEGACY
from strategies.work_strategies.LTA import *
from strategies.work_strategies.LTA2 import *
from strategies.work_strategies.PSTA0 import *
from strategies.work_strategies.OGTA import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.GLTA import *

def optimization_multi(ws,ts,params,test_folder,min_fee: float = 0.0004,
    max_fee: float = 0.0012):
    list_dir = os.listdir(test_folder)
    need_plot=False
    # need_plot=True
    optim = Optimizator2(ws,ts,params,min_fee=min_fee,max_fee=max_fee,need_plot=need_plot)
    # optim = Optimizator3(ws,ts,params,min_fee=min_fee,max_fee=max_fee,need_plot=need_plot)
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
# test_folder = 'DataForTests\DataFromMoexFastStock'
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

    # (GLTA2_BETA,(
    #     (5,10,100),
    #     (5,10,100),
    #     (10,16,30,45),
    #     ('GA_beta2_1.json','Q_beta2_000.json','Q_beta2_001.json','Q_beta2_002.json','QGA10_beta2_001.json','QGA20_beta2_001.json')
    # )),
    # (GLTA2_GAMMA,(
    #     (5,10,15,30,60,100),
    #     (5,10,15,30,60,100),
    #     (10,25,41),
    #     (5,10,15,30,60,100),
    #     (20,30,42),
    #     (30,50,61),
    #     ('gamma2.json','LP_1752353219.json')
    # )),
    # (
    #     PTA21_AURIEL,(
    #         (2,7,150),
    #         (5,10),
    #         (2,3,5),
    #         (1.5,3),
    #         (3,4,6),
    #         (0,0.25,0.5),
    #     )
    # ),
    # (
    #     PTA21_WHITEMANE,(
    #         (2,7,150),
    #         (2,7,150),
    #         (5,10),
    #         (2,3,5),
    #         (1.5,3),
    #         (3,4,6),
    #         (0,0.25,0.5),
    #         (0,1)
    #     )
    # ),
    # (
    #     PTA22_BERSERK,(
    #         (2,7,150),
    #         (3,5,10),
    #         (2,3,5),
    #         (1,1.5,3,10),
    #         (3,4,6,10),
    #         (0,0.20,0.75),
    #         (2,7,150),
    #         (2,7,150),
    #         (21,40,50,60),
    #         (11,30,60),
    #     )
    # ),


    # (LTA_CC,[
    #     (2,7,150),
    #     (2,5,20),
    #     (2,5,20),
    #     (3,5,14),
    #     (2,5,10),
    #     (0.5,1,3),
    #     (0,1),
    #     (0,1),
    # ]),
    (PSTA6_DODO,(
        (2,7,150),
        (2,7,150),
        (10,15,70),
        (10,15,70),
    )),
    (PSTA6_DUELDODO,(
        (2,7,150),
        (2,7,150),
        (10,15,70),
        (2,7,150),
        (0,1)
    )),
    (PSTA6_VULTURE,(
        (2,7,150),
        (2,7,150),
        (10,15,70),
        (2,7,150),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1)
    )),
    (PSTA6_PIGEON,(
        (2,7,150),
        (2,7,150),
        (2,7,150),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1),
        (0.1,0.5,3),
        (0,1)
    )),
    (PSTA6_SHERIFF,(
        (2,7,150),
        (2,7,150),
        (0.1,0.5,3),
    )),
    (PSTA6_ADVENTURE,(
        (2,7,150),
        (2,7,150),
        (2,7,150),
        (0.1,0.5,3),
        (0,1)
    )),
)


if __name__ == '__main__':
    for part in group:
        print(part[0])
        optimization_multi(part[0],ts,part[1],test_folder,min_fee,max_fee)