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
    '5GZU5_1':(
        (LTA2_HOTS,(146,1.4,7,50,27,21,0)),
        (LTA2_PUBG,(134,1.67,5,47,18,27,1)),
        (LTA_BIBI,(101,4,2,'rsi_tw')),
        (PTA2_DDCrVG,(10,)),
        (LTA_IRONANNY,(48,9,2,4)),
        (PTA2_DDCrWork,(8,)),
        (PTA21_AURIEL,(52,5,3,1.5,5,0.25)),
        (PTA22_BERSERK,(139,4,2,2.96,10,0.24,13,86,50,22)),
        (PTA18_DEHAKA,(100,5,22,35)),
        (PTA2_LISICA,(11,1.63)),
        (PSTA2_GGD,(60,2,3)),

    ),
    '5IMOEXF_1':(
        (LTA_IRONANNY,(93,4,2,7)),
        (PTA4_U3,(30,78,12,2,'VC','s')),
        (PTA19_JOHANNA,(100,5,5,93,47,17,1)),
        (PTA21_AURIEL,(57,5,2,3.0,3,0.5)),
        (LTA2_HOTS,(145,1.72,7,43,18,24,0)),
        (PTA14_RENEGADE,(97,40,56,5,27,33)),
        (PTA19_IMPERIUS,(100,4,9,53,13,26,0)),
        (LTA_BIBI,(61,4,2,'rsi_tw')),
        (PTA22_BERSERK,(138,8,2,5.15,9,0.19,87,28,49,43)),
        (PTA2_DDCrWork,(11,)),
        (LTA2_FENNEC,(146,1.8,9,50,13,26,1.12,1)),
        (PTA19_YREL,(100,8,7,43,21,11,1)),
        (PTA2_DVCr,(17,)),
        (LTA2_LYNX,(115,1.64,21,23,1.21,0)),
        (LTA2_DRG,(143,1.5,5,38,24,7,1)),

    ),
    '5MMU5_1':(
        (STAML2b_RAPTOR,(100,5,30,30,30,0,0)),
        (STAML2b_RAPTOR,(60,2,30,30,30,0,0)),
        (STAML2b_RAPTOR,(10,2,30,30,30,0,0)),
        (STAML2b_RAPTOR,(10,2,30,30,30,0,1)),
        (STAML2b_RAPTOR,(10,2,30,30,30,0,1,3)),
        (STAML2b_RAPTOR,(5,2,15,15,30,0,1,3)),
        (STAML2b_RAPTOR,(5,2,15,15,30,1,1,3)),

    ),
    '5RMU5_1':(
        (PSTA2_GGD,(60,2,2)),
        (PTA19_YREL,(100,8,2,42,40,4,0)),
        (LTA2_PUBG,(76,1.86,2,44,22,1,0)),
        (LTA2_ALKASH,(132,1.71,2,22,0)),
        (LTA2_HOTS,(140,1.93,2,41,23,1,0)),
        (PTA19_TYRAEL,(100,6,2,131,43,40,1)),
        (PTA14_RENEGADE,(90,30,40,5,38,27)),
        (PTA10_MAGIC,(5,142,2)),
        (PTA19_JOHANNA,(100,8,2,42,34,30,0)),
        (PTA19_IMPERIUS,(100,8,2,150,13,29,0)),
        (PTA19_CASSIA,(100,7,2,100,36,16,0)),
        (LTA_OKROSHKA2,(2,115)),
        (LTA2_LOGAN,(3,150,11)),
        (OGTA4_DOG,(2,11)),
        (PTA4_U3,(21,12,8,2,'VC','uo')),
        (PTA18_BLAZE,(144,2,44,44,34,0)),
        (LTA_IRONANNY,(94,4,4,4)),
        (PTA14_RANGER,(72,40,138,9,41,30)),
        (PTA22_BERSERK,(94,3,2,4.69,3,0.63,116,41,54,57)),

    ),
    'default':[]
}
