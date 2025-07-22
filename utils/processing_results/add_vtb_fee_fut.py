import pandas as pd
import re

dollar_step = 7.8

futures_fee_funcs = {
    'base': lambda total,count: total - count*2,
    r'BR..$': lambda total,count: total*100*dollar_step - count*2,
    r'ED..$': lambda total,count: total*10000*dollar_step - count*2,
    r'EURRUBF': lambda total,count: total*1000 - count*2,
    r'IMOEXF': lambda total,count: total*10 - count*2,
    r'MM..$': lambda total,count: total*10 - count*2,
    r'NG..$': lambda total,count: total*1000*dollar_step - count*2,
    r'RM..$': lambda total,count: total*2*dollar_step - count*2,
    r'RI..$': lambda total,count: total*2*dollar_step*0.1 - count*2,
    r'CNYRUBF': lambda total,count: total*1000 - count*2,
    r'CR..$': lambda total,count: total*1000 - count*2,
}

tests = ('BR','BRQ5','BQR5','BRU5','BRQ51')
def get_func_vtb_fee(name):
    for fff in futures_fee_funcs:
        if re.match(fff,name):
            return futures_fee_funcs[fff]
    return futures_fee_funcs['base']

# print(get_func_vtb_fee('RMU5')(1000,100))