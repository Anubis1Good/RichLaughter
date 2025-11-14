from datetime import datetime

def configuration_traiders(filename:str):
    fields = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            field = tuple(map(int,line.split(',')))
            fields.append(field)
    return fields

def only_close(action,hour,minute):
    now = datetime.now()
    chour = now.hour
    cminute = now.minute
    end_minute = minute + 15
    if hour == chour:
        if end_minute > cminute > minute:
            if action == 'long':
                return 'close_short'
            if action == 'short':
                return 'close_long'
        if end_minute < cminute:
            return 'close_all'
    return action