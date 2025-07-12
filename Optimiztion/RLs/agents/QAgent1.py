import os
import json
import numpy as np
from time import time
from tqdm import tqdm
from Optimiztion.RLs.utils.greeks import decay_schedule
from Optimiztion.RLs.envs.QEnv1 import EnvBase

class QAgent1:
    def __init__(self,
                 env:EnvBase,
                 gamma=1.0,
                 init_alpha=0.5,
                 min_alpha=0.01,
                 alpha_decay_ratio=0.5,
                 init_epsilon=1.0,
                 min_epsilon=0.1,
                 epsilon_decay_ration=0.9,
                 n_episodes=3000,
                 step_save=100,
                 start_q=None):
        self.env = env
        self.step_save = step_save
        self.n_episodes = n_episodes
        self.gamma = gamma
        if start_q:
            self.q = np.load(start_q)
        else:
            nS, nA = env.n_states, env.n_actions

            self.q = np.zeros((nS,nA), dtype=np.float64)
        self.alphas = decay_schedule(init_alpha,min_alpha,alpha_decay_ratio,n_episodes)
        self.epsilons = decay_schedule(init_epsilon,min_epsilon,epsilon_decay_ration,n_episodes)
        self.policy = {
                "S": env.combs.tolist(),
                "A":np.zeros((env.n_states,),dtype=np.int8).tolist()
            }
        self.path = 'TestNewResults/QLearning/' + self.env.name_bot
        self.path_bp = os.path.join(self.path,'Policies')
        self.path_q = os.path.join(self.path,'QTables')
        self.create_folders()

    def create_folders(self):
        paths = (self.path,self.path_bp,self.path_q)
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)


    def select_action(self,state,epsilon):
        if np.random.random() > epsilon:
            return np.argmax(self.q[state])
        return np.random.randint(len(self.q[state]))

    def update_q(self,e,state,action,reward,next_state,done):
        td_target = reward + self.gamma * self.q[next_state].max() * (not done)
        td_error = td_target - self.q[state][action]
        self.q[state][action] = self.q[state][action] + self.alphas[e] * td_error

    def save_files(self,prefix=''):
        t = str(time())
        json_name = prefix+'P_' + t + '.json'
        with open(os.path.join(self.path_bp,json_name),'w') as f:
            json.dump(self.policy,f)
        np.save(os.path.join(self.path_q,prefix+'QTable_'+t+'.npy'),self.q)

    def train(self):
        for e in range(self.n_episodes):
            
            state, done = self.env.reset(),False

            while not done:
                action = self.select_action(state,self.epsilons[e])
                next_state,reward,done = self.env.step(action)
                self.update_q(e,state,action,reward,next_state,done)
                state = next_state
            self.env.print_info(e)
            if e % self.step_save == 0:
                A = [int(a) for a in np.argmax(self.q,axis=1)]
                # print(A)
                # print(type(A))
                self.policy['A'] = A
                self.save_files()
        V = np.max(self.q,axis=1)
        A = [int(a) for a in np.argmax(self.q,axis=1)]
        self.policy['A'] = A
        self.save_files('L')
        # print(self.q)
        print(V)
        print(A)
        # return pi
    