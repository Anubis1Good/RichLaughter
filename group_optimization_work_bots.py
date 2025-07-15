import os
import traceback
from Optimiztion.Optimizator1 import Optimizator2
from strategies.test_strategies.universal import universal_test_strategy as ts

from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.OGTA import *

from strategies.work_strategies.LTA import *
from strategies.work_strategies.LTA2 import *
from strategies.work_strategies.GLTA import *
from strategies.work_strategies.PSTA0 import *


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
# test_folder = 'DataForTests\otherMOEX'
min_fee: float = 0.0004
max_fee: float = 0.0012
# min_fee = 0.0002
# max_fee = 0.0009

old_group = (
    # (STA2,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    # ]),
    # (STA2_FAST,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     range(10,41,5),
    # ]),
    # (STA2_SLOW,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     range(10,41,5),
    # ]),
    # (STA2_ULTRA,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     range(10,41,5),
    # ]),
    # (STA_mini,[
    #     range(10,101,10),
    #     (0,1)
    # ]),
    # (PTA15_KERRIGAN,[
    #     range(10,101,10),
    # ]),
    # (PTA15_TRACER,[
    #     range(10,101,10),
    #     (0,)
    # ]),
    # (PTA15_SILVANA,[
    #     range(10,101,10),
    #     (20,30,40),
    #     range(10,101,10),
    # ]),
    # (PTA4_UNIVERSAL2,[
    #     range(10,61,10),
    #     range(5,61,5),
    #     (20,30,40,50),
    #     (20,30,40,50),
    #     ["DC","VG","BB","VC","WC"],
    #     ["rsi","rsi_tw","mfi","s","uo"],
    #     (1,),
    #     (1,)
    # ]), 
    # (PTA18_ARTAS,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_CHOGALL,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_DIABLO,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    # ]),
    # (PTA18_REXXAR,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (30,40,50),
    #     (10,20,30,40),
    # ]),
    # (PTA18_VARIAN,[
    #     (100,),
    #     (3,5,7,10),
    #     range(5,56,5),
    #     (10,20,30,40),
    #     range(10,41,5),
    # ]),
    # (PSTA3_ZEUS,[
    #     range(10,100,10),
    #     range(2,20,2),
    #     ('std','mean'),
    # ]),
    # (PTA20_HOGGER, (
    #     (30,60,90,120,150),
    #     (5,10,15,30,45,60),
    #     (0.5,1,2),
    #     (0.5,1,2),
    #     (20,30,40,50),
    #     (10,20,30,40)
    # )
    #  ),
    # (PTA20_HANZO, (
    #     (30,60,90,120,150),
    #     (5,10,15,30,45,60),
    #     (0.5,1,2),
    #     (0.5,1,2),
    # )
    #  ),
    #     (GLTA_BETA,(
    #     range(5,100,5),
    #     range(5,100,10),
    #     range(15,41,5),
    #     ('beta1.json',)
    # )),
)

