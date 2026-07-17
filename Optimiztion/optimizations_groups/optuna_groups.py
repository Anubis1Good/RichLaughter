from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.OGTA import *

from strategies.work_strategies.LTA import *
from strategies.work_strategies.LTA2 import *
# from strategies.work_strategies.GLTA import *
from strategies.work_strategies.PSTA0 import *
from strategies.work_strategies.VSAT import *
# from strategies.work_strategies.HelpTA import get_rws

top_limit = 55
group = (
    
    (PTA2_BDDC_FIX,[
        (5,10,top_limit),
        (1,),
        (1,),
    ]),
    (PTA2_BDDCr_UNIVERSAL,[
        (5,10,top_limit),
        (1,),
        (1,),
    ]),
    (PTA2_BBBUr,[
        (5,10,top_limit),
        (1,),
        (1,),
    ]),
    (PTA2_BBBU,[
        (5,10,top_limit),
        (1,),
        (1,),
    ]),
    (PTA2_BVGFIX,[
        (5,10,top_limit),
        (1,),
        (1,),
    ]),
    (PTA10_WIZARD,[
        (5,10,top_limit),
        (5,10,top_limit),
        (2,7,top_limit),
        (10,21,30),
        (20,31,40,50),
    ]),
    (PTA10_MAGIC,[
        (5,10,top_limit),
        (5,10,top_limit),
        (2,7,top_limit),
    ]),
    (PTA11_KUSURUKEN,[
        (5,10,top_limit),
        (2,7,top_limit),
        (2,7,top_limit),
        (11,30,40),
        ('c','hl')
    ]),
    (PTA12_SWDDCr,[
        (5,10,top_limit),
        (11,30,40),
        (0.25,0.5,1),
        (2,7,top_limit),
        (2,7,top_limit),
    ]),
    (PTA13_DWDDCr,[
        (2,7,top_limit),
        (11,30,40),
        (2,7,top_limit),
    ]),
    (PTA14_RWDDCr,[
        (2,7,top_limit),
        (11,30,40),
        (2,7,top_limit),
        (2,7,top_limit),
    ]),
    (PTA14_RANGER,[
        (2,7,top_limit),
        (20,30,40),
        (2,7,top_limit),
        (5,10,15,20,30),
        (21,40,50,60),
        (11,30,40),
    ]),

    (PTA15_VALLA,[
        (2,7,top_limit),
        (0,)
    ]),
    (PTA15_WIDOWMAKER,[
        (2,7,top_limit),
        (20,30,40),
    ]),
    (PTA15_ANNA,[
        (2,7,top_limit),
        (20,30,40),
    ]),

    (OGTA4_DOG,[
        (2,7,top_limit),
        (11,30,40),
    ]),
    (LTA_OKROSHKA,[
        (2,7,top_limit),
        (2,7,top_limit),
    ]),
    (LTA_OKROSHKA2,[
        (2,7,top_limit),
        (2,7,top_limit),
    ]),
    (LTA_PIN,[
        (2,7,top_limit),
        (2,7,top_limit),
        (11,30,40,50),
        (3,4,7)
    ]),

    (PTA4_UNIVERSAL,[
        (2,7,top_limit),
        (2,7,top_limit),
        (11,30,40),
        (11,30,40),
        ["DC","VG","BB","VC","WC"],
        ["rsi","rsi_tw","mfi","s","uo"],
        (1,),
        (1,)
    ]), 

    (PTA18_KELTHUZAD,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (11,20,30,40),
    ]),

    (PTA18_DEHAKA,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (11,20,30,40),
    ]),
    (PTA18_GULDAN,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (11,20,30,40),
    ]),

   
    (PTA19_JOHANNA,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (2,7,top_limit),
        (11,40,50),
        (11,20,30,40),
        (0,1)
    ]),
    (PTA19_TYRAEL,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (2,7,top_limit),
        (11,40,50),
        (11,20,30,40),
        (0,1)
    ]),
    (PTA19_CASSIA,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (2,7,top_limit),
        (11,40,50),
        (11,20,30,40),
        (0,1)
    ]),
    (PTA19_IMPERIUS,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (2,7,top_limit),
        (11,40,50),
        (11,20,30,40),
        (0,1)
    ]),
    (PTA18_BLAZE,[
        (2,7,top_limit),
        (2,7,top_limit),
        (2,7,top_limit),
        (11,40,50),
        (11,20,30,40),
        (0,1)
    ]),
    (PTA19_ANUBARAK,[
        (2,7,top_limit),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30,40),
        (11,20,30,40),
        (0,1)
    ]),
    (LTA2_LOGAN,[
        (2,7,top_limit),
        (2,7,top_limit),
        (11,30,40,50),
    ]),
    (PTA19_YREL,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30,40),
        (0,5,30),
        (0,1)
    ]),
    (PTA19_VALEERA,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30,40),
        (0,5,30),
        (0,1)
    ]),
    (PTA19_ZERATUL,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30,40),
        (0,1)
    ]),
    (PTA18_MISHA,[
        (top_limit,),
        (3,5,7,10),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30,40),
    ]),
    (LTA2_HOTS,[
        (2,7,top_limit),
        (0.5,1,2),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30),
        (0,5,30),
        (0,1)
    ]),
    (LTA2_PUBG,[
        (2,7,top_limit),
        (0.5,1,2),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30),
        (0,5,30),
        (0,1)
    ]),
    (LTA2_DRG,[
        (2,7,top_limit),
        (0.5,1,2),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30),
        (0,5,30),
        (0,1)
    ]),
    (OGTA4_PUPPY,[
        (2,7,top_limit),
        (11,30,40),
        (11,20,30,40),

    ]),
    (LTA2_DRINKER,[
        (2,7,top_limit),
        (0.5,1,2),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30),
        (0,7,30),
        (0,1)
    ]),
    (LTA2_FENNEC,[
        (2,7,top_limit),
        (0.5,1,2,),
        (2,7,top_limit),
        (21,40,50),
        (11,20,30),
        (0,5,30),
        (0.5,1,2),
        (0,1)
    ]),
    (LTA2_ALKASH,[
        (2,7,top_limit),
        (0.5,1,2),
        (2,7,top_limit),
        (0,5,30),
        (0,1)
    ]),
    (LTA2_LYNX,[
        (2,7,top_limit),
        (0.5,1,2),
        (2,7,top_limit),
        (0,5,30),
        (0.5,1,2),
        (0,1)
    ]),
    (PSTA3_HADES,[
        (2,7,top_limit),
        (2,7,top_limit),
        ('std','mean'),
    ]),
    (PSTA2_GGD,[
        (60,),
        (2,3,4,5,7,10,15,30),
        (2,3,4,5,10),
    ]),
    (STA3_LITE, (
        (2,7,top_limit),
        (3,4,10),
        (0.5,1,2),
        (2,6,9),
        (2,7,top_limit),
    )),
    (STA3_FORCE, (
        (2,7,top_limit),
        (3,4,9),
        (1,2,5),
        (2,6,9),
        (2,7,top_limit),
        (11,30,40),
        (11,30,60),
    )),
        (PTA4_U3,(
        (2,7,top_limit),
        (2,7,top_limit),
        (2,7,15),
        (2,7,15),
        ("DC","VG","BB","VC","WC"),
        ("rsi","rsi_tw","mfi","s","uo"),
    )),
    (
        LTA_BIBI, (
            (2,7,top_limit),
            (4,10,15),
            (2,3,5,10,30),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d')
        )
    ),
    (
        LTA_IGOGOSHA, (
            (2,7,top_limit),
            (4,10,15),
            (2,3,5,10,30),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d')
        )
    ),
    (
        LTA_IRONANNY, (
            (2,7,top_limit),
            (4,10,15),
            (2,3,5,10,30),
            (2,4,5,6,7)
        )
    ),
    (
        PTA21_AURIEL,(
            (2,7,top_limit),
            (5,10),
            (2,3,5),
            (1.5,3),
            (3,4,6),
            (0,0.25,0.5),
        )
    ),
    (
        PTA21_WHITEMANE,(
            (2,7,top_limit),
            (2,7,top_limit),
            (5,10),
            (2,3,5),
            (1.5,3),
            (3,4,6),
            (0,0.25,0.5),
            (0,1)
        )
    ),
    # (
    #     PTA22_BERSERK,(
    #         (2,7,top_limit),
    #         (3,5,10),
    #         (2,3,5),
    #         (1,1.5,3,10),
    #         (3,4,6,10),
    #         (0,0.20,0.75),
    #         (2,7,top_limit),
    #         (2,7,top_limit),
    #         (21,40,50,60),
    #         (11,30,60),
    #     )
    # ),
    (PTA14_RENEGADE,[
        (2,7,top_limit),
        (20,30,40),
        (2,7,top_limit),
        (5,10,15,20,30),
        (21,40,50,60),
        (11,30,40),
    ]),
    (OGTA4_HAMSTER,(
        (2,7,top_limit),
        (9,20,40),)
    ),
    (OGTA4_RAT,
       ( (2,7,top_limit),
        (3,5,10,20),
        (2,7,18,30),)
    ),
    (OGTA6_CERBERUS,
       ( (2,7,top_limit),
        (2,7,top_limit),
        (2,7,top_limit),)
    ),
    (OGTA7_PARADOX,
       ( (2,7,top_limit),
        (0.3,1,3),)
    ),
    (PSTA3_REVAN,[
        (2,7,top_limit),
        (2,5,20),
    ]),
    (LTA_CC,[
        (2,7,top_limit),
        (2,5,20),
        (2,5,20),
        (3,5,14),
        (2,5,10),
        (0.5,1,3),
        (0,1),
        (0,1),
    ]),

    (PSTA2_GOOSE,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
    )),
    (PSTA2_DUCK,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
    )),
    (PSTA4_FALCON,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1)
    )),
    (PSTA4_PELICAN,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1)
    )),
    (PTA2_SDDCr,(
        (2,7,top_limit),
        (2,7,top_limit),
    )),
    # (PTA23_ULTIMATUM,(
    #     (2,7,top_limit),
    #     (2,7,top_limit),
    #     (2,7,top_limit),
    #     (2,7,top_limit),
    #     (2,7,top_limit),
    #     (0,1),
    #     (2,7,top_limit),
    #     (1,1.1,10),
    #     (2,7,top_limit),
    #     (0,0.1,1),
    #     (0,0.01,0.1,1),
    #     (0,1)
    # )),
    # (PSTA5_HAWK,(
    #     (2,7,top_limit),
    #     (2,5,30),
    #     (1,2,20),
    #     (2,7,top_limit),
    #     (0,1),
    #     (2,7,top_limit),
    #     (1,1.1,10),
    #     (2,7,top_limit),
    #     (0,0.1,1),
    #     (0,0.01,0.1,1),
    #     (0,1)
    # )),
    (PSTA6_DODO,(
        (2,7,top_limit),
        (2,7,top_limit),
        (10,15,70),
        (10,15,70),
    )),
    (PSTA6_DUELDODO,(
        (2,7,top_limit),
        (2,7,top_limit),
        (10,15,70),
        (2,7,top_limit),
        (0,1)
    )),
    (PSTA6_VULTURE,(
        (2,7,top_limit),
        (2,7,top_limit),
        (10,15,70),
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1)
    )),
    (PSTA6_PIGEON,(
        (2,7,top_limit),
        (2,7,top_limit),
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1),
        (0.1,0.5,3),
        (0,1)
    )),
    (PSTA6_SHERIFF,(
        (2,7,top_limit),
        (2,7,top_limit),
        (0.1,0.5,3),
    )),
    (PSTA6_ADVENTURE,(
        (2,7,top_limit),
        (2,7,top_limit),
        (2,7,top_limit),
        (0.1,0.5,3),
        (0,1)
    )),
    (PSTA7_DODO,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (10,15,70),
        (10,15,70),
    )),
    (PSTA7_DUELDODO,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (10,15,70),
        (2,7,top_limit),
        (0,1)
    )),
    (PSTA7_VULTURE,(
        (2,7,top_limit),
        (10,15,70),
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1)
    )),
    (PSTA7_PIGEON,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (2,5,30),
        (1,2,20),
        (0,0.01,0.1,1),
        (0.1,0.5,3),
        (0,1)
    )),
    (PSTA7_SHERIFF,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (0.1,0.5,3),
    )),
    (PSTA7_ADVENTURE,(
        (2,7,top_limit),
        (2,5,30),
        (1,2,20),
        (0.1,0.5,3),
        (0,1)
    )),
    # (VSAT1_MERCURY,(
    #     (2,5,top_limit),
    #     (0.5,1,20),
    #     (0,0.1,1),
    #     (0.1,0.2,0.5),
    #     (0.5,1,1.1,2),
    #     (0,1),
    #     (0,1),
    #     (0,1),
    # )),
    # (VSAT1_VENUS,(
    #     (60,),
    #     (0.1,0.5,1),
    #     (0,0.1,1),
    #     (0.1,0.2,0.5),
    #     (0.5,1,1.1,2),
    #     (0,1),
    #     (0,1),
    #     (0,1),
    # )),
    (PTA21_MALTHAEL,(
        (2,7,top_limit),
        (2,5,30),
        (2,3,5),
        (0.1,0.5,1),
        (0,1)
    )),
    # (PTA24_BRIGHTWING,(
    #     (2,7,top_limit),
    #     (2,5,30),
    #     (2,3,5),
    #     (0.1,0.5,1),
    #     (0,0.1,1),
    #     (0.1,0.2,0.5),
    #     (0.5,1,1.1,2,10),
    #     (0,1)
    # )),
    # (PTA24_DEATHWING,(
    #     (2,7,top_limit),
    #     (2,5,30),
    #     (2,3,5),
    #     (0.1,0.5,1),
    #     (0,0.1,1),
    #     (0.1,0.2,0.5),
    #     (0.5,1,1.1,2,10),
    #     (0,1)
    # )),
        (PSTA8_AVENGER,(
        (60,),
        (2,3,20),
        (0.1,0.5,1),
        (0,0.1,1),
        (0.1,0.2,0.5),
        (0.5,1,1.1,2,10),
        (0,1)
    )),
    # (PTA25_TASSADAR,(
    #     (2,7,top_limit),
    #     (2,5,30),
    #     (2,3,5),
    #     (0.1,0.5,1),
    #     (0,0.1,1),
    #     (0.1,0.2,0.5),
    #     (0.5,1,1.1,2,10),
    #     (0,5,11,50),
    #     (0,1)
    # )),
    #     (PSTA9_BIRDWATCHER,(
    #     (2,7,top_limit),
    #     (1.5,3,10),
    #     (2,3,5),
    #     (0,0.1,0.3),
    #     (0.25,0.5,2),
    #     (0,1),
    #     (0,1),
    # )),
    # (PSTA9_GRAVY,(
    #     (2,7,top_limit),
    #     (1.5,3,10),
    #     (2,3,5),
    #     (0,0.1,0.3),
    #     (0.25,0.5,2),
    #     (0,1),
    # )),
)

# rev_group = [(get_rws(x[0]),x[1]) for x in group]
# all_group = list(group) + rev_group