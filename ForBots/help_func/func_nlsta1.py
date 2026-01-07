from ForBots.Indicators.classic_indicators import add_rsi,add_bollinger

def first_test(df,params):
    df = add_bollinger(df,params['period'])
    df = add_rsi(df,params['period2'])
    df['sma2'] = df['close'].rolling(params['period2']).mean()
    df['C_sma'] = df['close'] > df['sma']
    df['C_sma2'] = df['close'] > df['sma2']
    df['sma_sma2'] = df['sma'] > df['sma2']
    df['H_bbu'] = df['high'] >= df['bbu']
    df['L_bbd'] = df['low'] <= df['bbd']
    df['rsi_UT'] = df['rsi'] > 100-params['threshold']
    df['rsi_DT'] = df['rsi'] < params['threshold']
    return df