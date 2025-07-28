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
    'CNYRUBF_1':(
        (PSTA3_HADES,(105,30,'mean',)),
        (STA3_FORCE,(131,3,3,5,19,35,14,)),
        (PTA19_ZERATUL,(100,4,42,98,43,17,0,)),
        (PTA18_DEHAKA,(100,4,47,17,)),
        (PTA14_RENEGADE,(82,30,40,5,25,15,)),
        (PTA19_VALEERA,(100,4,13,25,27,5,1,)),
    ),
    'CRU5_1':(
        (PSTA3_HADES,(22,26,'std',)),
        (PTA10_WIZARD,(136,45,39,19,28,)),
        (PTA14_RENEGADE,(13,40,62,15,43,31,)),
        (PSTA4_FALCON,(41,19,1,0.09,)),
        (PTA4_U3,(37,135,13,2,'WC','uo',)),
        (OGTA6_CERBERUS,(57,150,62,)),
        (PSTA4_PELICAN,(9,25,1,0.03,)),
    ),
    'EDU5_1':(
        (LTA2_FENNEC,(9,1.7,72,43,30,12,1.54,0,)),
        (LTA2_DRINKER,(118,1.62,123,49,27,1,0,)),
        (PSTA3_HADES,(76,18,'mean',)),
        (LTA_BIBI,(132,10,13,'cmo',)),
        (PTA22_BERSERK,(80,4,5,2.89,10,0.28,102,143,21,39,)),
        (PTA2_LISICA,(137,0.86,)),
        (PTA11_KUSURUKEN,(85,112,43,32,'hl',)),
    ),
    'NGN5_1':(
        (PSTA2_GOOSE,(35,15,2,)),
        (PSTA4_PELICAN,(109,15,2,0.01,)),
        (PSTA2_DUCK,(150,17,2,)),
        (PTA22_BERSERK,(125,7,4,6.37,8,0.5,130,58,53,51,)),
        (PTA19_VALEERA,(100,6,46,44,33,8,1,)),
        (PTA19_IMPERIUS,(100,9,29,9,36,35,1,)),
        (LTA2_FENNEC,(121,1.8,24,39,13,17,1.01,0,)),
        (PTA22_BERSERK,(121,8,4,6.73,9,0.66,137,57,53,46,)),
        (LTA_IGOGOSHA,(51,10,2,'%d',)),
        (LTA_IRONANNY,(28,14,2,6,)),
        (PTA21_AURIEL,(69,10,2,3.0,5,0.5,)),
        (PTA19_ZERATUL,(100,6,41,39,49,24,1,)),
        (OGTA4_RAT,(29,20,4,)),
        (LTA_BIBI,(54,13,2,'rsi_tw',)),
        (STA3_FORCE,(147,7,2,6,35,19,25,)),
        (PTA4_U3,(6,57,13,2,'VG','rsi_tw',)),
        (PTA23_ULTIMATUM,(44,17,41,53,26,0,2,1.32,65,0.52,0.35,0,)),
        (LTA_CC,(81,19,2,8,10,0.68,0,1,)),
    ),
    'SRU5_1':(
        (PSTA3_REVAN,(95,8,)),
        (PTA21_AURIEL,(37,10,2,3.0,5,0.0,)),
        (LTA_BIBI,(82,13,2,'ultimate_oscillator',)),
        (OGTA6_CERBERUS,(80,120,71,)),
        (LTA_CC,(32,17,2,9,10,0.78,0,1,)),
        (PTA4_U3,(11,43,10,2,'WC','s',)),
        (PTA22_BERSERK,(22,9,2,6.17,8,0.2,16,27,45,50,)),
        (LTA_IGOGOSHA,(123,13,2,'ultimate_oscillator',)),
        (PTA19_YREL,(100,4,25,49,35,15,0,)),
        (PSTA2_DUCK,(120,22,1,)),
        (PTA21_WHITEMANE,(19,123,10,2,1.5,6,0.25,0,)),
        (OGTA4_RAT,(34,9,29,)),
        (PTA19_JOHANNA,(100,5,18,44,49,24,0,)),
        (OGTA4_HAMSTER,(28,39,)),
        (PTA14_RENEGADE,(15,30,126,8,35,31,)),
    ),
    'default':[]
}
