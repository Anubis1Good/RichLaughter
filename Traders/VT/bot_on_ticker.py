from strategies.work_strategies.LTA import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.PTA30_39 import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.STA_ml import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.OGTA import *
from strategies.work_strategies.PSTA0 import *
from strategies.work_strategies.VSAT import *
# from strategies.work_strategies.MTA import *
# from strategies.work_strategies.MTA_KING import MTA_KING,MTA_LIGHT
from strategies.work_strategies.BaseTA import BaseTABitget
from strategies.work_strategies.HelpTA import TestVTTA

from Optimiztion.Optimizator1 import generate_combinations

# wss_u = []
# configs = generate_combinations((
#     (6,11),
#     (6,11),
#     (30,60),
#     (30,60),
#     ('DC',),
#     ("rsi",),
#     (0,1),
#     (0,1)
# ))
# for conf in configs:
#     wss_u.append((PTA4_UNIVERSAL,conf))

bot_on_ticker = (
    ((PTA30_RAYNOR,(14,14,30,15,25,40,True,'12','12','2',5,10)),
     ('VTBR1','ETLN1','MTLR1','SGZH1','DATA1','DELI1','IVAT1','MVID1'),
     False
     ),

    ((PTA30_RAYNOR,(14,14,30,15,25,40,True,'2','12','2',1,5)),
     ('DELI','ETLN','MVID','GECO'),
     False
     ),

    ((PTA30_RAYNOR,(14,14,30,15,25,40,True,'2','12','2',3,10)),
     ('DATA','RAGR','ELMT','MAGN'),
     False
     ),

    ((PTA30_RAYNOR,(14,14,30,15,25,40,True,'2','12','2',5,10)),
     ('VSEH',),
     False
     ),
    # ((PSTA9_GRAVY,(10,2.81,2,0.28,0.77,1,)), #-1
    #  ('DATA',),
    #  False
    #  ),
    # ((VSAT1_VENUS,(60,0.13,0.58,0.32,0.94,0,1,0,)), #+1
    #  ('DELI',),
    #  False
    #  ),
    # ((PTA24_BRIGHTWING,(22,3,4,0.35,0.24,0.28,7.98,1,)), #=1
    #  ('ETLN',),
    #  False
    #  ),
    ((PSTA2_DUCK,(29,13,1,)),
     ('EUTR',),
     False
     ),
    ((PTA4_UNIVERSAL,(45,16,12,32,'WC','mfi',1,1,)),
     ('IVAT',),
     False
     ),
    ((OGTA7_PARADOX,(8,2.04,)),
     ('MTLR',),
     False
     ),
    # ((PSTA6_PIGEON,(16,5,26,9,6,0.12,2.52,0,)), #+1
    #  ('MVID',),
    #  False
    #  ),
    # ((PSTA9_BIRDWATCHER,(32,1.8,3,0.23,1.44,0,0,)), #+1
    #  ('RAGR',),
    #  False
    #  ),
    ((PTA11_KUSURUKEN,(58,41,16,11,'c',)), 
     ('RNFT',),
     False
     ),
    ((PTA11_KUSURUKEN,(36,31,16,16,'c',)),
     ('SGZH',),
     False
     ),
    ((PTA4_UNIVERSAL,(7,4,17,38,'DC','rsi_tw',1,1,)),
     ('SPBE',),
     False
     ),
    # ((PSTA4_PELICAN,(57,16,2,0.05,)), #-1
    #  ('VTBR',),
    #  False
    #  ),



    # ((MTA_LIGHT,(100,'KING_1_MOEX_FUT','u')),
    #  ('CRU5','MMU5','MXU5','GZU5','SRU5','RIU5','RMU5','SiU5','IMOEXF'),
    #  True),

)

# sleep_group = ()

def init_trader(ticker):
    for bt in  bot_on_ticker:
        if ticker in bt[1]:
            return bt[0],bt[2]
    return (BaseTABitget,(1,)),False