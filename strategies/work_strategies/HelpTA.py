from strategies.work_strategies.BaseTA import BaseTABitget

class CloseTA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df):
        return df
    def __call__(self, row, *args, **kwds):
        return 'close_all_pw'

def get_rws(original_class):
    # Создаем новое имя класса с префиксом "Rev"
    new_class_name = "Rev" + original_class.__name__
    
    # Создаем новый класс, наследуясь от оригинального
    class ReversedClass(original_class):
        def __call__(self, row, *args, **kwds):
            # Вызываем оригинальный __call__
            original_result = super().__call__(row, *args, **kwds)
            
            if original_result is None:
                return None
                
            # Меняем направления сигналов
            if 'long' in original_result:
                reversed_result = original_result.replace('long', 'short')
            elif 'short' in original_result:
                reversed_result = original_result.replace('short', 'long')
            else:
                reversed_result = original_result
                
            return reversed_result
    
    # Устанавливаем новое имя классу
    ReversedClass.__name__ = new_class_name
    ReversedClass.__qualname__ = new_class_name
    
    # Копируем docstring из оригинального класса
    ReversedClass.__doc__ = original_class.__doc__
    
    return ReversedClass