def get_action_PTA2_DDC(row,trades,shorts,longs,closes,equity):
    if row['high'] == row['max_hb']:
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
    elif row['low'] == row['min_hb']:
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
        if row['low'] <= row['avarege']:
            if trades['pos'] == -1:
                trades['pos'] = 0
                trades['total'] += row['low'] - trades['open_price']
                closes.append((row.name,row['low']))
                trades['count'] += 1
        if row['high'] >= row['avarege']:
            if trades['pos'] == 1:
                trades['pos'] = 0
                trades['total'] += trades['open_price'] - row['high']
                closes.append((row.name,row['high']))
                trades['count'] += 1

    equity.append(trades['total'])

def get_action_PTA2_BDDC(row,trades,shorts,longs,closes,equity):
    if row['high'] == row['max_hb']:
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
    elif row['low'] == row['min_hb']:
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
    else:
        if row['low'] <= row['avarege']:
            if trades['pos'] == 1:
                trades['pos'] = 0
                trades['total'] += trades['open_price'] - row['low']
                closes.append((row.name,row['low']))
                trades['count'] += 1
        if row['high'] >= row['avarege']:
            if trades['pos'] == -1:
                trades['pos'] = 0
                trades['total'] += row['high'] - trades['open_price']
                closes.append((row.name,row['high']))
                trades['count'] += 1

    equity.append(trades['total'])

def get_action_PTA2_BVGC(row,trades,shorts,longs,closes,equity):
    if row['high'] >= row['max_vg']:
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
    elif row['low'] <= row['min_vg']:
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
    else:
        if row['low'] <= row['avarege']:
            if trades['pos'] == 1:
                trades['pos'] = 0
                trades['total'] += trades['open_price'] - row['low']
                closes.append((row.name,row['low']))
                trades['count'] += 1
        if row['high'] >= row['avarege']:
            if trades['pos'] == -1:
                trades['pos'] = 0
                trades['total'] += row['high'] - trades['open_price']
                closes.append((row.name,row['high']))
                trades['count'] += 1

    equity.append(trades['total'])

