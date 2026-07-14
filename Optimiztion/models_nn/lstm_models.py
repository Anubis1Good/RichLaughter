import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import json
import os
from typing import List, Tuple, Optional

class NLSNN1_LSTM(nn.Module):
    """
    LSTM нейросеть для анализа последовательности баров
    Вход: [batch_size, sequence_length, n_features]
    """
    
    def __init__(self, 
                 input_dim: int = 5,  # Количество признаков на бар
                 hidden_layers: List[int] = None,  # Для совместимости
                 hidden_dim: int = 64,
                 num_layers: int = 2,
                 sequence_length: int = 20,
                 output_dim: int = 5,
                 dropout: float = 0.2,
                 use_attention: bool = True,
                 bidirectional: bool = False):
        super().__init__()
        
        # Обработка hidden_layers для совместимости
        if hidden_layers is not None and len(hidden_layers) > 0:
            hidden_dim = hidden_layers[0]
            num_layers = max(1, len(hidden_layers))
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.sequence_length = sequence_length
        self.output_dim = output_dim
        self.use_attention = use_attention
        self.bidirectional = bidirectional
        
        # LSTM слой
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=bidirectional
        )
        
        # Механизм внимания
        if use_attention:
            self.attention = nn.MultiheadAttention(
                embed_dim=hidden_dim * (2 if bidirectional else 1),
                num_heads=min(4, hidden_dim),
                batch_first=True,
                dropout=dropout
            )
        
        # Размерность после LSTM
        lstm_output_dim = hidden_dim * (2 if bidirectional else 1)
        
        # Полносвязные слои
        self.fc_layers = nn.Sequential(
            nn.Linear(lstm_output_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, output_dim)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Вход: [batch_size, sequence_length, input_dim]
        Выход: [batch_size, output_dim]
        """
        # LSTM обработка
        lstm_out, (hidden, cell) = self.lstm(x)
        
        if self.use_attention:
            # Применяем самовнимание
            attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
            last_output = attn_out[:, -1, :]
        else:
            if self.bidirectional:
                # Для двунаправленного LSTM
                last_output = torch.cat([hidden[-2], hidden[-1]], dim=1)
            else:
                last_output = hidden[-1]
        
        # Принимаем решение
        output = self.fc_layers(last_output)
        return output
    
    def predict_action(self, x: torch.Tensor, use_softmax: bool = True) -> Tuple[int, torch.Tensor]:
        """Предсказание действия"""
        with torch.no_grad():
            if x.dim() == 2:
                x = x.unsqueeze(0)
            logits = self.forward(x)
            if use_softmax:
                probs = F.softmax(logits, dim=-1)
            else:
                probs = logits
            action = torch.argmax(probs, dim=-1).item()
            return action, probs.squeeze()