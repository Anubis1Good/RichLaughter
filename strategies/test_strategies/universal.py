def t_long(row,trades,longs,closes,price):
    if trades['pos'] == 0:
        trades['pos'] = 1
        longs.append((row.name,row[price]))
        trades['open_price'] = row[price]
    elif trades['pos'] == -1:
        trades['pos'] = 1
        longs.append((row.name,row[price]))
        trades['total'] += trades['open_price'] - row[price]
        closes.append((row.name,row[price]))
        trades['count'] += 1
        trades['open_price'] = row[price]

def t_short(row,trades,shorts,closes,price):
    if trades['pos'] == 0:
        trades['pos'] = -1
        shorts.append((row.name,row[price]))
        trades['open_price'] = row[price]
    elif trades['pos'] == 1:
        trades['pos'] = -1
        shorts.append((row.name,row[price]))
        trades['total'] += row[price] - trades['open_price']
        closes.append((row.name,row[price]))
        trades['open_price'] = row[price]
        trades['count'] += 1

def t_close_long(row,trades,closes,price):
    open_price = price
    if price == 'low':
        open_price = 'high'
    elif price == 'high':
        open_price = 'low'
    if trades['pos'] == 1:
        trades['pos'] = 0
        trades['total'] += row[open_price] - trades['open_price']
        closes.append((row.name,row[price]))
        trades['count'] += 1  

def t_close_short(row,trades,closes,price):
    open_price = price
    if price == 'low':
        open_price = 'high'
    elif price == 'high':
        open_price = 'low'
    if trades['pos'] == -1:
        trades['pos'] = 0
        trades['total'] += trades['open_price'] - row[open_price]
        closes.append((row.name,row[price]))
        trades['count'] += 1 
        
def universal_test_strategy(row,trades,shorts,longs,closes,equity,work_strategy):
    action = work_strategy(row)
    if action in ('long_m','long_mt'):
        t_long(row,trades,longs,closes,'middle')
    elif action in ('short_m','short_mt'):
        t_short(row,trades,shorts,closes,'middle')
    elif action in ('close_long_m','close_long_mt'):
        t_close_long(row,trades,closes,'middle')
    elif action in ('close_short_m','close_short_mt'):
        t_close_short(row,trades,closes,'middle')
    elif action == 'long':
        t_long(row,trades,longs,closes,'high')
    elif action == 'short':
        t_short(row,trades,shorts,closes,'low')
    elif action == 'close_long':
        t_close_long(row,trades,closes,'low')
    elif action == 'close_short':
        t_close_short(row,trades,closes,'high')
    elif action == 'long_r':
        t_long(row,trades,longs,closes,'low')
    elif action == 'short_r':
        t_short(row,trades,shorts,closes,'high')
    elif action == 'close_long_r':
        t_close_long(row,trades,closes,'high')
    elif action == 'close_short_r':
        t_close_short(row,trades,closes,'low')
    elif action == 'long_ct':
        t_long(row,trades,longs,closes,'close')
    elif action == 'short_ct':
        t_short(row,trades,shorts,closes,'close')
    elif action == 'close_long_ct':
        t_close_long(row,trades,closes,'close')
    elif action == 'close_short_ct':
        t_close_short(row,trades,closes,'close')
    elif action in ('long_p','long_pw'):
        t_long(row,trades,longs,closes,'long_price')
    elif action in ('short_p','short_pw'):
        t_short(row,trades,shorts,closes,'short_price')
    elif action in ('close_long_p','close_long_pw'):
        t_close_long(row,trades,closes,'close_long_price')
    elif action in ('close_short_p','close_short_pw'):
        t_close_short(row,trades,closes,'close_short_price')
    elif action == 'close_all':
        t_close_long(row,trades,closes,'middle')
        t_close_short(row,trades,closes,'middle')
    else:
        pass

    equity.append(trades['total'])