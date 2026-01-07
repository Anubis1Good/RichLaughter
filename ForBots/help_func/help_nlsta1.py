from ForBots.help_func.func_nlsta1 import *
nlsta1_settings = {
    'default': {
        'flags': [],
        'func':lambda df,params:df,
        'need_params': {}
    },
    'first_test': {
        'flags': [
            'C_sma',
            'C_sma2',
            'sma_sma2',
            'H_bbu',
            'L_bbd',
            'rsi_UT',
            'rsi_DT'
        ],
        'func':first_test,
        'need_params': {
            'period': 20,
            'period2': 10,
            'threshold': 30
        }
    },
}

