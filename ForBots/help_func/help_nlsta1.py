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
    'crysis_small': {
        'flags': [
            'C_sma',
            'C_sma2',
            'sma_sma2',
            'C_bbu',
            'C_bbd',
            'C_tbbu',
            'C_dbbu',
            'C_tbbd',
            'C_dbbd',
            'rsi',
        ],
        'func':crysis_small,
        'need_params': {
            'period_bb': 20,
            'period_rsi': 14,
            'period_sma2': 14,
        }
    },
}

