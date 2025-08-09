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
(PTA24_DEATHWING,(92,11,2,0.32,0.02,0.2,4.54,0,)),
(PTA21_MALTHAEL,(15,15,4,0.7,0,)),

(PTA24_BRIGHTWING,(95,12,3,0.12,0.03,0.19,3.19,1,)),


    ),
    'EDU5_1':(

    ),
    'GZU5_1':(
(PTA24_DEATHWING,(49,26,2,0.56,0.88,0.47,8.26,0,)),

(PTA24_BRIGHTWING,(31,17,2,0.13,0.28,0.27,0.82,0,)),
(PTA21_MALTHAEL,(27,29,2,0.21,0,)),


    ),
    'IMOEXF_1':(
(PTA21_MALTHAEL,(27,12,2,0.8,0,)),
(PTA24_DEATHWING,(30,12,4,0.18,0.36,0.31,7.84,0,)),

(PTA24_BRIGHTWING,(88,13,2,0.61,0.08,0.46,0.98,0,)),


    ),
    'MMU5_1':(
(PTA21_MALTHAEL,(27,29,2,0.84,0,)),
(PTA24_DEATHWING,(35,14,2,0.22,0.42,0.22,0.95,0,)),

(PTA24_BRIGHTWING,(34,27,2,0.1,0.44,0.32,0.52,1,)),
(VSAT1_VENUS,(60,0.16,0.94,0.23,7.33,0,0,0,)),

    ),
    'NGN5_1':(
(PTA21_MALTHAEL,(73,16,2,0.14,0,)),

        (PTA24_BRIGHTWING,(73,24,2,0.54,0.79,0.49,5.98,1,)),
(VSAT1_VENUS,(60,0.91,0.04,0.49,9.02,0,1,1,)),
(PTA24_DEATHWING,(77,17,2,0.55,0.43,0.47,5.94,0,)),

    ),
    'RMU5_1':(

(VSAT1_VENUS,(60,0.5,0.17,0.26,7.19,0,1,0,)),
(PTA24_BRIGHTWING,(51,11,2,0.76,0.97,0.28,2.45,0,)),
(PTA21_MALTHAEL,(8,16,5,0.73,0,)),

    ),
    'SRU5_1':(
(PTA24_BRIGHTWING,(32,14,4,0.13,0.65,0.11,6.46,0,)),

(PTA21_MALTHAEL,(53,18,2,0.5,0,)),
(PTA24_DEATHWING,(50,25,2,0.28,0.35,0.23,9.88,0,)),

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
