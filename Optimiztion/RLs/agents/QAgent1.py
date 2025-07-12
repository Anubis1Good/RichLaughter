import os
import json
import numpy as np
from time import time
import cupy as cp  # Основная библиотека для GPU
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
                 epsilon_decay_ratio=0.9,
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

            self.q = np.zeros((nS,nA), dtype=np.float32)
            self.q += 1e-6
        self.alphas = decay_schedule(init_alpha,min_alpha,alpha_decay_ratio,n_episodes)
        self.epsilons = decay_schedule(init_epsilon,min_epsilon,epsilon_decay_ratio,n_episodes)
        self.policy = {
            "S": self.env.combs.tolist(),
            "A": np.argmax(self.q, axis=1).astype(np.int8).tolist()  # Единый формат хранения
        }
        self.path = 'TestNewResults/QLearning/' + self.env.name_bot
        self.path_bp = os.path.join(self.path,'Policies')
        self.path_q = os.path.join(self.path,'QTables')
        self.path_tr = os.path.join(self.path,'TestResults')
        self.create_folders()

    def create_folders(self):
        paths = (self.path,self.path_bp,self.path_q,self.path_tr)
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)


    def select_action(self,state,epsilon):
        if np.random.random() > epsilon:
            return np.argmax(self.q[state])
        return np.random.randint(len(self.q[state]))

    def update_q(self, e, states, actions, rewards, next_states, dones):
        """
        Векторизованное обновление с поддержкой:
        - Индивидуальных alpha для каждого эпизода (self.alphas[e])
        - Одиночных примеров (если переданы скаляры)
        """
        # Поддержка как одиночных примеров, так и батчей
        states = np.asarray([states]).flatten()
        actions = np.asarray([actions]).flatten()
        rewards = np.asarray([rewards]).flatten()
        next_states = np.asarray([next_states]).flatten()
        dones = np.asarray([dones]).flatten()
        
        next_values = self.q[next_states].max(axis=1)
        targets = rewards + self.gamma * next_values * (~dones)
        td_errors = targets - self.q[states, actions]
        
        # Используем alpha для текущего эпизода
        self.q[states, actions] += self.alphas[e] * td_errors

    def save_files(self,prefix=''):
        t = str(int(time()))  # Целочисленная временная метка
        json_name = prefix+'P_' + t + '.json'
        with open(os.path.join(self.path_bp,json_name),'w') as f:
            json.dump(self.policy,f)
        json_name = prefix+'TR_' + t + '.json'
        with open(os.path.join(self.path_tr,json_name),'w') as f:
            json.dump(self.env.test_result,f)
        np.save(os.path.join(self.path_q,prefix+'QTable_'+t+'.npy'),self.q)


    def train(self, batch_size=32):
        # Буферы для батч-обучения
        states_buf, actions_buf = [], []
        rewards_buf, next_states_buf, dones_buf = [], [], []
        
        for e in range(self.n_episodes):
            start = time()
            state, done = self.env.reset(), False
            episode_rewards = 0
            
            while not done:
                action = self.select_action(state, self.epsilons[e])
                next_state, reward, done = self.env.step(action)
                
                # Сохраняем переход в буфер
                states_buf.append(state)
                actions_buf.append(action)
                rewards_buf.append(reward)
                next_states_buf.append(next_state)
                dones_buf.append(done)
                
                episode_rewards += reward
                state = next_state
                
                # Батч-обновление
                if len(states_buf) >= batch_size:
                    self.update_q(
                        e,
                        states=states_buf,
                        actions=actions_buf,
                        rewards=rewards_buf,
                        next_states=next_states_buf,
                        dones=dones_buf
                    )
                    # Очищаем буферы
                    states_buf, actions_buf = [], []
                    rewards_buf, next_states_buf, dones_buf = [], [], []
            
            # Обновляем оставшиеся переходы (если есть)
            if states_buf:
                self.update_q(
                    e,
                    states=states_buf,
                    actions=actions_buf,
                    rewards=rewards_buf,
                    next_states=next_states_buf,
                    dones=dones_buf
                )
                states_buf, actions_buf = [], []
                rewards_buf, next_states_buf, dones_buf = [], [], []
            
            # Логирование и сохранение
            self.env.print_info(e, f'time: {time()-start:.2f}s | reward: {episode_rewards:.2f}')
            
            if e % self.step_save == 0:
                self.policy['A'] = np.argmax(self.q, axis=1).astype(np.int8).tolist()
                self.save_files()
        
        # Финализация обучения
        V = np.max(self.q, axis=1)
        self.policy['A'] = np.argmax(self.q, axis=1).astype(np.int8).tolist()
        self.save_files('L')
        
        print("Final values:", V)
        print("Final policy:", self.policy['A'])





