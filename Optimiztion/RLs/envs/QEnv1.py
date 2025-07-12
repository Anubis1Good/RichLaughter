import numpy as np
import itertools
from Loader.BitgetLoader import bitget_loader

class EnvBase:
    def __init__(self):
        self.n_actions = 0
        self.n_states = 0
        self.actions = 0
        self.combs = 0
    def reset(self):
        pass
    def print_info(self,e):
        pass
    def work_action(self,action):
        pass
    def step(self,action_agent):
        pass

class QEnv1(EnvBase):
    def __init__(self,raw_file:str,ws,param,fee=0.0002,variation_state=(0,1)):
        self.actions = list(range(5))
        # actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw')
        self.n_actions = len(self.actions)
        self.ws = ws
        n_features = ws.n_features
        self.fee = fee
        combs = list(itertools.product(variation_state,repeat=n_features))
        self.combs = np.array(combs)
        self.n_states = self.combs.shape[0]
        bot = self.ws('BTCUSDT',"1m","usdt-futures",1,*param)
        self.name_bot = str(type(ws())).split('.')[-1][:-2]
        df = bitget_loader(raw_file)
        df = bot.get_test_df(df)
        self.prices = df['close'].values  
        self.signals = df[self.ws.flags].values
        self.start_i = param[0]
        self.reset()
        self.test_result = {}

    def reset(self):
        self.i = self.start_i
        self.pos = 0
        self.open_price = 0
        self.count = 0
        self.total = 0
        self.total_per_fee = 0
        state = self.signals[self.i]
        index_state = np.where((self.combs == state).all(axis=1))[0][0]
        return index_state

    def print_info(self,e,add_info=''):
        print('E:',e,'Total:',self.total,'Count:',self.count, 'Total_per_fee:',self.total_per_fee,add_info)

    def work_action(self, action):
        """actions = (None, 'long_pw', 'short_pw', 'close_long_pw', 'close_short_pw')"""
        reward = 0
        cur_price = self.prices[self.i]
        fee = self.fee * cur_price  # fee абсолютное значение
        

        if action == 1:  # long
            if self.pos != 1:
                if self.pos == 0:
                    self.open_price = cur_price
                    reward = -self.fee * 100  # комиссия за открытие
                else:  # был шорт, закрываем его и открываем лонг
                    delta = self.open_price - cur_price  # прибыль по шорту (как при action=4)
                    self.total += delta
                    reward = ((delta - fee * 2) / cur_price) * 100   # комиссия за закрытие + открытие
                    self.open_price = cur_price  # новая цена для лонга
                self.pos = 1
                self.count += 1

        elif action == 2:  # short
            if self.pos != -1:
                if self.pos == 0:
                    self.open_price = cur_price
                    reward = -self.fee * 100  # комиссия за открытие
                else:  # был лонг, закрываем его и открываем шорт
                    delta = cur_price - self.open_price  # прибыль по лонгу (как при action=3)
                    self.total += delta
                    reward = ((delta - fee * 2) / cur_price) * 100  # комиссия за закрытие + открытие
                    self.open_price = cur_price  # новая цена для шорта
                self.pos = -1
                self.count += 1

        elif action == 3:  # close long
            if self.pos == 1:
                delta = cur_price - self.open_price
                self.total += delta
                reward = ((delta - fee) / cur_price) * 100 
                self.pos = 0

        elif action == 4:  # close short
            if self.pos == -1:
                delta = self.open_price - cur_price
                self.total += delta
                reward = ((delta - fee) / cur_price) * 100 
                self.pos = 0

        self.total_per_fee += reward
        return reward

                
    def step(self,action_agent):
        action = self.actions[action_agent]
        reward = self.work_action(action)
        self.i += 1
        cur_price = self.prices[self.i]
        done = False if self.i < len(self.signals)-1 else True
        state = self.signals[self.i]
        index_state = np.where((self.combs == state).all(axis=1))[0][0]
        if done:
            fee = self.fee * cur_price
            self.test_result = {
                'Total':self.total,
                'Count':self.count,
                'Total_fee_per':self.total_per_fee,
                'FeeBase':self.fee,
                'Fee':fee,
                'TheoryFee':self.count*fee,
                'TheoryTotalFee':self.total - self.fee,
                'TheoryTotalPer':((self.total - self.fee)/cur_price)*100
            }
        return index_state,reward,done



