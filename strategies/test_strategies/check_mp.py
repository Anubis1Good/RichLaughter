import pandas as pd
import numpy as np

def work_action_mp(need_pos, trades, cur_price, fee, fees, equity, equity_fee, pos, open_price, open_fee, row_name, longs:list, shorts:list, closes:list):
    """return pos,open_price,fees,open_fee"""
    reward = 0
    delta = 0
    feei = (fee * cur_price) / 100
    delta_pos = need_pos - pos
    
    if delta_pos > 0:  # add
        if pos > -1: # long or neutral
            if pos == 0: # new_long
                open_price = cur_price
                pos = delta_pos
                open_fee = feei * delta_pos
            else:  # change_long
                open_price = (open_price * pos + cur_price * delta_pos) / (pos + delta_pos)
                pos += delta_pos
                open_fee += feei * delta_pos
            reward = -fee * delta_pos
            fees += feei * delta_pos
            longs.append((row_name, cur_price))
            trades['count'] += 1
        else: # close_short (pos < 0)
            new_pos = delta_pos + pos
            abs_pos = abs(pos)
            
            if new_pos == 0: # close_short completely
                delta = open_price - cur_price
                trades['total'] += delta * abs_pos
                reward = (((delta / cur_price) * 100) - fee) * abs_pos
                fees += feei * delta_pos
                equity.append(equity[-1] + delta * abs_pos)
                equity_fee.append(equity_fee[-1] + (delta * abs_pos - feei * delta_pos - open_fee))
                open_fee = 0
                closes.append((row_name, cur_price))
                
            elif new_pos > 0: # close_short and open_long
                old_pos = abs(pos)
                delta = open_price - cur_price
                trades['total'] += delta * old_pos
                reward = ((delta / cur_price) * 100 * old_pos) - fee * delta_pos
                open_price = cur_price
                fees += feei * delta_pos
                equity.append(equity[-1] + delta * old_pos)
                equity_fee.append(equity_fee[-1] + (delta * old_pos - feei * delta_pos - open_fee))
                open_fee = feei * new_pos
                
            else: # change_short (reduce short)
                delta_short = abs(delta_pos)  # количество закрытых шортов
                delta = open_price - cur_price
                trades['total'] += delta * delta_short
                reward = (((delta / cur_price) * 100) - fee) * delta_short
                fees += feei * delta_pos
                equity.append(equity[-1] + delta * delta_short)
                equity_fee.append(equity_fee[-1] + (delta * delta_short - feei * delta_pos - open_fee * delta_short / abs_pos))
                # Пересчитываем open_fee для оставшейся позиции
                open_fee = open_fee * (abs(new_pos) / abs_pos)
                
            pos = new_pos
            
    elif delta_pos < 0: # sub
        if pos < 1: # short or neutral
            if pos == 0: # new_short
                open_price = cur_price
                pos = delta_pos
                open_fee = feei * abs(delta_pos)
            else:  # change_short (increase short)
                open_price = (abs(pos) * open_price + abs(delta_pos) * cur_price) / (abs(pos) + abs(delta_pos))
                pos += delta_pos
                open_fee += feei * abs(delta_pos)
            reward = -fee * abs(delta_pos)
            fees += feei * abs(delta_pos)
            shorts.append((row_name, cur_price))
            trades['count'] += 1
        else: # close_long (pos > 0)
            new_pos = delta_pos + pos
            
            if new_pos == 0: # close_long completely
                delta = cur_price - open_price
                trades['total'] += delta * pos
                reward = (((delta / cur_price) * 100) - fee) * pos
                fees += feei * abs(delta_pos)
                equity.append(equity[-1] + delta * pos)
                equity_fee.append(equity_fee[-1] + (delta * pos - feei * abs(delta_pos) - open_fee))
                open_fee = 0
                closes.append((row_name, cur_price))
                
            elif new_pos < 0: # close_long and open_short
                old_pos = pos
                delta = cur_price - open_price
                trades['total'] += delta * old_pos
                reward = ((delta / cur_price) * 100 * old_pos) - fee * abs(delta_pos)
                open_price = cur_price
                fees += feei * abs(delta_pos)
                equity.append(equity[-1] + delta * old_pos)
                equity_fee.append(equity_fee[-1] + (delta * old_pos - feei * abs(delta_pos) - open_fee))
                open_fee = feei * abs(new_pos)
                
            else: # change_long (reduce long)
                delta_long = pos - new_pos  # количество закрытых лонгов
                delta = cur_price - open_price
                trades['total'] += delta * delta_long
                reward = (((delta / cur_price) * 100) - fee) * delta_long
                fees += feei * abs(delta_pos)
                equity.append(equity[-1] + delta * delta_long)
                equity_fee.append(equity_fee[-1] + (delta * delta_long - feei * abs(delta_pos) - open_fee * delta_long / pos))
                # Пересчитываем open_fee для оставшейся позиции
                open_fee = open_fee * (new_pos / pos)
                
            pos = new_pos
            
    trades['total_fee_per'] += reward
    return pos, open_price, fees, open_fee

