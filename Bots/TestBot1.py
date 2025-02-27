import traceback
from datetime import datetime
import json
import os

class TestBot1:
    def __init__(self,symbol,strategy):
        self.symbol = symbol
        self.strategy = strategy
        self.name = symbol + '_' + str(self.strategy).split(' ')[0].split('.')[-1]
        self.bid = (0,0)
        self.trades = [{
            'open_price':0,
            'open_time':str(datetime.now()),
            'count': 0,
            'pos': 0,
            'close_price':0,
            'close_time':1,
            'total':0,
            'res':0
            }
        ]
        self.len_trades = 0
        self.json_path = f'logs\OT_{self.name}.json'
        if not os.path.exists('logs'):
            os.mkdir('logs')

    def open_long(self):
        self.trades.append({
            'open_price':self.bid[1],
            'open_time':str(datetime.now()),
            'count': self.len_trades,
            'pos': 1,
            'close_price':"",
            'close_time':"",
            'total':self.trades[-1]['total'],
            'res':0
        })
    def open_short(self):
        self.trades.append({
            'open_price':self.bid[1],
            'open_time':str(datetime.now()),
            'count': self.len_trades,
            'pos': -1,
            'close_price':"",
            'close_time':"",
            'total':self.trades[-1]['total'],
            'res':0
        })
    def close_long(self):
        self.trades[-1]['close_price'] = self.bid[1]
        self.trades[-1]['res'] = self.trades[-1]['close_price'] -  self.trades[-1]['open_price'] 
        self.trades[-1]['total'] += self.trades[-1]['res']
        self.trades[-1]['close_time'] = str(datetime.now())
    def close_short(self):
        self.trades[-1]['close_price'] = self.bid[1]
        self.trades[-1]['res'] = self.trades[-1]['open_price'] - self.trades[-1]['close_price']
        self.trades[-1]['total'] += self.trades[-1]['res']
        self.trades[-1]['close_time'] = str(datetime.now())
    
    def trade_prev(self,cur_price):
        if self.bid[0] > 0:
            if cur_price < self.bid[1]:
                if self.bid[0] == 2:
                    self.close_short()
                    self.open_long()
                else:
                    if not self.trades[-1]['close_time']:
                        self.close_short()
                    else:
                        self.open_long()
        elif self.bid[0] < 0:
            if cur_price > self.bid[1]:
                if self.bid[0] == -2:
                    self.close_long()
                    self.open_short()
                else:
                    if not self.trades[-1]['close_time']:
                        self.close_long()
                    else:
                        self.open_short()
        
    def trade_next(self,action,row):
        clp = row['close_long_price']
        csp = row['close_short_price']
        lp = row['long_price']
        sp = row['short_price']
        if action:
            if 'close_long' in action:
                if self.trades[-1]['pos'] == 1 and not self.trades[-1]['close_time']:
                    self.bid = (-1,clp)
                else:
                    self.bid = (0,0)
            elif 'close_short' in action:
                if self.trades[-1]['pos'] == -1 and not self.trades[-1]['close_time']:
                    self.bid = (1,csp)
                else:
                    self.bid = (0,0)
            elif 'long' in action:
                if self.trades[-1]['pos'] == 1 and not self.trades[-1]['close_time']:
                    self.bid = (0,0)
                elif self.trades[-1]['pos'] == -1 and not self.trades[-1]['close_time']:
                    self.bid = (2,lp)
                else:
                    self.bid = (1,lp)
            elif 'short' in action:
                if self.trades[-1]['pos'] == 1 and not self.trades[-1]['close_time']:
                    self.bid = (-2,sp)
                elif self.trades[-1]['pos'] == -1 and not self.trades[-1]['close_time']:
                    self.bid = (0,0)
                else:
                    self.bid = (-1,sp)
        else:
            self.bid = (0,0)

    def write_res(self):
        len_trades = len(self.trades)
        if self.len_trades != len_trades:
            self.len_trades = len_trades
            with open(self.json_path,'w') as f:
                json.dump(self.trades,f)
    def run(self):
        try:
            row = self.strategy.get_row()
            action = self.strategy(row)
            # print("+++++++++++++++++")
            # print(row)
            # print(action)
            # print("+++++++++++++++++")
            self.trade_prev(row['close'])
            self.trade_next(action,row)
            self.write_res()
        except Exception as err:
            traceback.print_exc()


