def reverse_action(action:str):
    if action:
        if 'long' in action:
            action = action.replace('long','short')
        elif 'short' in action:
            action = action.replace('short','long')
    return action

def chep(row,price):
    '''check_enter_price'''
    is_ok = row['low'] < price < row['high']
    return is_ok