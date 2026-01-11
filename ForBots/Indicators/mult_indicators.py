from ForBots.Indicators.classic_indicators import add_rsi,add_rsi_tw,add_williams_r,add_mfi,add_cci
# from ForBots.Indicators.vsa_indicators import *
# from ForBots.Indicators.rare_indicators import *
from ForBots.Indicators.pva_indicators import add_bbi
# from ForBots.Indicators.van_indicators import *
# from ForBots.Indicators.ml_indicators import *

def add_crysis_counter(df,period_rsi=14,period_bb=20):
    "add 'crysis_index'"
    df = df.copy()
    df = add_rsi(df,period_rsi)
    df = add_rsi_tw(df,period_rsi)
    df = add_bbi(df,period_bb)
    df = add_williams_r(df,period_rsi)
    df['williams_r'] = df['williams_r']/1.2 + 90
    df = add_mfi(df,period_rsi)
    df = add_cci(df,period_rsi)
    df['cci'] = df['cci']/8 +50
    df['crysis_index'] = (df['rsi'] + df['rsi_tw'] + df['bbi'] + df['williams_r'] + df['mfi'] + df['cci']) / 6
    return df