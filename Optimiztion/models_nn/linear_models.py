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