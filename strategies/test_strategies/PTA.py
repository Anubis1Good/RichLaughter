def get_action_PTA2_DDC(row,trades,shorts,longs,closes,equity,work_strategy):
    action = work_strategy(row)
    if action == 'short':
        if trades['pos'] == 0:
            trades['pos'] = -1
            shorts.append((row.name,row['high']))
            trades['open_price'] = row['high']
        elif trades['pos'] == 1:
            trades['pos'] = -1
            shorts.append((row.name,row['high']))
            trades['total'] += row['high'] - trades['open_price']
            closes.append((row.name,row['high']))
            trades['open_price'] = row['high']
            trades['count'] += 1
    elif action == 'long':
        if trades['pos'] == 0:
            trades['pos'] = 1
            longs.append((row.name,row['low']))
            trades['open_price'] = row['low']
        elif trades['pos'] == -1:
            trades['pos'] = 1
            longs.append((row.name,row['low']))
            trades['total'] += trades['open_price'] - row['low']
            closes.append((row.name,row['low']))
            trades['count'] += 1
            trades['open_price'] = row['low']
    else:
        if action == 'close_short':
            if trades['pos'] == -1:
                trades['pos'] = 0
                trades['total'] += row['low'] - trades['open_price']
                closes.append((row.name,row['low']))
                trades['count'] += 1
        if action == 'close_long':
            if trades['pos'] == 1:
                trades['pos'] = 0
                trades['total'] += trades['open_price'] - row['high']
                closes.append((row.name,row['high']))
                trades['count'] += 1

    equity.append(trades['total'])

def get_action_PTA2_BDDC(row,trades,shorts,longs,closes,equity,work_strategy):
    action = work_strategy(row)
    if action == 'long':
        if trades['pos'] == 0:
            trades['pos'] = 1
            longs.append((row.name,row['high']))
            trades['open_price'] = row['high']
        elif trades['pos'] == -1:
            trades['pos'] = 1
            longs.append((row.name,row['high']))
            trades['total'] += trades['open_price'] - row['high']
            closes.append((row.name,row['high']))
            trades['count'] += 1
            trades['open_price'] = row['high']
    elif action == 'short':
        if trades['pos'] == 0:
            trades['pos'] = -1
            shorts.append((row.name,row['low']))
            trades['open_price'] = row['low']
        elif trades['pos'] == 1:
            trades['pos'] = -1
            shorts.append((row.name,row['low']))
            trades['total'] += row['low'] - trades['open_price']
            closes.append((row.name,row['low']))
            trades['open_price'] = row['low']
            trades['count'] += 1
    elif action == 'close_long':
        if trades['pos'] == 1:
            trades['pos'] = 0
            trades['total'] += trades['open_price'] - row['low']
            closes.append((row.name,row['low']))
            trades['count'] += 1
    elif action == 'close_short':
        if trades['pos'] == -1:
            trades['pos'] = 0
            trades['total'] += row['high'] - trades['open_price']
            closes.append((row.name,row['high']))
            trades['count'] += 1
    elif action == 'close_all':
        pass
    else:
        pass
    equity.append(trades['total'])

def get_action_PTA2_BVGC(row,trades,shorts,longs,closes,equity,work_strategy):
    action = work_strategy(row)
    if action == 'long':
        if trades['pos'] == 0:
            trades['pos'] = 1
            longs.append((row.name,row['high']))
            trades['open_price'] = row['high']
        elif trades['pos'] == -1:
            trades['pos'] = 1
            longs.append((row.name,row['high']))
            trades['total'] += trades['open_price'] - row['high']
            closes.append((row.name,row['high']))
            trades['count'] += 1
            trades['open_price'] = row['high']
    elif action == 'short':
        if trades['pos'] == 0:
            trades['pos'] = -1
            shorts.append((row.name,row['low']))
            trades['open_price'] = row['low']
        elif trades['pos'] == 1:
            trades['pos'] = -1
            shorts.append((row.name,row['low']))
            trades['total'] += row['low'] - trades['open_price']
            closes.append((row.name,row['low']))
            trades['open_price'] = row['low']
            trades['count'] += 1
    elif action == 'close_long':
        if trades['pos'] == 1:
            trades['pos'] = 0
            trades['total'] += trades['open_price'] - row['low']
            closes.append((row.name,row['low']))
            trades['count'] += 1
    elif action == 'close_short':
        if trades['pos'] == -1:
            trades['pos'] = 0
            trades['total'] += row['high'] - trades['open_price']
            closes.append((row.name,row['high']))
            trades['count'] += 1
    elif action == 'close_all':
        pass
    else:
        pass

    equity.append(trades['total'])

