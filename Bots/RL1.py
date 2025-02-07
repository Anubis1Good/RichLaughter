


class RL1:
    def __init__(self,symbol,trader,strategy,work_amount,step_class):
        self.symbol = symbol
        self.trader = trader
        self.strategy = strategy
        self.work_amount = work_amount
        self.step_glass = step_class

    def open_long(self):
        self.trader.open_long(self.symbol,self.work_amount,self.step_glass)
    def open_short(self):
        self.trader.open_short(self.symbol,self.work_amount,self.step_glass)
    def close_long(self):
        self.trader.close_long(self.symbol,self.step_glass)
    def close_short(self):
        self.trader.close_short(self.symbol,self.step_glass)
    def close_all(self):
        self.trader.close_all(self.symbol,self.step_glass)

    def run(self):
        action = self.strategy()
        if action == 'long':
            self.open_long()
        elif action == 'short':
            self.open_short()
        elif action == 'close_long':
            self.close_long()
        elif action == 'close_short':
            self.close_short()
        elif action == 'close_all':
            self.close_all()
        else:
            pass
