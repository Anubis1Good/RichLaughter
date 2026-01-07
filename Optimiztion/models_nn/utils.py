import torch
import torch.nn as nn
import json
import os
from time import time
from typing import List, Optional

def save_neural_weights(model: nn.Module, 
                        filepath: str,
                        metadata: Optional[dict] = None):
    """
    Сохраняет веса нейросети с архитектурой в названии файла
    
    Формат имени файла: 
    neural_{hidden_layers_str}_{timestamp}.pth
    
    Пример: neural_64-32-16_1736251234.pth
    """
    
    # Создаем директорию если нужно
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Подготовка данных для сохранения
    save_data = {
        'state_dict': model.state_dict(),
        'input_dim': model.input_dim,
        'hidden_layers': model.hidden_layers,
        'output_dim': model.output_dim,
        'metadata': metadata or {}
    }
    
    # Сохраняем
    torch.save(save_data, filepath)
    print(f"Нейросеть сохранена: {filepath}")
    
    # Также сохраняем JSON с информацией для удобства
    info_filepath = filepath.replace('.pth', '_info.json')
    info = {
        'filepath': filepath,
        'architecture': {
            'input_dim': model.input_dim,
            'hidden_layers': model.hidden_layers,
            'output_dim': model.output_dim,
            'total_params': sum(p.numel() for p in model.parameters()),
            'trainable_params': sum(p.numel() for p in model.parameters() if p.requires_grad)
        },
        'metadata': metadata or {}
    }
    
    with open(info_filepath, 'w') as f:
        json.dump(info, f, indent=2)
    
    return filepath


def load_neural_weights(filepath: str, ModelCls:nn.Module,
                        device: str = 'cpu') -> nn.Module:
    """
    Загружает нейросеть из файла
    """
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    # Загружаем данные
    checkpoint = torch.load(filepath, map_location=device)
    
    # Создаем модель с правильной архитектурой
    model = ModelCls(
        input_dim=checkpoint['input_dim'],
        hidden_layers=checkpoint['hidden_layers'],
        output_dim=checkpoint['output_dim']
    )
    
    # Загружаем веса
    model.load_state_dict(checkpoint['state_dict'])
    model.to(device)
    model.eval()  # Переводим в режим оценки
    
    print(f"Нейросеть загружена: {filepath}")
    # print(f"Архитектура: {checkpoint['hidden_layers']}")
    
    return model, checkpoint.get('metadata', {})


def generate_neural_filename(model: nn.Module, 
                           hidden_layers: List[int], 
                           base_path: str = "modelML/_nls_models",
                           prefix: str = "evo3") -> str:
    """
    Генерирует имя файла с названием класса и архитектурой
    
    Пример: saved_models/neural_SimpleTradingNN_64-32_1736251234.pth
    """
    # Получаем имя класса модели
    class_name = model.__class__.__name__
    
    # Преобразуем архитектуру в строку
    layers_str = "-".join(str(l) for l in hidden_layers)
    
    # Текущее время для уникальности
    timestamp = str(int(time()))
    
    # Создаем имя файла
    filename = f"{prefix}_{class_name}_{layers_str}_{timestamp}.pth"
    
    # Полный путь
    full_path = os.path.join(base_path, filename)
    
    # Создаем директорию если нужно
    os.makedirs(base_path, exist_ok=True)
    
    return full_path