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
        self.actions = list(range(6))
        # actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
        self.n_actions = len(self.actions)
        self.ws = ws
        n_features = ws.n_features
        self.fee = fee
        combs = list(itertools.product(variation_state,repeat=n_features))
        self.combs = np.array(combs)
        self.n_states = self.combs.shape[0]
        bot = self.ws('BTCUSDT',"1m","usdt-futures",1,*param)
        self.name_bot = str(type(ws())).split('.')[-1][:-2]
        self.df = bitget_loader(raw_file)
        self.df = bot.get_test_df(self.df)
        self.start_i = param[0]
        self.reset()

    def reset(self):
        self.i = self.start_i
        self.pos = 0
        self.open_price = 0
        self.count = 0
        self.total = 0
        self.total_per_fee = 0
        self.row = self.df.iloc[self.i]
        state = self.row.loc[self.ws.flags].to_numpy()
        index_state = np.where((self.combs == state).all(axis=1))[0][0]
        return index_state

    def print_info(self,e):
        print('E:',e,'Total:',self.total,'Count:',self.count, 'Total_per_fee:',self.total_per_fee)

    def work_action(self,action):
        reward = 0
        cur_price = self.row['close']
        fee = ((self.fee * cur_price) / cur_price) * 100
        if action == 1: #long
            if self.pos != 1:
                if self.pos == 0:
                    self.open_price = cur_price
                    reward = -fee
                else:
                    delta = self.open_price - cur_price
                    self.total += delta
                    reward = (delta / cur_price) * 100 - fee*2
                self.pos = 1
                self.count += 1
        elif action == 2: #short
            if self.pos != -1:
                if self.pos == 0:
                    self.open_price = cur_price
                    reward = -fee
                else:
                    delta = cur_price - self.open_price
                    self.total += delta
                    reward = (delta / cur_price) * 100 - fee*2
                self.pos = -1
                self.count += 1
        elif action >= 3: #close
            if self.pos == 1 and action != 4:
                delta = cur_price - self.open_price
                self.total += delta
                reward = (delta / cur_price) * 100 - fee
                self.pos = 0
            elif self.pos == -1 and action != 3:
                delta = self.open_price - cur_price
                self.total += delta
                reward = (delta / cur_price) * 100 - fee
                self.pos = 0
        self.total_per_fee += reward
        return reward

                
    def step(self,action_agent):
        action = self.actions[action_agent]
        reward = self.work_action(action)
        self.i += 1
        self.row = self.df.iloc[self.i]
        done = False if self.i < len(self.df.index)-1 else True
        state = self.row.loc[self.ws.flags].to_numpy()
        index_state = np.where((self.combs == state).all(axis=1))[0][0]
        return index_state,reward,done



