def universal_test_strategy(row,trades,shorts,longs,closes,equity,work_strategy):
    action = work_strategy(row)
    if action == 'long':
        if trades['pos'] == 0:
            trades['pos'] = 1
            longs.append((row.name,row['middle']))
            trades['open_price'] = row['middle']
        elif trades['pos'] == -1:
            trades['pos'] = 1
            longs.append((row.name,row['middle']))
            trades['total'] += trades['open_price'] - row['middle']
            closes.append((row.name,row['middle']))
            trades['count'] += 1
            trades['open_price'] = row['middle']
    elif action == 'short':
        if trades['pos'] == 0:
            trades['pos'] = -1
            shorts.append((row.name,row['middle']))
            trades['open_price'] = row['middle']
        elif trades['pos'] == 1:
            trades['pos'] = -1
            shorts.append((row.name,row['middle']))
            trades['total'] += row['middle'] - trades['open_price']
            closes.append((row.name,row['middle']))
            trades['open_price'] = row['middle']
            trades['count'] += 1
    elif action == 'close_long':
        if trades['pos'] == 1:
            trades['pos'] = 0
            trades['total'] += row['middle'] - trades['open_price']
            closes.append((row.name,row['middle']))
            trades['count'] += 1
    elif action == 'close_short':
        if trades['pos'] == -1:
            trades['pos'] = 0
            trades['total'] += trades['open_price'] - row['middle']
            closes.append((row.name,row['middle']))
            trades['count'] += 1
    elif action == 'close_all':
        if trades['pos'] == 1:
            trades['pos'] = 0
            trades['total'] += row['middle'] - trades['open_price']
            closes.append((row.name,row['middle']))
            trades['count'] += 1
        if trades['pos'] == -1:
            trades['pos'] = 0
            trades['total'] += trades['open_price'] - row['middle']
            closes.append((row.name,row['middle']))
            trades['count'] += 1
    else:
        pass

    equity.append(trades['total'])