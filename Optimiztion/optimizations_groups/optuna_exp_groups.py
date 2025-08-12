from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.OGTA import *

from strategies.work_strategies.LTA import *
from strategies.work_strategies.LTA2 import *
from strategies.work_strategies.GLTA import *
from strategies.work_strategies.PSTA0 import *
from strategies.work_strategies.VSAT import *
# from strategies.work_strategies.HelpTA import get_rws

group = (
    (PSTA8_AVENGER,(
        (60,),
        (2,3,20),
        (0.1,0.5,1),
        (0,0.1,1),
        (0.1,0.2,0.5),
        (0.5,1,1.1,2,10),
        (0,1)
    )),
    (PTA25_TASSADAR,(
        (2,7,150),
        (2,5,30),
        (2,3,5),
        (0.1,0.5,1),
        (0,0.1,1),
        (0.1,0.2,0.5),
        (0.5,1,1.1,2,10),
        (0,5,11,50),
        (0,1)
    )),
    (VSAT1_VENUS,(
        (60,),
        (0.1,0.5,1),
        (0,0.1,1),
        (0.1,0.2,0.5),
        (0.5,1,1.1,2),
        (0,1),
        (0,1),
        (0,1),
    )),
    (PTA21_MALTHAEL,(
        (2,7,150),
        (2,5,30),
        (2,3,5),
        (0.1,0.5,1),
        (0,1)
    )),
    (PTA24_BRIGHTWING,(
        (2,7,150),
        (2,5,30),
        (2,3,5),
        (0.1,0.5,1),
        (0,0.1,1),
        (0.1,0.2,0.5),
        (0.5,1,1.1,2,10),
        (0,1)
    )),
    (PTA24_DEATHWING,(
        (2,7,150),
        (2,5,30),
        (2,3,5),
        (0.1,0.5,1),
        (0,0.1,1),
        (0.1,0.2,0.5),
        (0.5,1,1.1,2,10),
        (0,1)
    )),
)

