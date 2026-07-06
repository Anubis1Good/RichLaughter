from strategies.work_strategies.LTA import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.PTAXX import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.STA_ml import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.OGTA import *
from strategies.work_strategies.PSTA0 import *
from strategies.work_strategies.VSAT import *
from strategies.work_strategies.MTA import *
from strategies.work_strategies.MTA_KING import MTA_KING,MTA_LIGHT
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
    ((TestVTTA,(100,)),
     ('VTBR1','ETLN1','MTLR1','SGZH1','DATA1','DELI1','IVAT1','MVID1'),
     False
     ),
    ((PSTA9_GRAVY,(10,2.81,2,0.28,0.77,1,)),
     ('DATA',),
     False
     ),
    ((VSAT1_VENUS,(60,0.13,0.58,0.32,0.94,0,1,0,)),
     ('DELI',),
     False
     ),
    ((PTA24_BRIGHTWING,(22,3,4,0.35,0.24,0.28,7.98,1,)),
     ('ETLN',),
     False
     ),
    ((PSTA2_DUCK,(13,15,1,)),
     ('EUTR',),
     False
     ),
    ((VSAT1_MERCURY,(45,1.78,0.72,0.33,0.72,0,1,1,)),
     ('IVAT',),
     False
     ),
    ((PSTA2_GOOSE,(54,29,1,)),
     ('MTLR',),
     False
     ),
    ((PSTA6_PIGEON,(16,5,26,9,6,0.12,2.52,0,)),
     ('MVID',),
     False
     ),
    ((PSTA9_BIRDWATCHER,(32,1.8,3,0.23,1.44,0,0,)),
     ('RAGR',),
     False
     ),
    ((PTA14_RENEGADE,(57,40,9,5,25,19,)),
     ('RNFT',),
     False
     ),
    ((PTA22_BERSERK,(53,9,4,7.74,3,0.72,23,49,58,16,)),
     ('SGZH',),
     False
     ),
    ((PTA11_KUSURUKEN,(47,42,25,34,'hl',)),
     ('VSEH',),
     False
     ),
    ((PSTA4_PELICAN,(57,16,2,0.05,)),
     ('VTBR',),
     False
     ),


    # ((MTA_LIGHT,(100,'KING_5_MOEX_SPECIAL','u')),
    #  ('NVTK2','RUAL2','CHMF2','GAZP2','ALRS2','TRMK2','MTLR2','LSRG2','MAGN2','NMTP2','GMKN2','AFLT2','IRAO2','ROSN2','NLMK2','TATN2','AFKS2','HYDR2','PIKK2','SELG2','UPRO2','YDEX2','TRNFP2','BANEP2','RTKM2','MGNT2','SIBN2','MOEX2','MTSS2','SNGSP2','FESH2','LKOH2','CBOM2','FEES2','SBER2','VTBR2','SNGS2','APTK2','QIWI2','KZOSP2','UWGN2'),
    #  False),
    # ((MTA_KING,(100,'KING_5_MOEX_SPECIAL','u')),
    #  ('KZOSP2',),
    #  True),
    # ((MTA_LIGHT,(100,'KING_5_MOEX_STOCK','u')),
    #  ('NVTK','RUAL','CHMF','GAZP','ALRS','TRMK','MTLR','LSRG','MAGN','NMTP','GMKN','AFLT','IRAO','ROSN','NLMK','TATN','AFKS','HYDR','PIKK','SELG','UPRO','YDEX','TRNFP','BANEP','RTKM','MGNT','SIBN','MOEX','MTSS','SNGSP','FESH','LKOH','CBOM','FEES','SBER','VTBR','SNGS','APTK','QIWI','KZOSP','UWGN'),
    #  False),
    # ((MTA_KING,(100,'KING_5_MOEX_STOCK','u')),
    #  ('KZOSP',),
    #  True),
    # ((MTA_KING,(100,'KING_1_MOEX_STOCK','u')),
    #  ('',)),
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