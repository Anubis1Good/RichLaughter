from strategies.work_strategies.LTA import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.STA_ml import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.OGTA import *
from strategies.work_strategies.MTA import *
from strategies.work_strategies.MTA_KING import MTA_KING
from strategies.work_strategies.BaseTA import BaseTABitget

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

    ((MTA_KING,(100,'KING_1_MOEX_STOCK','u')),
     ('NVTK2','RUAL2','CHMF2','GAZP2','ALRS2','TRMK2','MTLR2','LSRG2','MAGN2''NMTP2','GMKN2','AFLT2','IRAO2','ROSN2','NLMK2','TATN2','AFKS2','HYDR2','PIKK2','SELG2','UPRO2','YDEX2','TRNFP2','BANEP2','RTKM2','MGNT2','SIBN2','MOEX2','MTSS2','SNGSP2','FESH2','LKOH2','CBOM2','FEES2','SBER2','VTBR2','SNGS2')),
    ((MTA_KING,(100,'KING_5_MOEX_STOCK','u')),
     ('NVTK','RUAL','CHMF','GAZP','ALRS','TRMK','MTLR','LSRG','MAGN''NMTP','GMKN','AFLT','IRAO','ROSN','NLMK','TATN','AFKS','HYDR','PIKK','SELG','UPRO','YDEX','TRNFP','BANEP','RTKM','MGNT','SIBN','MOEX','MTSS','SNGSP','FESH','LKOH','CBOM','FEES','SBER','VTBR','SNGS')),
    # ((MTA_KING,(100,'KING_1_MOEX_STOCK','u')),
    #  ('',)),
    ((MTA_KING,(100,'KING_1_MOEX_FUT','u')),
     ('CRU5','MMU5','MXU5','GZU5','SRU5','RIU5','RMU5','SiU5')),

)

# sleep_group = ()

def init_trader(ticker):
    for bt in  bot_on_ticker:
        if ticker in bt[1]:
            return bt[0]
    return (BaseTABitget,(1,))