group = (
    
    (PTA2_BDDC_FIX,[
        range(10,101,10),
        (1,),
        (1,),
    ]),
    (PTA2_BDDCr_UNIVERSAL,[
        range(10,101,10),
        (1,),
        (1,),
    ]),
    (PTA2_BBBUr,[
        range(10,101,10),
        (1,),
        (1,),
    ]),
    (PTA2_BBBU,[
        range(10,101,10),
        (1,),
        (1,),
    ]),
    (PTA2_BVGFIX,[
        range(10,101,10),
        (1,),
        (1,),
    ]),
    (PTA2_DDCrWork,[
        range(10,101,10),
    ]),
    (PTA2_DDCrVG,[
        range(10,101,10),
    ]),
    (PTA2_DVCr,[
        range(10,101,10),
    ]),
    (PTA2_LISICA,[
        range(10,101,10),
        (0.5,1,1.5,2),
    ]),
    (PTA2_VOLCHARA,[
        range(10,101,10),
        (0.5,1,1.5,2),
    ]), 

    (PTA10_WIZARD,[
        range(10,101,10),
        range(10,101,10),
        range(3,16,3),
        (20,30),
        (20,30,40,50),
    ]),
    (PTA10_MAGIC,[
        range(10,101,10),
        range(10,101,10),
        range(3,16,3),
    ]),
    (PTA11_KUSURUKEN,[
        range(10,101,10),
        range(3,16,3),
        range(5,36,5),
        (20,30,40),
        ('c','hl')
    ]),
    (PTA12_SWDDCr,[
        range(10,101,10),
        (20,30,40),
        (0.25,0.5,1),
        range(5,16,5),
        range(5,26,5),
    ]),
    (PTA13_DWDDCr,[
        range(10,101,10),
        (20,30,40),
        range(10,101,10),
    ]),
    (PTA14_RWDDCr,[
        range(10,101,10),
        (20,30,40),
        range(10,101,10),
        range(10,101,10),
    ]),
    (PTA14_RANGER,[
        range(10,200,30),
        (20,30,40),
        range(10,200,30),
        (5,10,15,20,30),
        (30,40,50,60),
        (20,30,40),
    ]),
    (PTA14_ANGER,[
        range(10,200,30),
        range(10,200,30),
        (5,10,15,20,30),
        (30,40,50,60),
        (20,30,40),
    ]),

    (PTA15_VALLA,[
        range(10,101,10),
        (0,)
    ]),
    (PTA15_WIDOWMAKER,[
        range(10,101,10),
        (20,30,40),
    ]),
    (PTA15_ANNA,[
        range(10,101,10),
        (20,30,40),
    ]),

    (OGTA4_DOG,[
        range(10,101,10),
        (20,30,40),
    ]),
    (LTA_OKROSHKA,[
        range(10,101,10),
        range(10,101,10),
    ]),
    (LTA_OKROSHKA2,[
        range(10,101,10),
        range(10,101,10),
    ]),
    (LTA_PIN,[
        range(10,101,10),
        range(3,16,3),
        (20,30,40,50),
        (3,5)
    ]),

    (PTA4_UNIVERSAL,[
        range(10,61,10),
        range(10,61,10),
        (20,30,40),
        (20,30,40),
        ["DC","VG","BB","VC","WC"],
        ["rsi","rsi_tw","mfi","s","uo"],
        (1,),
        (1,)
    ]), 

    (PTA18_KELTHUZAD,[
        (100,),
        (3,5,7,10),
        range(5,56,5),
        (10,20,30,40),
    ]),

    (PTA18_DEHAKA,[
        (100,),
        (3,5,7,10),
        range(5,56,5),
        (10,20,30,40),
    ]),
    (PTA18_GULDAN,[
        (100,),
        (3,5,7,10),
        range(5,56,5),
        (10,20,30,40),
    ]),

   
    (PTA19_JOHANNA,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        range(10,106,20),
        (30,40,50),
        (10,20,30,40),
        (0,1)
    ]),
    (PTA19_TYRAEL,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        range(10,106,20),
        (30,40,50),
        (10,20,30,40),
        (0,1)
    ]),
    (PTA19_CASSIA,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        range(10,106,20),
        (30,40,50),
        (10,20,30,40),
        (0,1)
    ]),
    (PTA19_IMPERIUS,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        range(10,106,20),
        (30,40,50),
        (10,20,30,40),
        (0,1)
    ]),
    (PTA18_BLAZE,[
        range(10,106,20),
        range(5,36,5),
        range(11,106,15),
        (30,40,50),
        (10,20,30,40),
        (0,1)
    ]),
    (PTA19_ANUBARAK,[
        range(10,106,20),
        range(5,36,5),
        (30,40,50),
        (10,20,30,40),
        (10,20,30,40),
        (0,1)
    ]),
    (LTA2_LOGAN,[
        range(10,106,10),
        range(10,106,15),
        (20,30,40,50),
    ]),
    (PTA19_YREL,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        (30,40,50),
        (10,20,30,40),
        range(0,31,10),
        (0,1)
    ]),
    (PTA19_VALEERA,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        (30,40,50),
        (10,20,30,40),
        range(0,31,10),
        (0,1)
    ]),
    (PTA19_ZERATUL,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        range(10,106,20),
        (30,40,50),
        (10,20,30,40),
        (0,1)
    ]),
    (PTA18_MISHA,[
        (100,),
        (3,5,7,10),
        range(5,36,5),
        (30,40,50),
        (10,20,30,40),
    ]),
    (LTA2_HOTS,[
        (60,90,150),
        (0.5,1,2),
        range(5,36,5),
        (30,40,50),
        (10,20,30),
        range(0,31,10),
        (0,1)
    ]),
    (LTA2_PUBG,[
        (60,90,150),
        (0.5,1,2),
        range(5,36,5),
        (30,40,50),
        (10,20,30),
        range(0,31,10),
        (0,1)
    ]),
    (LTA2_DRG,[
        (60,90,150),
        (0.5,1,2),
        range(5,36,5),
        (30,40,50),
        (10,20,30),
        range(0,31,10),
        (0,1)
    ]),
    (OGTA4_PUPPY,[
        range(5,66,5),
        (20,30,40),
        (10,20,30,40),

    ]),
    (LTA2_DRINKER,[
        (60,90,150),
        (0.5,1,2),
        range(5,36,5),
        (30,40,50),
        (10,20,30),
        range(0,31,10),
        (0,1)
    ]),
    (LTA2_FENNEC,[
        (150,),
        (2,),
        range(5,36,5),
        (30,40,50),
        (10,20,30),
        range(0,31,10),
        (0.5,1,2),
        (0,1)
    ]),
    (LTA2_ALKASH,[
        (60,90,150),
        (0.5,1,2),
        range(5,36,5),
        range(0,31,10),
        (0,1)
    ]),
    (LTA2_LYNX,[
        (60,90,150),
        (0.5,1,2),
        range(5,36,5),
        range(0,31,10),
        (0.5,1,2),
        (0,1)
    ]),
    (PSTA3_HADES,[
        range(10,100,10),
        range(2,20,2),
        ('std','mean'),
    ]),
    (PSTA2_GGD,[
        (60,),
        (2,3,4,5,7,10,15,30),
        (2,3,4,5,10),
    ]),
    (STA3_LITE, (
        (10,60,90),
        (3,6),
        (0.5,1,2),
        (6,9),
        (10,30,60),
    )),
    (STA3_FORCE, (
        (90,60,20,10),
        (3,9),
        (2,1),
        (9,6),
        (90,60,10),
        (20,30,40),
        (10,30,60),
    )),
        (PTA4_U3,(
        (5,10,15,30,60,90),
        (5,10,15,30,60,90),
        (5,10),
        (2,3,5),
        ("DC","VG","BB","VC","WC"),
        ("rsi","rsi_tw","mfi","s","uo"),
    )),
    (
        LTA_BIBI, (
            (5,10,15,30,60,90),
            (5,10,15),
            (2,3,5,10,30),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d')
        )
    ),
    (
        LTA_IGOGOSHA, (
            (5,10,15,30,60,90),
            (5,10,15),
            (2,3,5,10,30),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d')
        )
    ),
    (
        LTA_IRONANNY, (
            (5,10,15,30,60,90),
            (5,10,15),
            (2,3,5,10,30),
            (3,4,5,6,7)
        )
    ),
    (
        PTA21_AURIEL,(
            (5,10,15,30,60,90),
            (5,10),
            (2,3,5),
            (1.5,3),
            (3,5),
            (0,0.25,0.5),
        )
    ),
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
)

if __name__ == '__main__':
    for part in group:
        print(part[0])
        optimization_multi(part[0],ts,part[1],test_folder,min_fee,max_fee)