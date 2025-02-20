


class RL1:
    def __init__(self,symbol,trader,strategy,work_amount,step_class):
        self.symbol = symbol
        self.trader = trader
        self.strategy = strategy
        self.work_amount = work_amount
        self.step_glass = step_class
        self.middle_price = None
        self.long_price = None
        self.short_price = None
        self.close_long_price = None
        self.close_short_price = None

    def open_long(self):
        self.trader.open_long(self.symbol,self.work_amount,self.step_glass)
    def open_short(self):
        self.trader.open_short(self.symbol,self.work_amount,self.step_glass)
    def close_long(self):
        self.trader.close_long(self.symbol,self.step_glass)
    def close_short(self):
        self.trader.close_short(self.symbol,self.step_glass)
        
    def open_long_m(self):
        self.trader.open_long_pw(self.symbol,self.work_amount,self.middle_price)
    def open_short_m(self):
        self.trader.open_short_pw(self.symbol,self.work_amount,self.middle_price)
    def close_long_m(self):
        self.trader.close_long_pw(self.symbol,self.middle_price)
    def close_short_m(self):
        self.trader.close_short_pw(self.symbol,self.middle_price)

    def open_long_pw(self):
        self.trader.open_long_pw(self.symbol,self.work_amount,self.long_price)
    def open_short_pw(self):
        self.trader.open_short_pw(self.symbol,self.work_amount,self.short_price)
    def close_long_pw(self):
        self.trader.close_long_pw(self.symbol,self.close_long_price)
    def close_short_pw(self):
        self.trader.close_short_pw(self.symbol,self.close_long_price)

    def close_all(self):
        self.trader.close_all(self.symbol,self.step_glass)
    def none_action(self):
        self.trader.none_action(self.symbol)

    def get_price(self,row):
        self.middle_price = row['middle']
        self.long_price = row['long_price']
        self.short_price = row['short_price']
        self.close_long_price = row['close_long_price']
        self.close_short_price = row['close_short_price']

    def run(self):
        row = self.strategy.get_row()
        self.get_price(row)
        action = self.strategy(row)
        # print(action)
        if action in ('long','long_r','long_p','long_mt'):
            self.open_long()
        elif action in ('short','short_r','short_p','short_mt'):
            self.open_short()
        elif action in ('close_long','close_long_r','close_long_p','close_long_mt'):
            self.close_long()
        elif action in ('close_short','close_short_r','close_short_p','close_short_mt'):
            self.close_short()
        elif action == 'long_pw':
            self.open_long_pw()
        elif action == 'short_pw':
            self.open_short_pw()
        elif action == 'close_long_pw':
            self.close_long_pw()
        elif action == 'close_short_pw':
            self.close_short_pw()
        elif action == 'long_m':
            self.open_long_m()
        elif action == 'short_m':
            self.open_short_m()
        elif action == 'close_long_m':
            self.close_long_m()
        elif action == 'close_short_m':
            self.close_short_m()
        elif action == 'close_all':
            self.close_all()
        else:
            self.none_action()
