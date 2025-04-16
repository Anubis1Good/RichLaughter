# from strategies.work_strategies.LTA import *
# from strategies.work_strategies.PTA import *
# from strategies.work_strategies.PTAX import *
# from strategies.work_strategies.STA_ca import *
# from strategies.work_strategies.STA_ml import *
# from strategies.work_strategies.STA_ca import *
# from strategies.work_strategies.OGTA import *
# from strategies.work_strategies.MTA import *
# from strategies.work_strategies.BaseTA import BaseTABitget
from strategies.work_strategies.MTA_KING import MTA_KING

from Optimiztion.Optimizator1 import generate_combinations

from Traders.QuikTrader.QuikTrader1 import QuikTrader1
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
    (
        (MTA_KING,(100,'KING_5_MOEX_FUT')),
        (
            ('MMM5','SPBFUT','M5',1),
            ('RMM5','SPBFUT','M5',1),
            ('CRM5','SPBFUT','M5',1),
            ('GZM5','SPBFUT','M5',1),
        )
    ),
)

def init_trader() -> list[QuikTrader1]:
    bots = []
    for ws,data_tickers in bot_on_ticker:
        for dt in data_tickers:
            print(dt[0],ws)
            bot = QuikTrader1(*dt,ws)
            bots.append(bot)
    return bots