def check_mp_strategy_LSC(df: pd.DataFrame, work_strategy, fee=0.0002,close_2330=False):
    """
    return trades,equity,equity_fee,longs,shorts,closes
    Улучшенная версия:
    - Поддержка векторных операций.
    """
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    # Получаем сигналы
    # signals = df.apply(work_strategy, axis=1).values
    df['pos'] = df.apply(work_strategy, axis=1)
    if close_2330:
        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
        df['pos'] = np.where((df['ms'].dt.hour == 23)&(df['ms'].dt.minute > 25),0,df['pos'])
    signals = df['pos'].values

    row_names = df.index.to_series().values
    longs = []
    shorts = []
    closes = []
    prices = df['close'].values
    fee_one_p = (fee / 2) * 100
    open_fee = 0
    # from collections import defaultdict
    # debug = defaultdict(list)
    for i in range(len(signals)):
        pos, open_price, fees, open_fee = work_action_mp(
            signals[i], trades, prices[i], fee_one_p, fees, equity, equity_fee, pos, open_price,open_fee,row_names[i],longs,shorts,closes
        )
    # with open('debug.json','w') as f:
    #     import json
    #     json.dump(debug,f)
    df_eq = pd.DataFrame({'eq':equity,'eq_fee':equity_fee})
    if df_eq.empty:
        trades.update({
        'total_abs_fee': 0,
        'win_rate_wf': 0,
        'total_fee': fees,
        'mean_eq':0,
        'median_eq':0,
        'max_eq':0,
        'min_eq':0,
        'balance_eq':0,
        'mean_eqf':0,
        'median_eqf':0,
        'max_eqf':0,
        'min_eqf':0,
        'balance_eqf':0
        })
    else:
        df_eq['diff_eq'] = df_eq['eq'].diff()
        df_eq['diff_eq_fee'] = df_eq['eq_fee'].diff()
        mean_eq = df_eq['diff_eq'].mean()
        median_eq = df_eq['diff_eq'].median()
        min_eq = df_eq['diff_eq'].min()
        max_eq = df_eq['diff_eq'].max()
        mean_eqf = df_eq['diff_eq_fee'].mean()
        median_eqf = df_eq['diff_eq_fee'].median()
        min_eqf = df_eq['diff_eq_fee'].min()
        max_eqf = df_eq['diff_eq_fee'].max()
        wins = len(df_eq[df_eq['diff_eq'] > 0].index)
        loss = len(df_eq[df_eq['diff_eq'] < 0].index)
        if loss > 0:
            win_rate = round((wins / (wins + loss)) * 100,2)
        else:
            win_rate = 0

        trades['total_fee_per'] = round(trades['total_fee_per'],2)
        trades.update({
            'total_abs_fee': equity_fee[-1],
            'win_rate_wf': win_rate,
            'total_fee': fees,
            'mean_eq':mean_eq,
            'median_eq':median_eq,
            'max_eq':max_eq,
            'min_eq':min_eq,
            'balance_eq':max_eq+min_eq,
            'mean_eqf':mean_eqf,
            'median_eqf':median_eqf,
            'max_eqf':max_eqf,
            'min_eqf':min_eqf,
            'balance_eqf':max_eqf+min_eqf
        })
    longs = np.array(longs)
    shorts = np.array(shorts)
    closes = np.array(closes)
    equity = np.array(equity)
    equity_fee = np.array(equity_fee)
    return trades,equity,equity_fee,longs,shorts,closes