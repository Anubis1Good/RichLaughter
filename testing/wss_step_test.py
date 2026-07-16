from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.OGTA import *

from strategies.work_strategies.LTA import *
from strategies.work_strategies.LTA2 import *
# from strategies.work_strategies.GLTA import *
from strategies.work_strategies.PSTA0 import *
from strategies.work_strategies.STA_ml2 import *
from strategies.work_strategies.VSAT import *
from strategies.work_strategies.HelpTA import get_rws


map_wss = {

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

    '_5DATA': (
        (PSTA9_BIRDWATCHER,(40,2.18,4,0.29,1.96,1,0,)),
        (PSTA2_DUCK,(47,21,1,)),
        (PTA11_KUSURUKEN,(29,35,54,34,'c',)),
        (PTA24_BRIGHTWING,(52,10,5,0.1,0.82,0.31,4.46,1,)),
        (PTA4_U3,(32,56,15,10,'VC','rsi',)),
        (PTA19_YREL,(60,4,14,49,12,0,0,)),
    ),
    '_5EUTR': (
        (PSTA9_BIRDWATCHER,(17,1.69,5,0.29,0.85,1,1,)),
        (VSAT1_VENUS,(60,0.25,0.87,0.15,1.36,0,0,0,)),
        (PTA24_BRIGHTWING,(9,11,4,0.57,0.71,0.38,7.01,1,)),
        (PTA19_TYRAEL,(60,9,10,46,33,18,0,)),
        (PTA19_IMPERIUS,(60,9,12,31,40,20,0,)),
        (PSTA2_DUCK,(29,13,1,)),
    ),
    '_5IVAT': (
        (PSTA9_BIRDWATCHER,(33,1.72,3,0.26,1.55,1,1,)),
        (PSTA9_GRAVY,(9,2.15,2,0.26,1.3,1,)),
        (VSAT1_MERCURY,(17,1.48,1.0,0.36,0.88,1,1,0,)),
        (PTA19_TYRAEL,(60,10,20,22,37,24,0,)),
        (PTA4_UNIVERSAL,(45,16,12,32,'WC','mfi',1,1,)),
        (PSTA6_SHERIFF,(44,5,2.77,)),
    ),
    '_5MAGN': (
        (PSTA9_BIRDWATCHER,(25,2.03,3,0.24,1.58,1,1,)),
        (PSTA2_DUCK,(2,18,1,)),
        (PSTA4_FALCON,(51,13,2,0.31,)),
        (PTA25_TASSADAR,(37,18,2,0.24,0.51,0.38,3.05,7,0,)),
        (LTA_IGOGOSHA,(29,15,2,'%d',)),
        (PSTA5_HAWK,(50,11,12,2,0,34,4.42,16,0.97,0.31,0,)),
    ),
    '_5MTLR': (
        (PTA11_KUSURUKEN,(49,51,39,25,'c',)),
        (PTA18_BLAZE,(10,13,7,49,11,0,)),
        (PTA10_WIZARD,(18,55,60,29,21,)),
        (OGTA7_PARADOX,(8,2.04,)),
        (PSTA2_DUCK,(21,28,1,)),
        (PTA4_U3,(14,57,15,2,'VC','s',)),
    ),
    '_5RAGR': (
        (PSTA2_DUCK,(16,13,2,)),
        (VSAT1_MERCURY,(34,2.55,0.12,0.41,1.31,0,1,0,)),
        (PSTA2_GOOSE,(19,12,1,)),
        (PTA11_KUSURUKEN,(56,52,46,23,'hl',)),
        (LTA_CC,(38,6,2,10,10,1.38,0,0,)),
        (PSTA6_VULTURE,(55,30,10,57,11,1,0.18,)),
    ),
    '_5RNFT': (
        (PTA11_KUSURUKEN,(58,41,16,11,'c',)),
        (VSAT1_MERCURY,(26,2.01,0.46,0.33,1.16,0,1,0,)),
        (PTA19_TYRAEL,(60,4,43,60,50,13,0,)),
        (PTA22_BERSERK,(40,9,2,2.12,5,0.01,5,37,44,11,)),
        (PSTA6_DODO,(19,48,24,70,)),
        (LTA2_DRINKER,(46,1.81,33,43,20,29,0,)),
    ),
    '_5SGZH': (
        (PSTA9_GRAVY,(23,1.52,2,0.3,0.78,1,)),
        (PSTA9_BIRDWATCHER,(51,2.45,3,0.2,1.69,1,0,)),
        (PTA19_TYRAEL,(60,8,33,40,48,30,0,)),
        (PTA11_KUSURUKEN,(36,31,16,16,'c',)),
        (PSTA4_PELICAN,(43,7,5,0.29,)),
        (LTA2_FENNEC,(21,1.57,19,49,26,1,0.64,0,)),
    ),
    '_5SPBE': (
        (PSTA2_DUCK,(16,15,1,)),
        (VSAT1_VENUS,(60,0.88,0.47,0.31,1.84,0,1,0,)),
        (PSTA4_PELICAN,(5,15,1,0.08,)),
        (PTA19_JOHANNA,(60,5,29,58,44,13,0,)),
        (PTA4_UNIVERSAL,(7,4,17,38,'DC','rsi_tw',1,1,)),
        (PSTA6_VULTURE,(52,31,33,58,14,2,0.38,)),
    ),
    '_5VTBR': (
        (PSTA4_PELICAN,(48,14,4,0.27,)),
        (PSTA5_HAWK,(29,13,17,2,0,26,9.08,41,0.0,0.3,0,)),
        (PTA11_KUSURUKEN,(33,28,46,19,'c',)),
        (PSTA2_GOOSE,(28,15,5,)),
        (LTA_BIBI,(36,11,2,'%d',)),
        (PTA24_BRIGHTWING,(27,9,2,0.47,0.93,0.22,5.68,1,)),
    ),

    'default':[

    ]
}
