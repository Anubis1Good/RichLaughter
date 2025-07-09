import os
import traceback
from Optimiztion.Optimizator1 import Optimizator2
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
test_folder = 'DataForTests\DataFromMoexFastStock'
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
    (
        PTA21_WHITEMANE,(
            (5,10,15,30,60,90),
            (5,10,15,30,60,90),
            (5,10),
            (2,3,5),
            (1.5,3),
            (3,5),
            (0,0.25,0.5),
            (0,1)
        )
    ),
    # (GLTA_BETA,(
    #     range(5,100,5),
    #     range(5,100,10),
    #     range(15,41,5),
    #     ('beta1.json',)
    # )),
    # (GLTA_GAMMA,(
    #     (5,10,15,30,60),
    #     range(10,100,20),
    #     (20,30,40),
    #     range(10,100,20),
    #     range(20,30,40),
    #     range(40,50,60),
    #     ('BP_1751772093.832228.json',)
    # )),

  
)


if __name__ == '__main__':
    for part in group:
        print(part[0])
        optimization_multi(part[0],ts,part[1],test_folder,min_fee,max_fee)