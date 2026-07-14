import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import json
import os
from typing import List, Tuple, Optional


class NLSNN1(nn.Module):
    """Простая нейросеть для торговли с настраиваемой архитектурой"""
    
    def __init__(self, 
                 input_dim: int, 
                 hidden_layers: List[int] = [64, 32],  # Пример: [64, 32] - два скрытых слоя
                 output_dim: int = 5):  # 5 действий: 0-4
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.output_dim = output_dim
        
        # Динамически создаем слои
        layers = []
        prev_dim = input_dim
        
        for i, hidden_dim in enumerate(hidden_layers):
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            prev_dim = hidden_dim
        
        # Выходной слой
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Вход: [batch_size, input_dim], Выход: [batch_size, output_dim]"""
        logits = self.network(x)
        # Можно использовать softmax или оставить logits
        return logits  # или F.softmax(logits, dim=-1) для вероятностей
    
    def predict_action(self, x: torch.Tensor, use_softmax: bool = True) -> Tuple[int, torch.Tensor]:
        """Предсказание действия для одного состояния"""
        with torch.no_grad():
            logits = self.forward(x)
            if use_softmax:
                probs = F.softmax(logits, dim=-1)
            else:
                probs = logits
            
            action = torch.argmax(probs, dim=-1).item()
            return action, probs.squeeze()
        


# class NLSNN1_LSTM(nn.Module):
#     """
#     LSTM нейросеть для анализа последовательности баров
#     Вход: [batch_size, sequence_length, n_features]
#     """
    
#     def __init__(self, 
#                  input_dim: int = 5,  # Количество признаков на бар
#                  hidden_layers: List[int] = None,  # Для совместимости
#                  hidden_dim: int = 64,
#                  num_layers: int = 2,
#                  sequence_length: int = 20,
#                  output_dim: int = 5,
#                  dropout: float = 0.2,
#                  use_attention: bool = True,
#                  bidirectional: bool = False):
#         super().__init__()
        
#         # Обработка hidden_layers для совместимости
#         if hidden_layers is not None and len(hidden_layers) > 0:
#             hidden_dim = hidden_layers[0]
#             num_layers = max(1, len(hidden_layers))
        
#         self.input_dim = input_dim
#         self.hidden_dim = hidden_dim
#         self.num_layers = num_layers
#         self.sequence_length = sequence_length
#         self.output_dim = output_dim
#         self.use_attention = use_attention
#         self.bidirectional = bidirectional
        
#         # LSTM слой
#         self.lstm = nn.LSTM(
#             input_size=input_dim,
#             hidden_size=hidden_dim,
#             num_layers=num_layers,
#             batch_first=True,
#             dropout=dropout if num_layers > 1 else 0,
#             bidirectional=bidirectional
#         )
        
#         # Механизм внимания
#         if use_attention:
#             self.attention = nn.MultiheadAttention(
#                 embed_dim=hidden_dim * (2 if bidirectional else 1),
#                 num_heads=min(4, hidden_dim),
#                 batch_first=True,
#                 dropout=dropout
#             )
        
#         # Размерность после LSTM
#         lstm_output_dim = hidden_dim * (2 if bidirectional else 1)
        
#         # Полносвязные слои
#         self.fc_layers = nn.Sequential(
#             nn.Linear(lstm_output_dim, hidden_dim),
#             nn.ReLU(),
#             nn.Dropout(dropout),
#             nn.Linear(hidden_dim, hidden_dim // 2),
#             nn.ReLU(),
#             nn.Dropout(dropout),
#             nn.Linear(hidden_dim // 2, output_dim)
#         )
    
#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         """
#         Вход: [batch_size, sequence_length, input_dim]
#         Выход: [batch_size, output_dim]
#         """
#         # LSTM обработка
#         lstm_out, (hidden, cell) = self.lstm(x)
        
#         if self.use_attention:
#             # Применяем самовнимание
#             attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
#             last_output = attn_out[:, -1, :]
#         else:
#             if self.bidirectional:
#                 # Для двунаправленного LSTM
#                 last_output = torch.cat([hidden[-2], hidden[-1]], dim=1)
#             else:
#                 last_output = hidden[-1]
        
#         # Принимаем решение
#         output = self.fc_layers(last_output)
#         return output
    
#     def predict_action(self, x: torch.Tensor, use_softmax: bool = True) -> Tuple[int, torch.Tensor]:
#         """Предсказание действия"""
#         with torch.no_grad():
#             if x.dim() == 2:
#                 x = x.unsqueeze(0)
#             logits = self.forward(x)
#             if use_softmax:
#                 probs = F.softmax(logits, dim=-1)
#             else:
#                 probs = logits
#             action = torch.argmax(probs, dim=-1).item()
#             return action, probs.squeeze()


