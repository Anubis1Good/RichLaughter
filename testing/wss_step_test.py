from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.OGTA import *

from strategies.work_strategies.LTA import *
from strategies.work_strategies.LTA2 import *
from strategies.work_strategies.GLTA import *
from strategies.work_strategies.PSTA0 import *

wss_br = (
    (PTA19_TYRAEL,(100,9,26,75,36,13,0)),
    (LTA_IRONANNY,(25,15,2,7)),
    (PTA22_BERSERK,(134,6,2,2.26,6,0.33,31,34,41,12)),
    (PTA11_KUSURUKEN,(68,18,59,21,'c')),
    (LTA2_DRINKER,(96,1.78,44,45,18,18,0)),
    (PTA19_IMPERIUS,(100,10,24,84,47,23,0)),
    (PTA19_YREL,(100,9,28,43,14,24,0)),
    (LTA_BIBI,(107,6,10,'ultimate_oscillator')),
    (PTA12_SWDDCr,(26,36,0.49,39,58)),
    (PTA21_WHITEMANE,(7,92,10,2,3.0,6,0.25,0)),
    (PTA18_BLAZE,(113,12,34,46,13,0)),
    (PTA19_JOHANNA,(100,8,26,103,38,13,1)),
    (PTA19_CASSIA,(100,10,27,109,48,26,0)),
    (LTA_IGOGOSHA,(115,9,3,'ultimate_oscillator')),
    (STA3_LITE,(129,10,0.66,7,97)),
    (LTA2_LYNX,(80,1.72,51,18,0.84,0)),
    (PTA10_MAGIC,(94,143,2)),
    (PTA19_ZERATUL,(100,3,22,150,47,29,0)),
    (PTA21_AURIEL,(89,10,4,3.0,3,0.0)),
    (PTA14_RWDDCr,(2,40,134,105)),
    (LTA2_ALKASH,(119,0.81,103,4,0)),
    (LTA2_HOTS,(83,1.76,57,50,11,17,0))
)
wss_cny = (
    (PTA19_JOHANNA,(100,4,24,50,50,26,0)),
    (PTA18_BLAZE,(85,27,90,43,24,0)),
    (PTA19_ZERATUL,(100,5,35,90,43,39,0)),
    (PTA11_KUSURUKEN,(28,127,134,24,'hl')),
    (LTA2_HOTS,(142,0.84,15,48,26,22,0)),
    (LTA2_DRG,(114,1.78,19,41,15,28,0)),
    (PTA14_RANGER,(64,30,137,14,45,35)),
    (PTA4_U3,(13,150,9,3,'VG','uo')),
    (PTA21_WHITEMANE,(18,61,5,2,1.5,3,0.5,0)),
    (STA3_FORCE,(35,9,5,3,41,26,52)),
    (PTA19_TYRAEL,(100,4,27,55,48,39,0))
)
wss_ed = (
    (LTA2_DRINKER,(6,1.28,117,50,13,26,0)),
    (LTA2_LYNX,(38,0.76,129,15,1.42,0)),
    (PTA22_BERSERK,(36,8,2,3.37,7,0.0,132,88,26,55)),
    (PTA4_U3,(88,20,6,12,'DC','uo')),
    (LTA2_DRG,(4,0.58,146,33,22,19,0)),
    (LTA2_FENNEC,(31,0.9,89,50,30,0,0.5,0)),
    (PTA2_DDCrWork,(91,)),
    (PTA15_VALLA,(75,0)),
    (PTA2_LISICA,(128,1.01)),
    (LTA2_ALKASH,(34,1.34,133,21,0)),
    (LTA_OKROSHKA2,(10,79)),
    (PTA10_MAGIC,(79,146,150))
)
wss_euf = (
    (OGTA4_DOG,(7,19)),
    (LTA_BIBI,(51,9,2,'ultimate_oscillator')),
    (PTA21_AURIEL,(12,5,2,3.0,6,0.25)),
    (OGTA4_PUPPY,(8,28,21)),
    (PTA22_BERSERK,(65,7,4,6.17,6,0.74,43,74,29,16)),
    (PTA11_KUSURUKEN,(15,10,23,34,'hl')),
    (PTA2_BBBUr,(5,1,1)),
    (LTA2_ALKASH,(68,1.82,141,16,1)),
    (LTA2_LYNX,(79,1.91,116,8,1.0,1)),
    (PTA4_U3,(105,76,4,14,'VC','rsi')),
    (PTA11_KUSURUKEN,(103,34,10,35,'c')),
    (PTA15_VALLA,(21,0)),
    (PTA2_LISICA,(109,0.5)),
    (PTA2_DDCrVG,(15,)),
    (PTA14_RANGER,(146,30,103,13,38,30)),
)
wss_ng = (
    (LTA_BIBI,(133,5,2,'mfi')),
    (PTA22_BERSERK,(80,8,2,1.89,5,0.72,9,75,58,28)),
    (PTA4_U3,(14,58,7,2,'VC','s')),
    (PTA21_AURIEL,(79,10,2,3.0,6,0.25)),
    (PTA19_ZERATUL,(100,4,28,65,45,33,0)),
    (PTA4_U3,(8,70,12,2,'VC','rsi')),
    (PTA19_VALEERA,(100,5,13,34,21,20,1)),
    (PTA21_WHITEMANE,(38,66,10,4,3.0,3,0.5,1)),
    (LTA_IRONANNY,(88,6,7,6)),
    (LTA_IGOGOSHA,(82,13,2,'rsi')),
    (LTA_IGOGOSHA,(81,9,2,'%d')),
    (PTA18_DEHAKA,(100,10,5,30)),
    (PTA18_MISHA,(100,7,14,43,31)),
    (PTA19_YREL,(100,5,8,42,27,16,0)),
    (LTA2_DRINKER,(123,1.33,19,34,24,20,1)),
    (PTA14_ANGER,(138,41,16,60,11)),
    (PTA19_JOHANNA,(100,4,6,62,47,35,1)),
    (STA3_LITE,(124,9,0.76,6,92)),
    (PTA15_ANNA,(7,40))
)
wss_si = (
    (LTA_IRONANNY,(89,13,3,6)),
    (PTA22_BERSERK,(112,9,4,3.71,3,0.23,135,65,26,13)),
    (LTA2_HOTS,(121,1.6,33,48,22,8,0)),
    (PTA19_YREL,(100,5,29,39,15,20,0)),
    (PTA15_WIDOWMAKER,(27,40)),
    (PTA19_JOHANNA,(100,7,32,61,47,24,0)),
    (PTA19_TYRAEL,(100,5,32,69,46,20,0)),
    (PTA13_DWDDCr,(2,36,23)),
    (PTA11_KUSURUKEN,(46,63,61,27,'c')),
    (LTA_BIBI,(89,15,19,'rsi')),
    (LTA2_LYNX,(120,1.0,53,2,0.83,0)),
    (PTA2_DDCrWork,(39,)),
    (PTA12_SWDDCr,(29,37,0.97,50,80)),
    (PTA14_RANGER,(145,30,72,17,37,21)),

)
wss_sr = (
    (PTA21_AURIEL,(43,10,2,3.0,5,0.0)),
    (PTA21_WHITEMANE,(20,41,10,2,3.0,5,0.0,1)),
    (PTA4_U3,(22,45,12,2,'WC','s')),
    (LTA_BIBI,(139,13,3,'ultimate_oscillator')),
    (LTA_IRONANNY,(34,4,16,7)),
    (PTA11_KUSURUKEN,(66,30,26,13,'c')),
    (PTA22_BERSERK,(58,8,2,4.18,5,0.41,89,128,58,37)),
    (PTA10_WIZARD,(15,77,84,10,21)),
    (STA3_FORCE,(90,8,4,9,24,15,41)),
    (LTA2_HOTS,(87,1.41,24,46,26,25,1)),
    (PTA19_VALEERA,(100,6,22,35,25,28,0)),
    (PTA13_DWDDCr,(139,39,21))
)
