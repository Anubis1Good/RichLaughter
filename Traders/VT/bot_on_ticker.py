from strategies.work_strategies.LTA import *
from strategies.work_strategies.PTA import *
from strategies.work_strategies.PTAX import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.STA_ml import *
from strategies.work_strategies.STA_ca import *
from strategies.work_strategies.OGTA import *
from strategies.work_strategies.MTA import *
from strategies.work_strategies.BaseTA import BaseTABitget

bot_on_ticker = (
    ((PTA4_WDDCr,(21,30)),
     ('NVTK','VTBR',)),
    ((PTA4_WDDCr,(11,30)),
     ('CHMF','ALRS','GAZP')),
    ((PTA4_WDDCr,(10,20)),
     ('TATN','MXI','MOEX','FESH','YDEX')),
    ((PTA4_WDDCr,(6,30)),
     ('RTKM',)),
    ((PTA4_WDDCrE,(6,30)),
     ('MTLR',)),
    ((PTA4_WDDCrE,(10,20)),
     ('ROSN',)),
    ((PTA4_WDDCrVG,(11,30)),
     ('GAZR','HYDR','MAGN')),
    ((PTA4_WDVCr,(11,30)),
     ('RUAL','NLMK','UPRO')),
    ((PTA4_WLISICA,(7,2,30)),
     ('SELG','IRAO','LSRG')),
    ((PTA8_WDOBBY_FREEr,(11,0.5,30)),
     ('SBER',)),
    ((PTA8_WDOBBY_FREEr,(11,2,30)),
     ('SNGSP',)),
    ((PTA10_WIZARD,(30,55,3,15,20)),
     ('AFKS','CBOM','NMTP','PIKK','SIBN')),
    ((PTA10_WIZARD,(20,55,12,25,20)),
     ('CNY','FEES','MGNT')),
    ((OGTA4_DOG,(25,30)),
     ('SBRF',)),
    ((OGTA4_DOG,(20,40)),
     ('RTS',)),
    ((LTA_OKROSHKA,(10,15)),
     ('TRNFP',)),
    ((LTA_SAVUNIA,(30,25)),
     ('AFLT','MTSS','SNGS')),
    ((LTA_KOPATYCH,(10,40)),
     ('BANEP',)),
    ((LTA_NUSHA,(10,20)),
     ('LKOH',)),
    ((LTA_LOSYASH,(10,45)),
     ('TRMK',)),
    ((LTA_PIN,(10,7,50,5)),
     ('GMKN',)),
)

def init_trader(ticker):
    for bt in  bot_on_ticker:
        if ticker in bt[1]:
            return bt[0]
    return (BaseTABitget,(1,))