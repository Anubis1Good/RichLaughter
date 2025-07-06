import os
import itertools
import pandas as pd
import numpy as np
import psutil
import random
import json
from time import time
from multiprocessing import Pool
from collections import defaultdict
from tqdm import tqdm
from Loader.BitgetLoader import bitget_loader
from strategies.test_strategies.check import check_strategy
from strategies.test_strategies.universal import universal_test_strategy

phys_cores = psutil.cpu_count(logical=False) 

class Evolutionist:
    def __init__(self,n_individuals:int,raw_file:str,ws,param,min_fee=0.0002,max_fee=0.0009,variation_state=(0,1),n_save_cores=2,step_save=5,init_policy:dict|str|None=None):
        self.n_save_cores = n_save_cores
        self.ws = ws
        self.ts = universal_test_strategy
        self.n_features = ws.n_features
        self.n_individuals = n_individuals
        combs = list(itertools.product(variation_state,repeat=self.n_features))
        self.combs = np.array(combs)
        self.n_states = self.combs.shape[0]
        if init_policy:
            if isinstance(init_policy,str):
                try:
                    with open(os.path.join(init_policy)) as f:
                        self.policy = json.load(f)
                except:
                    print('err')
                    self.policy = None
            if isinstance(init_policy,dict):
                self.policy = init_policy
        else:
            self.policy = {
                "S": combs,
                "A":np.zeros((self.n_states,),dtype=np.int8).tolist()
            }
        self.param = param + [self.policy]
        self.min_fee = min_fee
        self.max_fee = max_fee
        self.average_fee = (max_fee+min_fee)/2
        self.generation = self.generate_random_policies(self.n_individuals)
        self.generation[0] = self.policy['A']
        self.df = bitget_loader(raw_file)
        bot = self.ws('BTCUSDT',"1m","usdt-futures",1,*param)
        self.df = bot.get_test_df(self.df)
        self.name_bot = str(type(ws())).split('.')[-1][:-2]
        self.path = 'TestNewResults/Evolutionist/' + self.name_bot
        self.path_g = os.path.join(self.path,'generations')
        self.path_bp = os.path.join(self.path,'best_policies')
        self.path_data = os.path.join(self.path,'data')
        self.create_folders()
        self.step_save = step_save
        with open(os.path.join(self.path,'Sample.json'),'w') as f:
            json.dump(self.policy,f)

    def generate_random_policies(self,n_individuals):
        return np.random.choice([-1,0,1],(n_individuals,self.n_states))
    
    def process_test(self,args):
        idx, individual, self_ref,start_idx = args
        if idx < start_idx:
            return
        self = self_ref  # получаем ссылку на экземпляр класса
        param = self.param.copy()
        param[-1]["A"] = individual
        bot = self.ws('BTCUSDT', "1m", "usdt-futures", 1, *param)
        trades, longs, shorts, closes, equity = check_strategy(self.df, self.ts, bot)
        
        result = None
        if trades['count'] != 0:
            total_without_fee = (trades['total']/trades['open_price'])*100
            min_fee = trades['count']*trades['open_price']*self.min_fee
            max_fee = trades['count']*trades['open_price']*self.max_fee
            average_fee = trades['count']*trades['open_price']*self.average_fee
            
            result = {
                'name': idx,
                'total': trades['total'],
                'total_min_fee': trades['total'] - min_fee,
                'total_max_fee': trades['total'] - max_fee,
                'total_average_fee': trades['total'] - average_fee,
                'total_per': total_without_fee,
                'count': trades['count']
            }
        return result
    
    def make_step(self,old_top:pd.DataFrame=pd.DataFrame()):
        data = defaultdict(list)
        start_index = len(old_top.index) 
        args = [(idx, individual, self, start_index) for idx,individual in enumerate(self.generation)]

        # Используем количество ядер, но можно задать меньше для экономии памяти
        num_processes = min(max(1, phys_cores - self.n_save_cores), len(self.generation))
        print('Use',num_processes,'cores')
        with Pool(processes=num_processes) as pool:
            # Используем imap_unordered для более быстрого выполнения (порядок не важен)
            results = list(tqdm(pool.imap_unordered(self.process_test, args), total=self.generation.shape[0]))
            
        for result in results:
            if result:
                name_file = result['name']
                data['name'].append(name_file)
                data['total'].append(result['total'])
                data['total_min_fee'].append(result['total_min_fee'])
                data['total_max_fee'].append(result['total_max_fee'])
                data['total_average_fee'].append(result['total_average_fee'])
                data['count'].append(result['count'])
        df = pd.DataFrame(data)
        df = pd.concat([old_top,df],axis=0)
        df = df.drop_duplicates(subset=['total'], keep='first')
        df = df.sort_values('total_min_fee',axis=0,ascending=False).reset_index(drop=True)
        df = df.head(len(df.index)//4)
        best_individuals = df['name'].to_numpy()
        return best_individuals,df
    
    def crossover(self,ind1,ind2):
        new_ind = []
        for i in range(len(ind1)):
            if random.random() > 0.5:
                new_ind.append(ind1[i])
            else:
                new_ind.append(ind2[i])
        return np.array(new_ind)
    
    def mutate(sefl,ind):
        new_ind = ind.copy()
        for i in range(len(new_ind)):
            if random.random() < 0.2:
                new_ind[i] = random.choice([-1,0,1])
        return np.array(new_ind)

    def update_generation(self,best_individuals):
        best = self.generation[best_individuals].tolist()
        part = self.n_individuals//4
        halfbloods = []
        mutants = []
        for i in range(part):
            ind1 = random.choice(best)
            ind2 = random.choice(best)
            halfbloods.append(self.crossover(ind1,ind2))
            mutants.append(self.mutate(ind1))
        new_generation = best + halfbloods + mutants
        deficit = self.n_individuals - len(new_generation)
        if deficit > 0:
            newbloods = self.generate_random_policies(deficit).tolist()
            new_generation += newbloods
        self.generation = np.array(new_generation)
        

    def create_folders(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.path_data):
            os.makedirs(self.path_data)
        if not os.path.exists(self.path_bp):
            os.makedirs(self.path_bp)
        if not os.path.exists(self.path_g):
            os.makedirs(self.path_g)

    def save_files(self,df:pd.DataFrame):
        best_policy = df['name'].iloc[0]
        best_policy = self.generation[best_policy].tolist()
        self.policy["A"] = best_policy
        t = str(time())
        json_name = 'BP_' + t + '.json'
        with open(os.path.join(self.path_bp,json_name),'w') as f:
            json.dump(self.policy,f)
        doc_name = os.path.join(self.path_data, 'Data_'+ t + '.xlsx')
        with pd.ExcelWriter(doc_name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='total')
            worksheet = writer.sheets['total']
            for i, col in enumerate(df.columns,start=1):
                width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
                worksheet.set_column(i, i, width)
        individuals = {}
        for i in range(self.generation.shape[0]//10):
            individuals[i] = self.generation[i].tolist()
        json_name = 'G_' + t + '.json'
        with open(os.path.join(self.path_g,json_name),'w') as f:
            json.dump(individuals,f)
    
    def evolution(self,epoch=10):
        print('Welcome to Evolution!')
        print('N_features: ', self.n_features)
        print('START EVOLUTION!')
        start = time()
        df = pd.DataFrame()
        for i in range(epoch):
            best_individuals,df = self.make_step(df)
            if i % self.step_save == 0:
                self.save_files(df)
            self.update_generation(best_individuals)
            print('Epoch: ', i, 'Best Result: ', df['name'].iloc[0], ':',df['total_min_fee'].iloc[0], 'Count: ', df['count'].iloc[0])
            df['name'] = df.index
        print('LAST SAVE..')
        self.save_files(df)
        print('LAST SAVED..')
        print('END EVOLUTION!')
        print('Time: ',round((time()-start)/3600,2), 'hours')
