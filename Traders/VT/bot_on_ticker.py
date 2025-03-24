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
     ('NVTK','VTBR','ROSN','RTKM','RUAL',)),
    ((PTA4_WDDCr,(11,30)),
     ('FESH','GAZP')),
    ((PTA4_WDDCr,(10,20)),
     ('AFKS','HYDR','TATN','MXI','MOEX',)),
    # ((PTA4_WDDCr,(6,30)),
    #  ()),
    # ((PTA4_WDDCrE,(6,30)),
    #  ()),
    ((PTA4_WDDCrE,(10,20)),
     ('MTLR',)),
    ((PTA4_WDDCrVG,(11,30)),
     ('AFLT',)),
    # ((PTA4_WDVCr,(11,30)),
    #  ()),
    ((PTA4_WLISICA,(7,2,30)),
     ('SELG','LSRG')),
    ((PTA8_WDOBBY_FREEr,(11,0.5,30)),
     ('PIKK',)),
    ((PTA8_WDOBBY_FREEr,(11,2,30)),
     ('UPRO','YDEX',)),
    ((PTA10_WIZARD,(30,55,3,15,20)),
     ('NMTP',)),
    ((PTA10_WIZARD,(20,55,12,25,20)),
     ('ALRS','MGNT')),
    ((PTA10_WIZARD,(50,55,12,10,30)),
     ('CHMF','FEES','GMKN','SIBN')),
    ((OGTA4_DOG,(25,30)),
     ('GAZR',)),
    ((OGTA4_DOG,(20,40)),
     ('RTS','MTSS',)),
    ((LTA_OKROSHKA,(10,15)),
     ('CNY','SNGSP','MAGN')),
    # ((LTA_SAVUNIA,(30,25)),
    #  ()),
    ((LTA_KOPATYCH,(10,40)),
     ('BANEP','NLMK','SNGS')),
    ((LTA_NUSHA,(10,20)),
     ('CBOM',)),
    ((LTA_LOSYASH,(10,45)),
     ('TRMK','IRAO','LKOH',)),
    # ((LTA_PIN,(10,7,50,5)),
    #  ()),
    ((MTA_LORD,(100,wss_u,0.0002,4)),
     ('SBER','SBRF','TRNFP',)),
)

def init_trader(ticker):
    for bt in  bot_on_ticker:
        if ticker in bt[1]:
            return bt[0]
    return (BaseTABitget,(1,))