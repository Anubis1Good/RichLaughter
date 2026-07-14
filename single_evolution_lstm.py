def main():
    raw_file = 'DataForTests\DataMoexStock5P\_5ROSN_1_1783336759.parquet'
    
    # Общие параметры
    n_individuals = 100
    n_save_cores = 1
    step_save = 1
    epochs = 10
    
    # Параметры LSTM
    sequence_length = 20
    hidden_dim = 64
    num_layers = 2
    
    # ВЫБЕРИТЕ ВАРИАНТ:
    feature_type = 'HLVD'  # или 'HLVCOD'
    
    # Параметры стратегии
    if feature_type == 'HLVD':
        params = {
            'name_settings': 'lstm_hlvd',
            'sequence_length': sequence_length,
            'feature_type': 'HLVD',
            'normalize': True
        }
        print("Используем признаки: High, Low, Volume, Direction")
    else:  # HLVCOD
        params = {
            'name_settings': 'lstm_hlvcod',
            'sequence_length': sequence_length,
            'feature_type': 'HLVCOD',
            'normalize': True
        }
        print("Используем признаки: High, Low, Volume, Close, Open, Direction")
    
    # Создаем эволюцию с LSTM параметрами
    evo = Evolutionist4(
        n_individuals=n_individuals,
        raw_file=raw_file,
        ws_class=NLSTA1_UNION_LSTM,
        param=params,
        nn_class=NLSNN1_LSTM,
        ticker='IMOEXF',
        tf='5min',
        hidden_archs=[64, 32],  # Для совместимости
        # LSTM параметры
        lstm_hidden_dim=hidden_dim,
        lstm_num_layers=num_layers,
        lstm_sequence_length=sequence_length,
        lstm_use_attention=True,
        lstm_bidirectional=False,
        fee=0.001,
        n_save_cores=n_save_cores,
        step_save=step_save,
        need_adapt=False,
        kind_test=0,
        normalization=False,
        vtb=False,
        stop_risk=False,
        close_on_time=True,
        lower_limit=100,
        upper_limit=600
    )
    
    evo.evolution(epochs)


if __name__ == '__main__':
    from strategies.work_strategies.NLSTA import NLSTA1_UNION_LSTM
    from Optimiztion.models_nn.lstm_models import NLSNN1_LSTM
    from Optimiztion.generation_wss.Evolutionist4 import Evolutionist4
    main()