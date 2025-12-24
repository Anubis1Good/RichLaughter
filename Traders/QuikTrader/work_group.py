# from strategies.work_strategies.LTA import *
# from strategies.work_strategies.PTA import *
# from strategies.work_strategies.PTAX import *
# from strategies.work_strategies.STA_ca import *
# from strategies.work_strategies.STA_ml import *
# from strategies.work_strategies.STA_ca import *
# from strategies.work_strategies.OGTA import *
# from strategies.work_strategies.MTA import *
# from strategies.work_strategies.BaseTA import BaseTABitget
from strategies.work_strategies.MTA_KING import MTA_LIGHT

from Optimiztion.Optimizator1 import generate_combinations

from Traders.QuikTrader.QuikTrader1 import QuikTrader3
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
        (MTA_LIGHT,(100,'KING_5_MOEX_FUT')),
        (
            #+
            {
                'sec_code':'MMH6',
                'class_code':'SPBFUT',
                'granularity':'M5',
                'quantity':1,
                'stop_risk':350

            },
            {
                'sec_code':'GZH6',
                'class_code':'SPBFUT',
                'granularity':'M5',
                'quantity':1,
                'stop_risk':250

            },
            {
                'sec_code':'GAZPF',
                'class_code':'SPBFUT',
                'granularity':'M5',
                'quantity':1,
                'stop_risk':250

            },
            {
                'sec_code':'RMH6',
                'class_code':'SPBFUT',
                'granularity':'M5',
                'quantity':1,
                'stop_risk':300

            },
            {
                'sec_code':'SBERF',
                'class_code':'SPBFUT',
                'granularity':'M5',
                'quantity':1,
                'stop_risk':500

            },

        )
    ),
    # (
    #     (MTA_LIGHT,(100,'KING_1_MOEX_FUT')),
    #     (   
    #         #+
    #         # ('GZZ5','SPBFUT','M1',1),
    #         # ('IMOEXF','SPBFUT','M1',1),
    #         # ('NGV5','SPBFUT','M1',1),
    #     )
    # ),
)

def init_trader() -> list[QuikTrader3]:
    bots = []
    for ws,data_tickers in bot_on_ticker:
        for dt in data_tickers:
            print(dt['sec_code'],'risk:',dt['stop_risk'],ws)
            bot = QuikTrader3(
                dt['sec_code'],
                dt['class_code'],
                dt['granularity'],
                dt['quantity'],
                ws,
                True,
                stop_risk=dt['stop_risk']
            )
            bots.append(bot)
    return bots

