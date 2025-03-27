from strategies.work_strategies.LTA import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.STA_ml import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.OGTA import *
from strategies.work_strategies.MTA import *
from strategies.work_strategies.BaseTA import BaseTABitget

from Optimiztion.Optimizator1 import generate_combinations

wss_u = []
configs = generate_combinations((
    (6,11),
    (6,11),
    (30,60),
    (30,60),
    ('DC',),
    ("rsi",),
    (0,1),
    (0,1)
))
for conf in configs:
    wss_u.append((PTA4_UNIVERSAL,conf))

bot_on_ticker = (
    ((PTA4_WDDCr,(21,30)),
     ('NVTK','RTKM','RUAL','CHMF','PIKK','MAGN')),
    ((PTA4_WDDCr,(11,30)),
     ('GAZP',)),
    ((PTA4_WDDCr,(10,20)),
     ('TRMK','LSRG')),
    ((PTA4_WDDCr,(6,30)),
     ('NMTP',)),
    # ((PTA4_WDDCrE,(6,30)),
    #  ()),
    # ((PTA4_WDDCrE,(10,20)),
    #  ()),
    ((PTA4_WDDCrVG,(11,30)),
     ('AFLT','IRAO','ROSN','VTBR',)),
    ((PTA4_WDVCr,(11,30)),
     ('NLMK','TATN',)),
    ((PTA4_WLISICA,(7,2,30)),
     ('SELG','AFKS','HYDR',)),
    # ((PTA8_WDOBBY_FREEr,(11,0.5,30)),
    #  ()),
    ((PTA8_WDOBBY_FREEr,(11,2,30)),
     ('UPRO','YDEX','TRNFP',)),
    ((PTA10_WIZARD,(30,55,3,15,20)),
     ('BANEP',)),
    ((PTA10_WIZARD,(20,55,12,25,20)),
     ('GMKN','ALRS','MGNT')),
    ((PTA10_WIZARD,(50,55,12,10,30)),
     ('MTLR','SIBN','CHMF5',)),
    ((OGTA4_DOG,(25,30)),
     ('GAZR','MOEX',)),
    ((OGTA4_DOG,(20,40)),
     ('MTSS',)),
    ((LTA_OKROSHKA,(10,15)),
     ('CNY','SNGSP',)),
    ((LTA_OKROSHKA,(10,30)),
     ('FESH',)),
    # ((LTA_SAVUNIA,(30,25)),
    #  ()),
    ((LTA_KOPATYCH,(10,40)),
     ('SNGS')),
    ((LTA_NUSHA,(10,20)),
     ()),
    ((LTA_LOSYASH,(10,45)),
     ('LKOH',)),
    # ((LTA_PIN,(10,7,50,5)),
    #  ()),
    ((LTA_PIN,(10,9,45,3)),
     ('CBOM','FEES',)),
    ((MTA_LORD,(100,wss_u,0.0002,4)),
     ('SBER','SBRF',)),
    ((MTA_LORD,(100,wss_u,0.00001,3)),
     ('MXI','RTS',)),
)

def init_trader(ticker):
    for bt in  bot_on_ticker:
        if ticker in bt[1]:
            return bt[0]
    return (BaseTABitget,(1,))