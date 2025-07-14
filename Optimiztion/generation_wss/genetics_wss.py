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
from typing import Dict,Union
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
        df = df.sort_values('total_min_fee',ascending=False).reset_index(drop=True)
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





class Evolutionist2:
    def __init__(self, n_individuals: int, raw_file: str, ws, param, 
                 fee: float = 0.0002,
                 variation_state: tuple = (0, 1), n_save_cores: int = 2,
                 step_save: int = 5, init_policy: Union[Dict, str, None] = None,
                 total_generations: int = 100):
        """
        Улучшенный генетический алгоритм для оптимизации торговых стратегий

        Параметры:
            n_individuals: Количество особей в популяции
            raw_file: Путь к файлу с данными
            ws: Класс стратегии
            param: Параметры стратегии
            min_fee/max_fee: Диапазон комиссий
            variation_state: Возможные значения состояний
            n_save_cores: Ядра для сохранения
            step_save: Частота сохранения
            init_policy: Начальная политика
            total_generations: Общее число поколений
        """
        # Инициализация параметров
        self.n_save_cores = n_save_cores
        self.ws = ws
        self.ts = universal_test_strategy
        self.n_features = ws.n_features
        self.n_individuals = n_individuals
        self.total_generations = total_generations
        self.current_generation = 0
        
        # Генерация состояний
        combs = list(itertools.product(variation_state, repeat=self.n_features))
        self.combs = np.array(combs)
        self.n_states = self.combs.shape[0]
        
        # Настройки генетического алгоритма
        self.elite_size = max(1, int(n_individuals * 0.1))
        self.mutation_rate = 0.15
        self.diversity_threshold = 0.5
        self.fitness_scores = {}
        
        # Инициализация политики
        self._initialize_policy(init_policy)
        
        # Настройки комиссий
        self.fee = fee / 2
        
        # Генерация популяции
        self.generation = self._initialize_population()
        
        # Загрузка данных
        self._load_data(raw_file, param)
        
        # Настройка путей сохранения
        self._setup_paths()
        self.step_save = step_save
        
    def _initialize_policy(self, init_policy):
        """Инициализация политики"""
        if isinstance(init_policy, str):
            try:
                with open(init_policy) as f:
                    self.policy = json.load(f)
            except Exception as e:
                print(f'Error loading policy: {e}')
                self.policy = self._create_default_policy()
        elif isinstance(init_policy, dict):
            self.policy = init_policy
        else:
            self.policy = self._create_default_policy()
    
    def _create_default_policy(self):
        """Создание политики по умолчанию"""
        return {
            "S": self.combs.tolist(),
            "A": np.zeros((self.n_states,), dtype=np.int8).tolist()
        }
    
    def _initialize_population(self):
        """Инициализация начальной популяции"""
        population = np.random.choice([0,1,2,3,4], (self.n_individuals, self.n_states))
        if self.policy['A'] != [0]*self.n_states:
            population[0] = self.policy['A']
        return population
    
    def _load_data(self, raw_file, param):
        """Загрузка и подготовка данных"""
        df = bitget_loader(raw_file)
        self.param = param + [self.policy]
        bot = self.ws('BTCUSDT', "1m", "usdt-futures", 1, *(self.param))
        df = bot.get_test_df(df)
        self.name_bot = str(type(self.ws())).split('.')[-1][:-2]
        self.prices = df['close'].values  
        self.signals = df[self.ws.flags].values
    
    def _setup_paths(self):
        """Настройка путей для сохранения результатов"""
        self.path = f'TestNewResults/Evolutionist2/{self.name_bot}'
        self.path_g = os.path.join(self.path, 'generations')
        self.path_bp = os.path.join(self.path, 'best_policies')
        self.path_data = os.path.join(self.path, 'data')
        self.path_checkpoints = os.path.join(self.path, 'checkpoints')
        
        for p in [self.path, self.path_g, self.path_bp, self.path_data, self.path_checkpoints]:
            os.makedirs(p, exist_ok=True)
        
        with open(os.path.join(self.path, 'Sample.json'), 'w') as f:
            json.dump(self.policy, f)

    def generate_random_policies(self, n: int) -> np.ndarray:
        """Генерация случайных политик с учетом текущего знания"""
        new = np.random.choice([0,1,2,3,4], (n, self.n_states))
        if random.random() < 0.3:  # 30% chance добавить знания из лучшей политики
            best = np.array(self.policy['A'])
            mask = np.random.choice([True, False], size=self.n_states, p=[0.2, 0.8])
            new[:, mask] = best[mask]
        return new
    
    def work_action(self, action,test_result,cur_price,pos,open_price):
        """actions = (None, 'long_pw', 'short_pw', 'close_long_pw', 'close_short_pw')"""
        reward = 0
        
        fee = self.fee * 100  # fee в %


        if action == 1:  # long
            if pos != 1:
                if pos == 0:
                    open_price = cur_price
                    reward = -fee  # комиссия за открытие
                else:  # был шорт, закрываем его и открываем лонг
                    delta = open_price - cur_price  # прибыль по шорту (как при action=4)
                    test_result['total'] += delta
                    reward = ((delta  / cur_price) * 100) - fee*2  # комиссия за закрытие + открытие
                    open_price = cur_price  # новая цена для лонга
                pos = 1
                test_result['count'] += 1

        elif action == 2:  # short
            if pos != -1:
                if pos == 0:
                    open_price = cur_price
                    reward = -fee  # комиссия за открытие
                else:  # был лонг, закрываем его и открываем шорт
                    delta = cur_price - open_price  # прибыль по лонгу (как при action=3)
                    test_result['total'] += delta
                    reward = ((delta  / cur_price) * 100) - fee*2 # комиссия за закрытие + открытие
                    open_price = cur_price  # новая цена для шорта
                pos = -1
                test_result['count'] += 1

        elif action == 3:  # close long
            if pos == 1:
                delta = cur_price - open_price
                test_result['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee
                pos = 0

        elif action == 4:  # close short
            if pos == -1:
                delta = open_price - cur_price
                test_result['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee
                pos = 0

            
        test_result['total_fee_per'] += reward
        return pos,open_price
    
    def check_strategy(self,bot):
        test_result = {
            'total':0,
            'count':0,
            'total_fee_per':0,
        }
        pos = 0
        open_price = 0
        for i in range(len(self.prices)):
            s = self.signals[i]
            S = bot.policy['S']
            A = bot.policy['A']
            index_state = np.where((S == s).all(axis=1))[0][0]
            action = A[index_state]
            cur_price = self.prices[i]
            pos,open_price = self.work_action(action,test_result,cur_price,pos,open_price)

        return test_result
    
    def process_test(self, args) -> Union[Dict, None]:
        """Оценка одной особи"""
        idx, individual, self_ref, start_idx = args
        if idx < start_idx:
            # print(idx,start_idx)
            return None
            
        self = self_ref  # получаем ссылку на экземпляр класса
        param = self.param.copy()
        param[-1]["A"] = individual
        bot = self.ws('BTCUSDT', "1m", "usdt-futures", 1, *param)
        trades = self.check_strategy(bot)
        if trades['count'] == 0:
            return None
            
        trades['name'] = idx
        return trades
    
    def calculate_fitness(self, result: Dict) -> float:
        """Расчет fitness-функции"""
        return result['total_fee_per']
        # return result['total_fee_per'] * 0.8 + np.log(result['count'] + 1) * 0.1
        
    
    def population_diversity(self) -> float:
        """Вычисление разнообразия популяции"""
        unique = len(set(tuple(ind) for ind in self.generation))
        return unique / self.n_individuals
    
    def make_step(self, old_top: pd.DataFrame = pd.DataFrame()) -> tuple:
        """Оценка поколения"""
        data = defaultdict(list)
        start_index = len(old_top.index)
        args = [(idx, individual, self, start_index) 
               for idx, individual in enumerate(self.generation)]
        
        num_processes = min(max(1, psutil.cpu_count(logical=False) - self.n_save_cores), len(self.generation))
        
        with Pool(processes=num_processes) as pool:
            results = []
            with tqdm(total=len(args), desc=f"Generation {self.current_generation}") as pbar:
                for res in pool.imap_unordered(self.process_test, args):
                    if res:
                        self.fitness_scores[res['name']] = self.calculate_fitness(res)
                        results.append(res)
                    pbar.update()
        
        # Обработка результатов
        for result in results:
            for key in result:
                data[key].append(result[key])
                
        df = pd.DataFrame(data)
        df = pd.concat([old_top, df], axis=0).drop_duplicates(subset=['total'], keep='first')
        df = df.sort_values('total_fee_per', ascending=False).reset_index(drop=True)
        df = df.head(len(df.index)//4)
        return df.head()['name'].to_numpy(), df
    
    def crossover(self, ind1: np.ndarray, ind2: np.ndarray) -> np.ndarray:
        """Улучшенное скрещивание с несколькими точками"""
        points = sorted(random.sample(range(len(ind1)), k=3))
        child = np.concatenate([
            ind1[:points[0]],
            ind2[points[0]:points[1]],
            ind1[points[1]:points[2]],
            ind2[points[2]:]
        ])
        return child
    
    def mutate(self, ind: np.ndarray) -> np.ndarray:
        mutation_rate = self.mutation_rate * (1 - self.current_generation/self.total_generations)
        new_ind = ind.copy()
        
        for i in range(len(new_ind)):
            if random.random() < mutation_rate:
                if random.random() < 0.7:  # Небольшие изменения
                    new_ind[i] += random.choice([-1, 1])
                    new_ind[i] = max(0, min(4, new_ind[i]))  # Ограничение 0-4
                else:  # Полностью новое значение
                    new_ind[i] = random.choice([0, 1, 2, 3, 4])  # ВАЖНО: выбор числа, а не списка
        return new_ind
    
    def update_generation(self, best_individuals: np.ndarray):
        """Обновление поколения с элитизмом и турнирным отбором"""
        # Сохраняем элиту
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
        self.current_generation += 1
        
        # Адаптация параметров
        self._adapt_parameters()

    
    def _adapt_parameters(self):
        """Адаптация параметров алгоритма"""
        self.mutation_rate = max(0.05, 0.2 * (1 - self.current_generation/self.total_generations))
        
    def save_files(self, df: pd.DataFrame):
        """Сохранение результатов и чекпоинта"""
        # Сохранение лучшей политики
        best_idx = df['name'].iloc[0]
        self.policy["A"] = self.generation[best_idx].astype(np.int8).tolist()
        
        t = str(int(time()))
        
        # Сохранение политики
        with open(os.path.join(self.path_bp, f'BP_{t}.json'), 'w') as f:
            json.dump(self.policy, f)
        
        # Сохранение данных
        with pd.ExcelWriter(os.path.join(self.path_data, f'Data_{t}.xlsx'), engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Results')
        
        # Сохранение поколения
        with open(os.path.join(self.path_g, f'Generation_{t}.json'), 'w') as f:
            json.dump({
                'generation': self.generation.tolist(),
                'fitness': {int(k): float(v) for k, v in self.fitness_scores.items()}
            }, f)
        
        # Чекпоинт
        self.save_checkpoint(df)
    
    def save_checkpoint(self, df: pd.DataFrame):
        """Полное сохранение состояния"""
        checkpoint = {
            'generation': self.generation.tolist(),
            'policy': self.policy,
            'fitness_scores': self.fitness_scores,
            'parameters': {
                'current_generation': self.current_generation,
                'mutation_rate': self.mutation_rate,
                'diversity': self.population_diversity()
            },
            'metadata': {
                'n_individuals': self.n_individuals,
                'n_features': self.n_features,
                'best_score': df['total_fee_per'].max()
            }
        }
        
        t = str(int(time()))
        with open(os.path.join(self.path_checkpoints, f'checkpoint_{t}.json'), 'w') as f:
            json.dump(checkpoint, f)
    
    @classmethod
    def from_checkpoint(cls, checkpoint_path: str, raw_file: str, ws, param, **kwargs):
        """Загрузка из чекпоинта"""
        with open(checkpoint_path) as f:
            data = json.load(f)
        
        # Создание экземпляра
        instance = cls(
            n_individuals=data['metadata']['n_individuals'],
            raw_file=raw_file,
            ws=ws,
            param=param,
            init_policy=data['policy'],
            **kwargs
        )
        
        # Восстановление состояния
        instance.generation = np.array(data['generation'])
        instance.fitness_scores = data['fitness_scores']
        instance.current_generation = data['parameters']['current_generation']
        instance.mutation_rate = data['parameters']['mutation_rate']
        
        return instance
    
    def evolution(self, epochs: int = 50):
        """Основной цикл эволюции"""
        print(f'\n=== Starting Evolution ===')
        print(f'Individuals: {self.n_individuals}')
        print(f'States: {self.n_states}')
        print(f'Generations: {epochs}')
        print(f'Mutation Rate: {self.mutation_rate:.2f}')
        print('='*25)
        
        start_time = time()
        df = pd.DataFrame()
        
        try:
            for epoch in range(epochs):
                print(f'\nGeneration {self.current_generation + 1}/{epochs}')
                
                # Оценка поколения
                best_individuals, df = self.make_step(df)
                
                # Сохранение
                if epoch % self.step_save == 0:
                    self.save_files(df)
                
                # Обновление поколения
                self.update_generation(best_individuals)
                # Логирование
                best = df.iloc[0]
                print(f"Best: ID={best['name']} | Percent={best['total_fee_per']:.2f} | Count={best['count']} | Total={best['total']}")
                print(f"Diversity: {self.population_diversity():.2f} | "
                      f"Mutation: {self.mutation_rate:.3f}")
                df['name'] = df.index
                
        except KeyboardInterrupt:
            print("\nEvolution interrupted by user!")
        
        # Финальное сохранение
        self.save_files(df)
        
        # Статистика
        total_time = (time() - start_time) / 3600
        print(f'\n=== Evolution Completed ===')
        print(f'Total time: {total_time:.2f} hours')
        print(f'Best Result: {df["total_fee_per"].iloc[0]:.2f}')
        print(f'Final Diversity: {self.population_diversity():.2f}')
        
        return df