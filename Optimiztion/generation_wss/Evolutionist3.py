import os
import glob
import pandas as pd
import numpy as np
import psutil
import random
import simplejson as json
import torch
import torch.nn as nn
from time import time
from multiprocessing import Pool
from collections import defaultdict
from typing import Dict, List
from tqdm import tqdm
from strategies.test_strategies.CheckWSTrader import CheckWSTrader
from utils.work_with_dataframe.load_df import simple_load_df
from Optimiztion.models_nn.utils import load_neural_weights

phys_cores = psutil.cpu_count(logical=False)

class Evolutionist3:
    """Эволюционный алгоритм для оптимизации нейросетевых стратегий"""
    def __init__(self, 
                 n_individuals: int, 
                 raw_file: str, 
                 ws_class,  # Класс стратегии (например, NLSTA1_)
                 param: dict,  # Параметры стратегии
                 nn_class,  # Класс нейросети (например, NLSNN1)
                 ticker:str='IMOEXF',
                 tf:str='5min',
                 hidden_archs: List[int] = [64, 32],  # Архитектуры для тестирования
                 fee: float = 0.001,
                 n_save_cores: int = 2,
                 step_save: int = 5,
                 init_population_dir: str = None,  # Директория с готовыми моделями
                 need_adapt:bool=False,
                 kind_test:int = 0, #вариант теста 0 - fast, 1 - window, 2 - child
                 normalization:bool = False,
                 vtb:bool = False,
                 stop_risk:int|float|None = None,
                 window:int=60,
                 close_on_time:bool=False,
                 new_tf:str|None = None,
                 lower_limit:int|None = None,
                 upper_limit:int|None = None):
        # Базовые параметры
        self.n_individuals = n_individuals
        self.n_save_cores = n_save_cores
        self.step_save = step_save
        self.current_generation = 0
        self.ws_class = ws_class
        self.nn_class = nn_class
        self.hidden_archs = hidden_archs
        self.need_adapt = need_adapt
        #Параметры теста
        self.kind_test = kind_test
        self.normalization = normalization
        self.vtb = vtb
        self.stop_risk = stop_risk
        self.window = window
        self.close_on_time = close_on_time
        self.new_tf = new_tf
        self.ticker = ticker
        self.tf = tf
        self.lower_limit = 0 if lower_limit is None else lower_limit
        self.upper_limit = np.inf if upper_limit is None else upper_limit

        # Настройки генетического алгоритма
        self.elite_size = max(1, int(n_individuals * 0.1))
        self.mutation_rate = 0.15
        self.mutation_scale = 0.1  # Сила мутации весов
        self.fitness_scores = {}
        
        # Настройки комиссий
        self.fee = fee
        
        # Загрузка данных
        self._load_data(raw_file, param)
        
        # Определение размерности входа
        sample_bot = ws_class(self.ticker, self.tf, "usdt-futures", 1, **param)
        self.n_features = sample_bot.n_features
        
        # Инициализация популяции
        self.population = self._initialize_population(
            n_individuals, ws_class, param, nn_class, 
            init_population_dir
        )
        
        # Настройка путей сохранения
        self._setup_paths()
        
        
    def _load_data(self, raw_file: str, param: list):
        """Загрузка и подготовка данных"""
        self.df = simple_load_df(raw_file)
        
        # Создаем базовую стратегию для получения данных
        sample_bot = self.ws_class(self.ticker, self.tf, "usdt-futures", 1, **param)
        
        # Сохраняем параметры для создания ботов
        self.param = param
        
        # Получаем имя бота для путей сохранения
        self.name_bot = str(type(sample_bot)).split('.')[-1][:-2] + '_' + sample_bot.name_settings
        
    def _initialize_population(self, n_individuals, ws_class, param, nn_class, 
                             init_population_dir):
        """Инициализация популяции нейросетей"""
        population = []
        
        # Если есть директория с готовыми моделями
        if init_population_dir and os.path.exists(init_population_dir):
            population = self._load_population_from_dir(
                init_population_dir, ws_class, param
            )
        
        # Добираем случайными моделями если нужно
        remaining = n_individuals - len(population)
        if remaining > 0:
            # print(f"Создаем {remaining} случайных моделей...")
            new_bots = self._create_random_bots(
                remaining, ws_class, param, nn_class
            )
            population.extend(new_bots)
        
        # Обрезаем если перебор
        if len(population) > n_individuals:
            population = population[:n_individuals]
            
        return population
    
    def _load_population_from_dir(self, directory, ws_class, param):
        """Загрузка популяции из директории с моделями"""
        bots = []
        neural_files = glob.glob(os.path.join(directory, "*.pth"))
        
        for i, model_path in enumerate(neural_files[:self.n_individuals]):
            try:
                model,_ = load_neural_weights(model_path,self.nn_class)
                bot = ws_class(
                    self.ticker, self.tf, "usdt-futures", 1,
                    **param,
                    policy_model=model
                )
                bots.append(bot)
                print(f"Загружена модель {i+1}: {os.path.basename(model_path)}")
            except Exception as e:
                print(f"Ошибка загрузки {model_path}: {e}")
        
        return bots
    
    def _create_random_bots(self, n, ws_class, param, nn_class):
        """Создание случайных нейросетей"""
        bots = []
        
        for i in range(n):

            # Создаем нейросеть
            model = nn_class(
                input_dim=self.n_features,
                hidden_layers=self.hidden_archs,
                output_dim=5
            )
            
            # Сохраняем во временный файл
            
            # Создаем бота с этой моделью
            bot = ws_class(
                self.ticker, self.tf, "usdt-futures", 1,
                **param,
                policy_model=model
            )
            
            bots.append(bot)
        
        return bots
    
    def _setup_paths(self):
        """Настройка путей для сохранения результатов"""
        self.path = f'TestNewResults/Evolutionist3/{self.name_bot}'
        self.path_g = os.path.join(self.path, 'generations')
        self.path_models = os.path.join(self.path, 'models')  # Для сохранения нейросетей
        self.path_data = os.path.join(self.path, 'data')
        self.path_checkpoints = os.path.join(self.path, 'checkpoints')
        
        for p in [self.path, self.path_g, self.path_models, self.path_data, self.path_checkpoints]:
            os.makedirs(p, exist_ok=True)
        
        # print(f"Пути сохранения настроены: {self.path}")
    
    def process_test(self, args):
        """Оценка одной нейросетевой стратегии"""
        idx, bot, self_ref, start_idx = args
        
        if idx < start_idx:
            return None
        
        try:
            # Используем стандартную функцию проверки
            cwt = CheckWSTrader(self.df,bot,self.fee,self.ticker,self.tf,self.close_on_time,measure_time=False,use_tqdm=False,stop_risk=self.stop_risk)
            cwt.reload_data()
            if self.kind_test == 1:
                cwt.check_strategy_window(window=self.window,normalization=self.normalization,vtb=self.vtb)
            elif self.kind_test == 2:
                cwt.check_strategy_child(window=self.window,normalization=self.normalization,vtb=self.vtb)
            else:
                cwt.check_strategy_fast(self.vtb)
            
            if cwt.trade_data['count'] != 0:
                if self.upper_limit > cwt.trade_data['count'] > self.lower_limit:
                    if self.vtb:
                        fee_amount = cwt.trade_data['count'] * 2
                        total_with_fee = cwt.trade_data['step_eq_vtb'][-1]
                    else:
                        fee_amount = cwt.trade_data['fees']
                        total_with_fee = cwt.trade_data['step_eq_fee'][-1]
                    result = {
                        'name': idx,
                        'bot': bot,  # Сохраняем самого бота
                        'total': cwt.trade_data['total'],
                        'total_with_fee': total_with_fee,
                        'total_per': cwt.trade_data['total_wfees_per'],
                        'count': cwt.trade_data['count'],
                        'fee_amount': fee_amount
                    }
                    return result
                
        except Exception as e:
            print(f"Ошибка при оценке бота {idx}: {e}")
        
        return None
    
    def calculate_fitness(self, result: Dict) -> float:
        """Расчет fitness-функции"""
        # Простейшая фитнес-функция - прибыль после комиссий
        return result['total_with_fee']

        
    def make_step(self, old_top: pd.DataFrame = pd.DataFrame()):
        """Оценка поколения"""
        data = defaultdict(list)
        start_index = len(old_top.index)
        
        # Подготавливаем аргументы
        args = [(idx, bot, self, start_index) 
               for idx, bot in enumerate(self.population)]
        
        # Определяем количество процессов
        num_processes = min(
            max(1, phys_cores - self.n_save_cores), 
            len(self.population)
        )
        
        # print(f'Используем {num_processes} ядер для оценки')
        
        with Pool(processes=num_processes) as pool:
            results = []
            with tqdm(total=len(args), desc=f"Поколение {self.current_generation}") as pbar:
                for res in pool.imap_unordered(self.process_test, args):
                    if res:
                        self.fitness_scores[res['name']] = self.calculate_fitness(res)
                        results.append(res)
                    pbar.update()
        
        # Обработка результатов
        for result in results:
            for key in result:
                if key != 'bot':  # Не сохраняем объект бота в DataFrame
                    data[key].append(result[key])
        
        # Сохраняем ссылки на ботов отдельно
        # bots_dict = {r['name']: r['bot'] for r in results if 'bot' in r}
        bots_dict = {}
        for i, bot in enumerate(self.population):
            bots_dict[i] = bot  # ← ВСЕ боты!
        
        # Создаем DataFrame с результатами
        df = pd.DataFrame(data)
        if not df.empty:
            df = pd.concat([old_top, df], axis=0)
            df = df.drop_duplicates(subset=['total_with_fee', 'count'], keep='first')
            df = df.sort_values('total_with_fee', ascending=False).reset_index(drop=True)
            
            # Отбираем лучших (топ 25%)
            selection_size = max(1, len(df.index) // 4)
            df_top = df.head(selection_size)
            best_indices = df_top['name'].to_numpy()
            
            return best_indices, df, bots_dict
        else:
            return np.array([]), pd.DataFrame(), {}
    
    def crossover_neuro(self, bot1, bot2):
        """Скрещивание двух нейросетей"""
        try:
            # Получаем модели из ботов
            model1 = bot1.policy_model
            model2 = bot2.policy_model
            
            # Создаем новую модель
            child_model = self.nn_class(
                input_dim=self.n_features,
                hidden_layers=model1.hidden_layers,  # Берем архитектуру от первого родителя
                output_dim=5
            )
            
            # Uniform crossover весов
            child_state_dict = child_model.state_dict()
            state_dict1 = model1.state_dict()
            state_dict2 = model2.state_dict()
            
            for key in child_state_dict:
                if key in state_dict1 and key in state_dict2:
                    # Случайно выбираем веса от одного из родителей
                    mask = torch.rand_like(child_state_dict[key]) > 0.5
                    child_state_dict[key] = torch.where(
                        mask, state_dict1[key], state_dict2[key]
                    )
            
            child_model.load_state_dict(child_state_dict)
            
            
            # Создаем нового бота
            child_bot = self.ws_class(
                self.ticker, self.tf, "usdt-futures", 1,
                **self.param,
                policy_model=child_model
            )
            
            return child_bot
            
        except Exception as e:
            print(f"Ошибка при скрещивании: {e}")
            # В случае ошибки возвращаем копию первого бота
            return self._copy_bot(bot1)
        
    def mutate_neuro(self, bot, mutation_rate=None, mutation_scale=None):
        """Быстрая мутация на CPU"""
        if mutation_rate is None:
            mutation_rate = self.mutation_rate
        if mutation_scale is None:
            mutation_scale = self.mutation_scale
        
        try:
            model = bot.policy_model
            
            # Создаем новую модель
            mutated_model = self.nn_class(
                input_dim=self.n_features,
                hidden_layers=self.hidden_archs,  # Используем общую архитектуру
                output_dim=5
            )
            
            # Копируем веса и сразу мутируем
            with torch.no_grad():
                for param, new_param in zip(model.parameters(), mutated_model.parameters()):
                    # Копируем веса
                    new_param.data.copy_(param.data)
                    
                    # Применяем мутацию
                    if param.requires_grad:  # Мутируем только обучаемые параметры
                        mask = torch.rand_like(param.data) < mutation_rate
                        noise = torch.randn_like(param.data) * mutation_scale
                        new_param.data[mask] += noise[mask]
            
            mutated_bot = self.ws_class(
                self.ticker, self.tf, "usdt-futures", 1,
                **self.param,
                policy_model=mutated_model
            )
            
            return mutated_bot
            
        except Exception as e:
            print(f"Ошибка при быстрой мутации: {e}")
            return self._copy_bot(bot)
    
    def _copy_bot(self, bot):
        """Создание глубокой копии бота"""
        model = bot.policy_model
        
        # Создаем новую модель с теми же весами
        copied_model = self.nn_class(
            input_dim=self.n_features,
            hidden_layers=self.hidden_archs,
            output_dim=5
        )
        
        # Копируем веса
        copied_model.load_state_dict(model.state_dict().copy())
        
        # Создаем нового бота
        copied_bot = self.ws_class(
            self.ticker, self.tf, "usdt-futures", 1,
            **self.param,
            policy_model=copied_model
        )
        
        return copied_bot
    
    def update_generation(self, best_indices: np.ndarray, bots_dict: Dict):
        """Обновление поколения на основе лучших особей"""
        if len(best_indices) == 0:
            print("Нет лучших особей для отбора")
            return
        
        # Получаем лучших ботов
        best_bots = [bots_dict[idx] for idx in best_indices if idx in bots_dict]
        
        if not best_bots:
            print("Не удалось получить лучших ботов")
            return
        
        # print(f"Отобрано {len(best_bots)} лучших особей")
        
        # Стратегия обновления поколения
        new_population = []
        
        # 1. Элитизм - сохраняем лучших без изменений
        elite_size = min(len(best_bots), self.elite_size)
        new_population.extend(best_bots[:elite_size])
        # print(f"Элита: {elite_size} особей")
        
        # 2. Скрещивание лучших между собой
        crossover_count = min(len(best_bots), self.n_individuals // 3)
        for i in range(crossover_count):
            parent1 = random.choice(best_bots)
            parent2 = random.choice(best_bots)
            child = self.crossover_neuro(parent1, parent2)
            new_population.append(child)
        # print(f"Скрещивание: {crossover_count} особей")
        
        # 3. Мутация лучших
        mutate_count = min(len(best_bots), self.n_individuals // 3)
        for i in range(mutate_count):
            parent = random.choice(best_bots)
            mutated = self.mutate_neuro(parent)
            new_population.append(mutated)
        # print(f"Мутация: {mutate_count} особей")
        
        # 4. Добавляем случайные новые особи если нужно
        remaining = self.n_individuals - len(new_population)
        if remaining > 0:
            # print(f"Добавляем {remaining} случайных особей")
            random_bots = self._create_random_bots(
                remaining, self.ws_class, self.param, 
                self.nn_class
            )
            new_population.extend(random_bots)
        
        # Обновляем популяцию
        self.population = new_population
        self.current_generation += 1
        
        # Адаптируем параметры мутации
        if self.need_adapt:
            self._adapt_parameters()
    
    def _adapt_parameters(self):
        """Адаптация параметров алгоритма"""
        # Уменьшаем скорость мутации со временем
        # progress = self.current_generation / self.total_generations
        # self.mutation_rate = max(0.05, 0.2 * (1 - progress))
        # self.mutation_scale = max(0.01, 0.1 * (1 - progress))
        self.mutation_rate *= 0.99
        self.mutation_scale *= 0.99
    
    def save_files(self, df: pd.DataFrame, bots_dict: Dict):
        """Сохранение результатов - топ-5 моделей"""
        if df.empty:
            print("Нет данных для сохранения")
            return
        
        timestamp = str(int(time()))
        
        # Сохраняем топ-5 в подпапке
        saved_models = []
        top_n = min(5, len(df))
        
        for rank in range(top_n):
            idx = df['name'].iloc[rank]
            score = df['total_with_fee'].iloc[rank]
            count = df['count'].iloc[rank]
            if score < 0:
                continue
            if idx not in bots_dict:
                continue
                
            bot = bots_dict[idx]
            model = bot.policy_model
            
            if not hasattr(model, 'state_dict'):
                print(f"  Пропускаем топ-{rank+1}: нет state_dict")
                continue
            
            # ★ ИСПРАВЛЕННОЕ ИМЯ ФАЙЛА ★
            
            # Форматируем: убираем точки, заменяем минусы, добавляем ранг для уникальности
            score_str = f"{score:+.2f}".replace('.', 'p').replace('-', 'm').replace('+', '')
            count_str = str(count)
            
            model_filename = f"_total_{score_str}_count_{count_str}.pth"
            model_path = os.path.join(self.path_models, model_filename)
            
            # Сохраняем с полной информацией
            torch.save({
                'state_dict': model.state_dict(),
                'rank': rank + 1,
                'score': score,
                'generation': self.current_generation,
                'timestamp': timestamp,
                'input_dim': self.n_features,
                'hidden_layers': self.hidden_archs,
                'output_dim': 5,
                'model_class': self.nn_class.__name__,
                'count_trades': count
            }, model_path)
            
            # Проверяем сохранение
            if os.path.exists(model_path):
                file_size = os.path.getsize(model_path) / 1024  # KB
                saved_models.append({
                    'rank': rank + 1,
                    'filename': model_filename,
                    'score': df['total_with_fee'].iloc[rank],
                    'file_size_kb': round(file_size, 1)
                })
            else:
                print(f"  ОШИБКА сохранения топ-{rank+1}")
        
        
        # Сохраняем общие результаты (остальное без изменений)
        data_path = os.path.join(self.path_data, f'results_{timestamp}.xlsx')
        with pd.ExcelWriter(data_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Results', index=False)
        
        # Сохраняем информацию о поколении
        gen_info = {
            'generation': self.current_generation,
            'n_individuals': len(self.population),
            'best_score': df['total_with_fee'].iloc[0] if not df.empty else 0,
            'top5_scores': df['total_with_fee'].head(5).tolist(),
            'timestamp': timestamp,
            'saved_models': saved_models,
            'parameters': {
                'mutation_rate': self.mutation_rate,
                'mutation_scale': self.mutation_scale
            }
        }
        
        info_path = os.path.join(self.path_g, f'generation_{timestamp}.json')
        with open(info_path, 'w') as f:
            json.dump(gen_info, f, indent=2)
        
        print(f"✓ Результаты поколения {self.current_generation} сохранены")
    
    def save_checkpoint(self, df: pd.DataFrame, bots_dict: Dict):
        """Сохранение полного чекпоинта"""
        checkpoint = {
            'current_generation': self.current_generation,
            'fitness_scores': self.fitness_scores,
            'parameters': {
                'mutation_rate': self.mutation_rate,
                'mutation_scale': self.mutation_scale
            },
            'metadata': {
                'n_individuals': self.n_individuals,
                'n_features': self.n_features,
                'best_score': df['total_with_fee'].max() if not df.empty else 0,
                'ws_class': self.ws_class.__name__,
                'nn_class': self.nn_class.__name__
            }
        }
        
        # Сохраняем информацию о популяции (только пути к моделям)
        population_info = []
        for i, bot in enumerate(self.population):
            try:
                model = bot.model if hasattr(bot, 'model') else bot.policy_model
                arch_str = "-".join(str(x) for x in model.hidden_layers)
                population_info.append({
                    'index': i,
                    'architecture': arch_str,
                    'hidden_layers': model.hidden_layers
                })
            except:
                population_info.append({'index': i, 'error': 'cannot_get_info'})
        
        checkpoint['population_info'] = population_info
        
        timestamp = str(int(time()))
        checkpoint_path = os.path.join(self.path_checkpoints, f'checkpoint_{timestamp}.json')
        
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        # print(f"Чекпоинт сохранен: {checkpoint_path}")
        
        # Также сохраняем текущие результаты
        self.save_files(df, bots_dict)
    
    def evolution(self, epochs: int = 50):
        """Основной цикл эволюции с улучшенным логированием"""
        print('\n' + '='*60)
        print(f'ЗАПУСК НЕЙРО-ЭВОЛЮЦИИ: {self.name_bot}')
        print('='*60)
        print(f'Стратегия: {self.ws_class.__name__}')
        print(f'Нейросеть: {self.nn_class.__name__}')
        print(f'Особей: {self.n_individuals}')
        print(f'Признаков: {self.n_features}')
        print(f'Архитектура: {self.hidden_archs}')
        print(f'Тест: {["fast", "window", "child"][self.kind_test]}')
        print('='*60)
        
        start_time = time()
        df = pd.DataFrame()
        
        try:
            for epoch in range(epochs):
                print(f'\n--- Поколение {self.current_generation + 1}/{epochs} ---')
                
                # Оценка поколения
                best_indices, df, bots_dict = self.make_step(df)
                
                if len(best_indices) == 0:
                    print("Нет валидных результатов, пропускаем поколение")
                    continue
                
                # Сохранение
                if epoch % self.step_save == 0:
                    print("Сохранение результатов...")
                    self.save_files(df, bots_dict)
                    self.save_checkpoint(df, bots_dict)
                
                # Обновление поколения
                # print("Обновление поколения...")
                self.update_generation(best_indices, bots_dict)
                
                # Логирование
                if not df.empty:
                    best = df.iloc[0]
                    print(f"Лучший: ID={best['name']} | Прибыль={best['total_with_fee']:.2f} | Сделок={best['count']}")
                    print(f"Мутация: {self.mutation_rate:.3f} | Сила: {self.mutation_scale:.3f}")
                
                # Обновляем имена для следующей итерации
                df['name'] = df.index
                
        except KeyboardInterrupt:
            print("\nЭволюция прервана пользователем!")
            print("Сохранение текущего состояния...")
            if not df.empty:
                self.save_files(df, bots_dict if 'bots_dict' in locals() else {})
        
        # Финальное сохранение
        print("\nФинальное сохранение...")
        if not df.empty:
            self.save_files(df, bots_dict if 'bots_dict' in locals() else {})
        
        # Статистика
        total_time = (time() - start_time) / 3600
        print('\n' + '='*60)
        print('ЭВОЛЮЦИЯ ЗАВЕРШЕНА')
        print('='*60)
        print(f'Общее время: {total_time:.2f} часов')
        print(f'Пройдено поколений: {self.current_generation}')
        
        if not df.empty:
            print(f'Лучший результат: {df["total_with_fee"].iloc[0]:.2f}')
            print(f'Лучшее количество сделок: {df["count"].max()}')
        
        print('='*60)
        
        return df