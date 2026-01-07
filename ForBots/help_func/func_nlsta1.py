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

def crysis_small(df,params):
    df = add_bollinger(df,params['period_bb'])
    df['buffer'] = (df['bbu'] - df['bbd'])/ 4
    df['tbbu'] = df['bbu'] + df['buffer']
    df['dbbu'] = df['bbu'] - df['buffer']
    df['tbbd'] = df['bbd'] + df['buffer']
    df['dbbd'] = df['bbd'] - df['buffer']
    df = add_rsi(df,params['period_rsi'])
    df['rsi'] = df['rsi']/100
    df['sma2'] = df['close'].rolling(params['period_sma2']).mean()
    df['C_sma'] = df['close'] > df['sma']
    df['C_sma2'] = df['close'] > df['sma2']
    df['sma_sma2'] = df['sma'] > df['sma2']
    df['C_bbu'] = df['close'] >= df['bbu']
    df['C_bbd'] = df['close'] >= df['bbd']
    df['C_tbbu'] = df['close'] >= df['tbbu']
    df['C_dbbu'] = df['close'] >= df['dbbu']
    df['C_tbbd'] = df['close'] >= df['tbbd']
    df['C_dbbd'] = df['close'] >= df['dbbd']
    return df