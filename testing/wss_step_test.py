from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.OGTA import *

from strategies.work_strategies.LTA import *
from strategies.work_strategies.LTA2 import *
from strategies.work_strategies.GLTA import *
from strategies.work_strategies.PSTA0 import *
from strategies.work_strategies.STA_ml2 import *
from strategies.work_strategies.VSAT import *
from strategies.work_strategies.HelpTA import get_rws


map_wss = {
    'BRQ5_1':(
        (PSTA9_BIRDWATCHER,(67,1.88,2,0.29,1.74,1,1,)),
(PSTA9_GRAVY,(47,2.16,2,0.29,1.21,1,)),

    ),
    'EDU5_1':(
(PSTA9_BIRDWATCHER,(104,1.52,5,0.24,1.04,1,1,)),
(PSTA9_GRAVY,(19,2.86,3,0.01,0.84,1,)),


    ),
    'GZU5_1':(
(PSTA9_BIRDWATCHER,(13,3.18,2,0.25,1.75,1,1,)),
(PSTA9_GRAVY,(25,1.74,2,0.29,0.35,0,)),




    ),
    'IMOEXF_1':(
(PSTA9_BIRDWATCHER,(12,4.36,4,0.21,1.92,1,0,)),
(PSTA9_GRAVY,(9,1.83,2,0.09,0.34,0,)),





    ),
    'MMU5_1':(
(PSTA9_BIRDWATCHER,(24,2.71,5,0.28,0.54,1,1,)),
(PSTA9_GRAVY,(7,1.51,2,0.29,0.55,0,)),



    ),
    'NGN5_1':(
(PSTA9_BIRDWATCHER,(31,2.67,5,0.2,1.35,1,1,)),
(PSTA9_GRAVY,(23,2.27,2,0.29,0.89,1,)),



    ),
    'RMU5_1':(
(PSTA9_BIRDWATCHER,(46,2.6,2,0.27,1.69,1,1,)),
(PSTA9_GRAVY,(27,1.61,3,0.1,1.55,1,)),




    ),
    'SRU5_1':(
(PSTA9_BIRDWATCHER,(21,3.71,2,0.2,1.52,1,1,)),
(PSTA9_GRAVY,(19,2.71,2,0.3,0.37,0,)),



    ),

    # 'UWGN_1':(
    #     (PSTA6_ADVENTURE,(41,2,104,3.0,0,)),
    #     (PSTA6_DUELDODO,(56,2,56,94,0,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'QIWI_1':(
    #     (PSTA6_ADVENTURE,(2,2,139,2.99,1,)),
    #     (PSTA6_SHERIFF,(5,5,2.1,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'APTK_1':(
    #     (PSTA6_DODO,(72,2,57,60,)),
    #     (PSTA6_SHERIFF,(5,8,2.83,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'KZOSP_1':(
    #     (PSTA6_DODO,(45,5,67,66,)),
    #     (PSTA6_PIGEON,(132,5,50,26,14,0.84,3.0,0,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'CBOM_1':(
    #     (PSTA6_ADVENTURE,(28,2,131,2.36,0,)),
    #     (PSTA6_SHERIFF,(37,2,2.74,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'TRMK_1':(
    #     (PSTA6_DUELDODO,(30,6,55,37,0,)),
    #     (PSTA6_DODO,(97,6,48,57,)),
    #     (PSTA6_VULTURE,(93,5,46,67,30,3,0.46,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'SELG_1':(
    #     (PSTA6_SHERIFF,(136,2,2.5,)),
    #     (PSTA6_VULTURE,(53,2,40,112,17,3,0.36,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'GMKN_1':(
    #     (PSTA6_PIGEON,(122,87,31,25,6,0.24,0.54,0,)),
    #     (PSTA6_VULTURE,(101,18,17,101,24,11,0.07,)),
    #     (PSTA6_SHERIFF,(136,35,1.34,)),
    #     (PTA19_YREL,(100,7,16,36,26,2,0)),
    # ),
    # 'VTBR_1':(
    #     (PSTA6_PIGEON,(82,78,124,15,11,0.21,0.68,0,)),
    #     (PSTA6_VULTURE,(67,67,64,99,30,9,0.82,)),
    #     (PSTA6_ADVENTURE,(85,76,119,0.82,1,)),
    #     (PTA19_VALEERA,(100,7,10,30,10,10,0)),
    #     (PTA19_ANUBARAK,(30,10,40,10,10,0)),
    # ),
    # 'MTLR_1':(
    #     (PSTA6_PIGEON,(110,56,35,2,3,0.36,1.07,0,)),
    #     (PSTA6_SHERIFF,(147,59,3.0,)),
    #     (LTA2_DRINKER,(90,2,10,30,10,30,0)),
    #     (PTA19_YREL,(100,7,16,36,26,2,0)),
    # ),
    # 'NMTP_1':(
    #     (PSTA6_ADVENTURE,(99,2,39,2.82,1,)),
    #     (PSTA6_VULTURE,(86,2,63,83,30,10,0.57,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'ROSN_1':(
    #     (PSTA6_PIGEON,(147,127,112,18,2,0.08,0.16,0,)),
    #     (PSTA6_VULTURE,(61,136,15,133,15,4,0.33,)),
    #     (PSTA6_DODO,(39,63,16,61,)),
    #     (PSTA6_SHERIFF,(17,17,2.07,)),
    #     (PSTA6_ADVENTURE,(88,50,50,0.49,0,)),
    #     (LTA2_DRINKER,(110,1.43,15,44,22,26,0)),
    # ),
    # 'FESH_1':(
    #     (PSTA6_SHERIFF,(144,4,1.76,)),
    #     (PSTA6_ADVENTURE,(135,3,11,2.35,1,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    # 'RUAL_1':(
    #     (PSTA6_VULTURE,(150,2,49,93,13,6,0.35,)),
    #     (PSTA6_SHERIFF,(4,4,2.99,)),
    #     (PSTA6_DUELDODO,(127,4,35,37,1,)),
    #     (PSTA6_PIGEON,(150,19,61,28,18,0.36,1.21,0,)),
    #     (PTA21_WHITEMANE,(3,149,10,2,3.0,4,0.0,1)), 
    #     (LTA2_HOTS,(60,2,15,40,10,30,0)),
    # ),
    # 'LSRG_1':(
    #     (PSTA6_ADVENTURE,(11,2,95,2.62,0,)),
    #     (PSTA6_SHERIFF,(10,2,2.61,)),
    #     (PSTA6_PIGEON,(146,2,114,26,2,0.72,2.82,1,)),
    #     (PSTA2_GGD,(60,2,5)),
    # ),
    'default':[

    ]
}