# class NLSNN1_GRU(nn.Module):
#     """
#     GRU версия - быстрее и легче, чем LSTM
#     """
#     def __init__(self, 
#                  input_dim: int = 5,
#                  hidden_dim: int = 64,
#                  num_layers: int = 2,
#                  sequence_length: int = 20,
#                  output_dim: int = 5,
#                  dropout: float = 0.2):
#         super().__init__()
        
#         self.input_dim = input_dim
#         self.hidden_dim = hidden_dim
#         self.num_layers = num_layers
#         self.sequence_length = sequence_length
#         self.output_dim = output_dim
        
#         self.gru = nn.GRU(
#             input_size=input_dim,
#             hidden_size=hidden_dim,
#             num_layers=num_layers,
#             batch_first=True,
#             dropout=dropout if num_layers > 1 else 0
#         )
        
#         self.fc_layers = nn.Sequential(
#             nn.Linear(hidden_dim, hidden_dim // 2),
#             nn.ReLU(),
#             nn.Dropout(dropout),
#             nn.Linear(hidden_dim // 2, output_dim)
#         )
    
#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         gru_out, hidden = self.gru(x)
#         last_output = hidden[-1]  # [batch_size, hidden_dim]
#         return self.fc_layers(last_output)
    
#     def predict_action(self, x: torch.Tensor, use_softmax: bool = True) -> Tuple[int, torch.Tensor]:
#         with torch.no_grad():
#             if x.dim() == 2:
#                 x = x.unsqueeze(0)
#             logits = self.forward(x)
#             if use_softmax:
#                 probs = F.softmax(logits, dim=-1)
#             else:
#                 probs = logits
#             action = torch.argmax(probs, dim=-1).item()
#             return action, probs.squeeze()


# class NLSNN1_Transformer(nn.Module):
#     """
#     Transformer версия - для длинных последовательностей и сложных паттернов
#     """
#     def __init__(self, 
#                  input_dim: int = 5,
#                  d_model: int = 64,
#                  nhead: int = 4,
#                  num_layers: int = 3,
#                  sequence_length: int = 30,
#                  output_dim: int = 5,
#                  dropout: float = 0.1):
#         super().__init__()
        
#         self.input_dim = input_dim
#         self.d_model = d_model
#         self.sequence_length = sequence_length
#         self.output_dim = output_dim
        
#         # Входной проекционный слой
#         self.input_projection = nn.Linear(input_dim, d_model)
#         self.pos_encoding = PositionalEncoding(d_model, dropout)
        
#         # Transformer encoder
#         encoder_layer = nn.TransformerEncoderLayer(
#             d_model=d_model,
#             nhead=nhead,
#             dim_feedforward=d_model * 4,
#             dropout=dropout,
#             batch_first=True
#         )
#         self.transformer_encoder = nn.TransformerEncoder(
#             encoder_layer, 
#             num_layers=num_layers
#         )
        
#         # Выходной слой
#         self.fc = nn.Linear(d_model, output_dim)
    
#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         # Проекция и позиционное кодирование
#         x = self.input_projection(x)  # [batch, seq_len, d_model]
#         x = self.pos_encoding(x)
        
#         # Transformer
#         x = self.transformer_encoder(x)
        
#         # Берем последний выход
#         x = x[:, -1, :]
        
#         return self.fc(x)
    
#     def predict_action(self, x: torch.Tensor, use_softmax: bool = True) -> Tuple[int, torch.Tensor]:
#         with torch.no_grad():
#             if x.dim() == 2:
#                 x = x.unsqueeze(0)
#             logits = self.forward(x)
#             if use_softmax:
#                 probs = F.softmax(logits, dim=-1)
#             else:
#                 probs = logits
#             action = torch.argmax(probs, dim=-1).item()
#             return action, probs.squeeze()


# class PositionalEncoding(nn.Module):
#     """Позиционное кодирование для Transformer"""
#     def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 100):
#         super().__init__()
#         self.dropout = nn.Dropout(p=dropout)
        
#         position = torch.arange(max_len).unsqueeze(1)
#         div_term = torch.exp(torch.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
        
#         pe = torch.zeros(max_len, d_model)
#         pe[:, 0::2] = torch.sin(position * div_term)
#         pe[:, 1::2] = torch.cos(position * div_term)
#         pe = pe.unsqueeze(0)
        
#         self.register_buffer('pe', pe)
    
#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         x = x + self.pe[:, :x.size(1), :]
#         return self.dropout(x)