import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close
from Optimiztion.models_nn.linear_models import NLSNN1
from Optimiztion.models_nn.utils import load_neural_weights
from ForBots.help_func.help_nlsta1 import nlsta1_settings

def get_action5(action):
    actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw')
    return actions[action]



class NLSTA1_UNION(BaseTABitget):
    """period=20,name_settings:str='first_test',policy_model:str|nn.Module|None=None,cparams:dict={}"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,name_settings:str='first_test',policy_model:str|nn.Module|None=None,cparams:dict={}):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.name_settings = name_settings
        settings = nlsta1_settings.get(name_settings,nlsta1_settings['default']).copy()
        self.flags = settings['flags'].copy()
        self.func = settings['func']
        self.params = settings['need_params'].copy()
        self.params.update(cparams)
        self.n_features = len(self.flags)
        if policy_model:
            if isinstance(policy_model,str):
                self.policy_model,_ = load_neural_weights(policy_model,NLSNN1)
            else:
                self.policy_model = policy_model
        else:
            self.polipolicy_model = None

    def preprocessing(self, df):
        df = self.func(df,self.params)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if self.policy_model is None:
            return None
        try:
            s = row.loc[self.flags].to_numpy(dtype=np.float32)
            s = torch.tensor(s, dtype=torch.float32)
            action_idx, _ = self.policy_model.predict_action(s)
            a = get_action5(action_idx)
            # print(a,action_idx)
            return a
        except:
            return None



import torch
import numpy as np
import pandas as pd
from typing import Optional, Union, List
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df, add_enter_price2close
from Optimiztion.models_nn.lstm_models import NLSNN1_LSTM
from Optimiztion.models_nn.utils import load_neural_weights

def get_action5(action):
    actions = (None, 'long_pw', 'short_pw', 'close_long_pw', 'close_short_pw')
    return actions[action]


class NLSTA1_UNION_LSTM(BaseTABitget):
    """
    LSTM стратегия для анализа последовательности баров с direction
    
    Варианты признаков:
    1. HLVD - High, Low, Volume, Direction
    2. HLVCOD - High, Low, Volume, Close, Open, Direction
    """
    
    def __init__(self, 
                 symbol: str = "BTCUSDT", 
                 granularity: str = "1m", 
                 productType: str = "usdt-futures", 
                 n_parts: int = 1, 
                 period: int = 20,
                 name_settings: str = 'first_test',
                 policy_model: Union[str, nn.Module, None] = None,
                 sequence_length: int = 20,
                 feature_type: str = 'HLVD',  # 'HLVD' или 'HLVCOD'
                 normalize: bool = True,
                 cparams: dict = {}):
        
        super().__init__(symbol, granularity, productType, n_parts, period)
        
        self.name_settings = name_settings
        self.sequence_length = sequence_length
        self.feature_type = feature_type.upper()
        self.normalize = normalize
        
        # Определяем количество признаков
        self.n_features = self._get_feature_count()
        
        # Загружаем или создаем модель
        if policy_model:
            if isinstance(policy_model, str):
                self.policy_model, _ = load_neural_weights(policy_model, NLSNN1_LSTM)
            else:
                self.policy_model = policy_model
        else:
            self.policy_model = None
        
        # Кэш для данных
        self._cached_df = None
    
    def _get_feature_count(self) -> int:
        """Определяем количество признаков"""
        if self.feature_type == 'HLVD':
            return 4  # high, low, volume, direction
        elif self.feature_type == 'HLVCOD':
            return 6  # high, low, volume, close, open, direction
        else:
            raise ValueError(f"Unknown feature_type: {self.feature_type}. Use 'HLVD' or 'HLVCOD'")
    
    def _get_feature_columns(self) -> List[str]:
        """Возвращает список колонок для признаков"""
        if self.feature_type == 'HLVD':
            return ['high', 'low', 'volume', 'direction']
        else:  # HLVCOD
            return ['high', 'low', 'volume', 'close', 'open', 'direction']
    
    def _prepare_direction_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Подготовка direction как числового признака
        direction уже есть в данных: -1 (вниз), 1 (вверх)
        """
        df = df.copy()
        # Убеждаемся что direction есть и он в правильном формате
        if 'direction' not in df.columns:
            # Если нет direction, вычисляем по close
            df['direction'] = np.sign(df['close'].diff()).fillna(0).astype(np.int8)
        
        return df
    
    def preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Предобработка данных"""
        # Подготавливаем direction
        df = self._prepare_direction_feature(df)
        
        # Базовые колонки
        df = add_enter_price2close(df)
        df = add_slice_df(df, self.period)
        
        # Сохраняем для использования
        self._cached_df = df
        
        return df
    
    def _normalize_sequence(self, sequence: np.ndarray) -> np.ndarray:
        """
        Нормализация последовательности
        """
        if not self.normalize:
            return sequence
        
        normalized = np.zeros_like(sequence)
        
        for i in range(sequence.shape[1]):
            col = sequence[:, i]
            
            # Для direction не нормализуем (он уже в [-1, 1])
            feature_cols = self._get_feature_columns()
            if i < len(feature_cols) and feature_cols[i] == 'direction':
                normalized[:, i] = col
            else:
                mean = np.mean(col)
                std = np.std(col) + 1e-8
                normalized[:, i] = (col - mean) / std
        
        return normalized
    
    def _get_sequence_from_df(self, df: pd.DataFrame, idx: int) -> torch.Tensor:
        """
        Получение последовательности для индекса idx
        """
        # Определяем начальный индекс
        start_idx = max(0, idx - self.sequence_length + 1)
        
        # Получаем данные
        feature_cols = self._get_feature_columns()
        
        if idx - start_idx + 1 < self.sequence_length:
            # Не хватает данных - берем что есть и дополняем
            seq_df = df.iloc[start_idx:idx+1][feature_cols].copy()
            
            # Дополняем нулями
            padding = self.sequence_length - len(seq_df)
            if padding > 0:
                pad_df = pd.DataFrame(0, index=range(padding), columns=feature_cols)
                # Для direction используем 0 как нейтральное значение
                if 'direction' in pad_df.columns:
                    pad_df['direction'] = 0
                seq_df = pd.concat([pad_df, seq_df], ignore_index=True)
        else:
            # Берем ровно sequence_length последних баров
            seq_df = df.iloc[idx - self.sequence_length + 1:idx+1][feature_cols].copy()
        
        # Преобразуем в numpy array
        sequence = seq_df.values.astype(np.float32)
        
        # Нормализуем
        sequence = self._normalize_sequence(sequence)
        
        return torch.tensor(sequence, dtype=torch.float32)
    
    def __call__(self, row: pd.Series, *args, **kwds) -> Optional[str]:
        """
        Вызов стратегии для одной строки
        """
        if self.policy_model is None:
            return None
        
        try:
            # Получаем индекс
            idx = row.name if hasattr(row, 'name') else row.get('x', 0)
            
            # Получаем DataFrame
            df = self._cached_df if self._cached_df is not None else self.df
            if df is None:
                return None
            
            # Получаем последовательность
            sequence = self._get_sequence_from_df(df, idx)
            
            # Добавляем размерность батча [1, seq_len, n_features]
            if sequence.dim() == 2:
                sequence = sequence.unsqueeze(0)
            
            # Предсказываем
            action_idx, _ = self.policy_model.predict_action(sequence)
            action = get_action5(action_idx)
            
            return action
            
        except Exception as e:
            print(f"Ошибка в LSTM стратегии: {e}")
            return None
    
    def get_feature_stats(self, df: pd.DataFrame) -> dict:
        """
        Получение статистики по признакам для отладки
        """
        feature_cols = self._get_feature_columns()
        stats = {}
        
        for col in feature_cols:
            if col in df.columns:
                stats[col] = {
                    'mean': df[col].mean(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'unique_values': df[col].nunique() if col == 'direction' else 'N/A'
                }
        
        return stats


# Альтернативный вариант с дополнительной предобработкой
class NLSTA1_UNION_LSTM_ENHANCED(NLSTA1_UNION_LSTM):
    """
    Расширенная LSTM стратегия с дополнительными фичами:
    - Логарифмирование объема
    - Сглаженный direction (тренд за последние N баров)
    """
    
    def __init__(self, 
                 *args, 
                 use_log_volume: bool = True, 
                 smooth_direction: bool = True,
                 direction_window: int = 5,
                 **kwargs):
        self.use_log_volume = use_log_volume
        self.smooth_direction = smooth_direction
        self.direction_window = direction_window
        super().__init__(*args, **kwargs)
    
    def _get_feature_columns(self) -> List[str]:
        """Возвращает колонки с учетом предобработки"""
        cols = super()._get_feature_columns()
        
        # Заменяем volume на log_volume если нужно
        if self.use_log_volume and 'volume' in cols:
            cols[cols.index('volume')] = 'log_volume'
        
        # Заменяем direction на smooth_direction если нужно
        if self.smooth_direction and 'direction' in cols:
            cols[cols.index('direction')] = 'smooth_direction'
        
        return cols
    
    def preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Предобработка с дополнительными признаками"""
        # Базовое сохранение direction
        df = self._prepare_direction_feature(df)
        
        # Логарифмируем объем
        if self.use_log_volume:
            df['log_volume'] = np.log1p(df['volume'])
        
        # Сглаженный direction (тренд за последние N баров)
        if self.smooth_direction:
            # Считаем преобладающее направление за окно
            df['smooth_direction'] = df['direction'].rolling(self.direction_window).sum()
            # Нормализуем в [-1, 1]
            df['smooth_direction'] = np.clip(df['smooth_direction'] / self.direction_window, -1, 1)
            # Заполняем NaN
            df['smooth_direction'] = df['smooth_direction'].fillna(0)
        
        # Базовые колонки
        df = add_enter_price2close(df)
        df = add_slice_df(df, self.period)
        
        self._cached_df = df
        return df