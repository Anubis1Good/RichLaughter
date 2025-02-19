from utils.help_trades import reverse_action
from strategies.work_strategies.BaseTA import BaseTABitget

class OGTA1_Rails(BaseTABitget):
    def preprocessing(self, df):
        return super().preprocessing(df)

    def __call__(self, row, *args, **kwds):
        return super().__call__(row, *args, **kwds) 