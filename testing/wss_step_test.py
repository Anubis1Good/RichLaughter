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
        # (PSTA6_DODO,(34,2,20,35,)),
        # (PSTA6_VULTURE,(40,2,20,50,17,13,0.81,)),
        # (PSTA6_PIGEON,(84,62,70,13,2,0.11,0.46,0,)),
        # (PSTA6_SHERIFF,(150,19,2.3,)),
        # (PSTA6_ADVENTURE,(39,27,94,1.26,1,)),
        # (PSTA6_DUELDODO,(38,2,20,149,1,)),
        (LTA_CC,(5,20,2,8,3,0.66,0,1,)), #1907
        (PSTA2_GGD,(60,2,3)), #1907
        (PSTA2_GOOSE,(50,4,1,)), #2507 BRQ5
        (PSTA4_PELICAN,(108,3,1,0.0,)), #2507 BRQ5
        (PTA19_YREL,(100,8,2,42,40,4,0)),
    ),
    'EDU5_1':(
        # (PSTA6_PIGEON,(55,150,120,25,11,0.17,0.58,0,)),
        # (PSTA6_SHERIFF,(75,138,1.02,)),
        # (PSTA6_VULTURE,(5,91,28,36,11,9,0.35,)),
        # (PSTA6_DUELDODO,(150,131,10,107,0,)),
        # (PSTA6_DODO,(146,137,13,69,)),
        # (PSTA6_ADVENTURE,(42,138,5,0.79,1,)),
        (LTA2_FENNEC, (9,1.7,72,43,30,12,1.54,0)),
        (PTA11_KUSURUKEN, (85,112,43,32,'hl')),
        (LTA2_DRINKER, (118,1.62,123,49,27,1,0)),
        (PTA19_JOHANNA,(100,3,5,10,40,10,0)),
        (PTA14_RENEGADE,(70,30,10,5,30,40)),
    ),
    'GZU5_1':(
        # (PSTA6_SHERIFF,(25,3,2.57,)),
        # (PSTA6_ADVENTURE,(31,3,135,2.93,1,)),
        # (PSTA6_PIGEON,(25,3,124,18,5,0.24,2.39,1,)),
        # (PSTA6_DUELDODO,(41,3,46,68,0,)),
        # (PSTA6_DODO,(134,3,62,55,)),
        # (PSTA6_VULTURE,(150,3,39,57,5,19,0.29,)),
        (PTA21_AURIEL,(4,10,3,3,6,0.5)),
        (LTA_CC,(5,20,2,8,3,0.66,0,1,)),
        (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',1,1)),
        (PTA15_WIDOWMAKER,(5,30)),
        (PTA4_WDVCr,(7,30)),
    ),
    'IMOEXF_1':(
        # (PSTA6_SHERIFF,(28,3,2.97,)),
        # (PSTA6_PIGEON,(9,3,139,2,15,0.38,2.43,1,)),
        # (PSTA6_ADVENTURE,(100,2,14,1.76,0,)),
        # (PSTA6_VULTURE,(150,3,52,10,12,9,0.49,)),
        # (PSTA6_ADVENTURE,(114,13,45,2.11,0,)),
        # (PSTA6_DUELDODO,(128,3,65,86,1,)),
        # (PSTA6_DODO,(94,3,48,55,)),
        # (PSTA6_PIGEON,(100,13,59,17,16,0.16,2.02,0,)),
        (LTA_CC,(28,11,2,8,9,2.31,0,0,)),
        (PSTA2_GGD,(60,2,2)),
        (LTA_CC,(5,20,2,8,3,0.66,0,1,)), 
        (LTA_IRONANNY,(30,10,3,4)),
        (PTA19_JOHANNA,(100,7,9,108,45,17,0)),
    ),
    'MMU5_1':(
        # (PSTA6_SHERIFF,(37,5,2.93,)),
        # (PSTA6_PIGEON,(50,11,138,4,6,0.18,1.7,0,)),
        # (PSTA6_PIGEON,(24,5,97,6,10,0.19,2.65,0,)),
        # (PSTA6_ADVENTURE,(117,5,101,2.08,0,)),
        # (PSTA6_VULTURE,(141,5,60,80,11,7,0.18,)),
        # (PSTA6_DODO,(76,5,51,34,)),
        # (PSTA6_DUELDODO,(141,5,55,59,1,)),
        # (PSTA6_VULTURE,(9,12,30,140,8,1,0.77,)),
        (PTA18_DEHAKA,(100,10,5,30)),
        (PSTA2_GGD,(60,2,3)),
        (OGTA6_CERBERUS,(28,29,54,)),
        (PTA14_RANGER,(70,30,10,5,30,40)),
        (PTA18_MISHA,(100,8,5,44,33)),
    ),
    'NGN5_1':(
        # (PSTA6_PIGEON,(101,86,115,8,1,0.96,0.85,0,)),
        # (PSTA6_SHERIFF,(145,86,1.09,)),
        # (PSTA6_VULTURE,(69,104,10,64,9,1,0.26,)),
        # (PSTA6_ADVENTURE,(141,86,143,0.95,1,)),
        # (PSTA6_DODO,(63,107,11,31,)),
        # (PSTA6_DUELDODO,(60,85,11,143,0,)),
        (PTA22_BERSERK,(65,7,4,6.17,6,0.74,43,74,29,16)),
        (PTA22_BERSERK,(80,8,2,1.89,5,0.72,9,75,58,28)),
        (PTA14_RANGER,(40,30,130,15,40,40)),
        (PTA21_AURIEL,(30,10,3,3,3,0.5)),
        (PTA19_CASSIA,(100,7,5,10,40,10,0)),
    ),
    'RMU5_1':(
        # (PSTA6_SHERIFF,(61,2,2.68,)),
        # (PSTA6_SHERIFF,(53,5,2.36,)),
        # (PSTA6_ADVENTURE,(70,2,11,2.94,0,)),
        # (PSTA6_ADVENTURE,(132,4,131,1.93,1,)),
        # (PSTA6_PIGEON,(16,2,150,30,3,0.55,2.45,0,)),
        # (PSTA6_PIGEON,(53,5,77,22,19,0.42,2.51,0,)),
        # (PSTA6_DODO,(72,4,33,47,)),
        # (PSTA6_VULTURE,(36,2,64,116,28,11,0.21,)),
        # (PSTA6_DUELDODO,(40,2,69,122,1,)),
        # (PSTA6_DUELDODO,(99,5,25,79,1,)),
        # (PSTA6_VULTURE,(117,4,54,82,13,6,0.42,)),
        (PSTA2_GGD,(60,2,2)), 
        (LTA_CC,(136,2,7,4,3,2.23,1,1,)),
        (LTA2_DRINKER,(60,2,5,40,30,0,0)), 
        (LTA2_ALKASH,(150,1,20,30,0)),
        (PTA19_YREL,(100,8,2,42,40,4,0)),
    ),
    'SRU5_1':(
        # (PSTA6_SHERIFF,(85,48,1.63,)),
        # (PSTA6_VULTURE,(12,46,37,69,10,5,0.1,)),
        # (PSTA6_ADVENTURE,(62,49,84,1.61,0,)),
        # (PSTA6_PIGEON,(61,48,37,14,14,0.97,1.61,0,)),
        # (PSTA6_DODO,(11,47,35,53,)),
        # (PSTA6_DUELDODO,(20,51,29,102,0,)),
        (OGTA6_CERBERUS,(80,120,71)),
        (PTA19_YREL,(100,4,25,49,35,15,0,)), 
        (PTA19_JOHANNA,(100,5,18,44,49,24,0)),
        (LTA_IGOGOSHA,(123,13,2,'ultimate_oscillator')),
        (LTA2_FENNEC,(68,1.95,23,49,13,17,1.88,0)),
    ),

    'default':[]
}