class QAgent1GPU:
    def __init__(self,
                 env: EnvBase,
                 gamma=1.0,
                 init_alpha=0.5,
                 min_alpha=0.01,
                 alpha_decay_ratio=0.5,
                 init_epsilon=1.0,
                 min_epsilon=0.1,
                 epsilon_decay_ratio=0.9,
                 n_episodes=3000,
                 step_save=100,
                 start_q=None):
        
        self.env = env
        self.step_save = step_save
        self.n_episodes = n_episodes
        self.gamma = gamma
        
        # Инициализация Q-таблицы на GPU
        if start_q:
            self.q = cp.asarray(np.load(start_q))  # Загрузка на GPU
        else:
            nS, nA = env.n_states, env.n_actions
            self.q = cp.zeros((nS, nA), dtype=cp.float32)
            self.q += 1e-6
        
        # CPU-параметры (оставляем на CPU для совместимости)
        self.alphas = decay_schedule(init_alpha, min_alpha, alpha_decay_ratio, n_episodes)
        self.epsilons = decay_schedule(init_epsilon, min_epsilon, epsilon_decay_ratio, n_episodes)
        
        # Политика (хранится на CPU)
        self._update_policy()
        
        # Пути для сохранения
        self.path = 'TestNewResults/QLearning/' + self.env.name_bot
        self.path_bp = os.path.join(self.path, 'Policies')
        self.path_q = os.path.join(self.path, 'QTables')
        self.path_tr = os.path.join(self.path, 'TestResults')
        self.create_folders()

    def _update_policy(self):
        """Обновление политики с переносом данных на CPU"""
        q_cpu = cp.asnumpy(self.q)  # Переносим Q-таблицу на CPU
        self.policy = {
            "S": self.env.combs.tolist(),
            "A": np.argmax(q_cpu, axis=1).astype(np.int8).tolist()
        }

    def create_folders(self):
        paths = (self.path, self.path_bp, self.path_q, self.path_tr)
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def select_action(self, state, epsilon):
        if np.random.random() > epsilon:
            return int(cp.argmax(self.q[state]))  # cp.argmax возвращает cupy массив
        return np.random.randint(self.q.shape[1])

    def update_q(self, e, states, actions, rewards, next_states, dones):
        # Конвертируем входные данные в cupy массивы
        states = cp.asarray(states, dtype=cp.int32)
        actions = cp.asarray(actions, dtype=cp.int32)
        rewards = cp.asarray(rewards, dtype=cp.float32)
        next_states = cp.asarray(next_states, dtype=cp.int32)
        dones = cp.asarray(dones, dtype=cp.bool_)
        
        # Векторизованные операции на GPU
        next_values = cp.max(self.q[next_states], axis=1)
        targets = rewards + self.gamma * next_values * (~dones)
        td_errors = targets - self.q[states, actions]
        
        # Обновление с учетом learning rate
        self.q[states, actions] += self.alphas[e] * td_errors

    def save_files(self, prefix=''):
        t = str(int(time()))
        json_name = prefix + 'P_' + t + '.json'
        
        # Перед сохранением обновляем политику
        self._update_policy()
        
        with open(os.path.join(self.path_bp, json_name), 'w') as f:
            json.dump(self.policy, f)
            
        json_name = prefix + 'TR_' + t + '.json'
        with open(os.path.join(self.path_tr, json_name), 'w') as f:
            json.dump(self.env.test_result, f)
            
        # Сохраняем Q-таблицу (переносим на CPU)
        np.save(os.path.join(self.path_q, prefix + 'QTable_' + t + '.npy'), 
                cp.asnumpy(self.q))

    def train(self, batch_size=256):  # Увеличиваем размер батча для GPU
        states_buf, actions_buf = [], []
        rewards_buf, next_states_buf, dones_buf = [], [], []
        
        for e in range(self.n_episodes):
            start = time()
            state, done = self.env.reset(), False
            episode_rewards = 0
            
            while not done:
                action = self.select_action(state, self.epsilons[e])
                next_state, reward, done = self.env.step(action)
                
                # Сохраняем переход в буфер
                states_buf.append(state)
                actions_buf.append(action)
                rewards_buf.append(reward)
                next_states_buf.append(next_state)
                dones_buf.append(done)
                
                episode_rewards += reward
                state = next_state
                
                # Батч-обновление
                if len(states_buf) >= batch_size:
                    self.update_q(
                        e,
                        states=states_buf,
                        actions=actions_buf,
                        rewards=rewards_buf,
                        next_states=next_states_buf,
                        dones=dones_buf
                    )
                    states_buf.clear()
                    actions_buf.clear()
                    rewards_buf.clear()
                    next_states_buf.clear()
                    dones_buf.clear()
            
            # Обновляем оставшиеся переходы
            if states_buf:
                self.update_q(
                    e,
                    states=states_buf,
                    actions=actions_buf,
                    rewards=rewards_buf,
                    next_states=next_states_buf,
                    dones=dones_buf
                )
                states_buf.clear()
                actions_buf.clear()
                rewards_buf.clear()
                next_states_buf.clear()
                dones_buf.clear()
            
            # Логирование
            self.env.print_info(e, f'GPU-time: {time()-start:.2f}s | reward: {episode_rewards:.2f}')
            
            if e % self.step_save == 0:
                self.save_files()
        
        # Финализация
        self.save_files('L_GPU_')
        final_values = cp.asnumpy(cp.max(self.q, axis=1))
        print("Final values:", final_values)
        print("Final policy:", self.policy['A'])