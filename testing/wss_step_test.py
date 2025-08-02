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

map_wss = {
    'BRQ5_1':(
        (PSTA6_VULTURE,(34,19,23,45,2,19,0.67,)),
        (PSTA7_SHERIFF,(150,12,2,2.14,)),
        (PSTA6_SHERIFF,(138,19,2.52,)),
        (PSTA6_ADVENTURE,(70,26,68,1.15,0,)),
        (PSTA7_ADVENTURE,(98,4,15,1.15,0,)),
        (PSTA6_DUELDODO,(100,65,14,24,0,)),
        (PSTA7_DUELDODO,(141,3,15,16,110,1,)),
        (PSTA6_DODO,(100,73,21,14,)),

        (PSTA6_DODO,(33,2,22,45,)),
        (PSTA7_DODO,(96,2,19,32,42,)),
        (PSTA6_SHERIFF,(124,19,2.42,)),
        (PSTA7_SHERIFF,(117,12,2,2.45,)),
        (PSTA6_ADVENTURE,(33,19,127,1.33,1,)),
        (PSTA6_VULTURE,(144,21,10,38,13,14,0.04,)),
        (PSTA7_VULTURE,(104,10,93,2,19,11,11,0.34,)),
        (PSTA6_DUELDODO,(137,19,12,47,1,)),
    ),
    'EDU5_1':(

        (PSTA6_VULTURE,(136,144,15,89,16,15,0.02,)),
        (PSTA7_SHERIFF,(52,15,20,1.29,)),
        (PSTA6_SHERIFF,(27,131,2.64,)),
    ),
    'GZU5_1':(
        (PSTA6_DUELDODO,(58,9,65,72,1,)),
        (PSTA6_SHERIFF,(137,10,0.82,)),
        (PSTA7_DUELDODO,(84,3,3,10,124,0,)),

        (PSTA6_DODO,(124,3,49,52,)),
        (PSTA7_ADVENTURE,(36,2,3,2.7,1,)),
        (PSTA6_ADVENTURE,(27,3,123,2.67,0,)),
        (PSTA6_SHERIFF,(21,9,2.24,)),
        (PSTA7_PIGEON,(68,2,6,10,6,0.96,2.53,0,)),
        (PSTA6_VULTURE,(141,3,37,133,5,11,0.21,)),
        (PSTA7_VULTURE,(139,54,147,2,7,12,1,0.65,)),
        (PSTA7_DUELDODO,(125,2,3,40,47,0,)),
        (PSTA6_DUELDODO,(137,7,53,140,1,)),
    ),
    'IMOEXF_1':(
        (PSTA7_ADVENTURE,(112,5,4,1.74,0,)),
        (PSTA6_PIGEON,(17,53,25,21,5,0.15,2.79,1,)),
        (PSTA7_DUELDODO,(118,5,4,33,62,1,)),
        (PSTA6_DUELDODO,(141,51,48,91,1,)),
        (PSTA7_VULTURE,(115,58,131,6,4,9,2,0.71,)),
        (PSTA7_DODO,(51,6,4,50,62,)),
        (PSTA6_VULTURE,(140,51,63,68,20,3,0.62,)),
        (PSTA6_DODO,(58,53,63,31,)),

        (PSTA6_SHERIFF,(22,4,1.99,)),
        (PSTA6_ADVENTURE,(15,5,39,1.91,0,)),
        (PSTA7_ADVENTURE,(34,2,10,2.24,1,)),
        (PSTA6_PIGEON,(78,65,93,9,12,0.08,0.82,0,)),
        (PSTA7_PIGEON,(143,6,4,29,4,0.81,2.53,0,)),
        (PSTA6_VULTURE,(44,10,31,43,12,3,0.13,)),
        (PSTA7_VULTURE,(135,63,94,4,2,12,7,0.82,)),
        (PSTA6_DUELDODO,(43,10,31,22,0,)),
        (PSTA7_DUELDODO,(137,4,2,61,120,1,)),
        (PSTA6_DODO,(50,10,35,42,)),
        (PSTA7_DODO,(129,2,10,63,20,)),

    ),
    'MMU5_1':(
        (PSTA6_DUELDODO,(100,39,12,39,0,)),

        (PSTA6_PIGEON,(54,11,62,5,13,0.11,1.78,0,)),
        (PSTA6_ADVENTURE,(41,5,70,2.83,0,)),
        (PSTA6_VULTURE,(94,5,23,130,10,16,0.47,)),
        (PSTA7_VULTURE,(85,26,150,2,13,26,20,0.02,)),
        (PSTA6_DODO,(112,5,33,46,)),
        (PSTA7_DODO,(150,2,11,34,58,)),
        (PSTA6_SHERIFF,(139,13,2.27,)),
        (PSTA7_DUELDODO,(46,2,5,49,84,0,)),
        (PSTA6_DUELDODO,(133,5,67,129,1,)),
    ),
    'NGN5_1':(
        (PSTA6_SHERIFF,(101,87,0.63,)),
        (PSTA6_ADVENTURE,(97,86,136,0.79,1,)),
        (PSTA6_VULTURE,(68,134,10,87,9,1,0.02,)),

        (PSTA6_PIGEON,(140,88,13,5,7,0.36,1.06,1,)),
        (PSTA6_SHERIFF,(150,87,1.11,)),
        (PSTA6_PIGEON,(142,85,26,6,11,0.27,0.95,1,)),
        (PSTA6_ADVENTURE,(104,88,33,0.85,0,)),
    ),
    'RMU5_1':(
        (PSTA6_SHERIFF,(72,6,2.53,)),
        (PSTA7_SHERIFF,(71,3,1,2.46,)),
        (PSTA6_ADVENTURE,(68,6,92,1.79,0,)),
        (PSTA7_ADVENTURE,(138,3,1,1.1,0,)),
        (PSTA7_PIGEON,(16,4,1,22,17,0.85,2.08,1,)),
        (PSTA6_PIGEON,(146,52,68,7,18,0.81,1.07,0,)),
        (PSTA6_DODO,(71,6,32,48,)),
        (PSTA7_DODO,(116,4,2,65,69,)),
        (PSTA6_DUELDODO,(35,6,70,12,1,)),
        (PSTA7_DUELDODO,(15,4,1,66,9,0,)),
        (PSTA6_VULTURE,(83,8,22,20,4,2,0.27,)),
        (PSTA7_VULTURE,(112,56,77,3,1,11,12,0.32,)),

        (PSTA7_PIGEON,(54,2,6,26,2,0.03,2.46,0,)),
    ),
    'SRU5_1':(
        (PSTA6_VULTURE,(11,42,33,10,3,5,0.53,)),
        (PSTA6_ADVENTURE,(91,58,94,0.85,0,)),
        (PSTA6_DUELDODO,(31,48,15,52,0,)),

        (PSTA6_SHERIFF,(89,51,1.57,)),
        (PSTA7_SHERIFF,(118,4,7,2.19,)),
        (PSTA6_ADVENTURE,(66,48,90,1.62,1,)),
        (PSTA7_ADVENTURE,(91,4,7,1.53,0,)),
        (PSTA6_DODO,(20,49,34,69,)),
        (PSTA7_DODO,(12,4,12,28,41,)),
        (PSTA6_DUELDODO,(23,51,29,15,0,)),
        (PSTA7_DUELDODO,(84,4,7,13,36,0,)),
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
    'default':[]
}
