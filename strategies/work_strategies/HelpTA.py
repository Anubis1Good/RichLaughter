from strategies.work_strategies.BaseTA import BaseTABitget

from ForBots.Indicators.classic_indicators import add_slice_df,add_enter_price2close,add_dzz_peaks,add_percent_zz_peaks
from ForBots.Indicators.pva_indicators import add_pattern18_dzz,add_pattern18_dzz_czd,add_stop_loss_p18czd

class CloseTA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df):
        return df
    def __call__(self, row, *args, **kwds):
        return 'close_all_pw'
    
class TestVTTA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df):
        # df = add_dzz_peaks(df,n_std=3,period=50)
        # df = add_pattern18_dzz_czd(df)
        # df['level_vt1'] = df['zp1']
        # df['level_vt2'] = df['zp2']
        # df['level_vt3'] = df['zp3']
        # df['level_vt4'] = df['zp4']

        df['level_vt1'] = df['high'].max()
        df['level_vt2'] = df['low'].min()
        df['level_vt3'] = df['middle'].median()
        return df
    
    def __call__(self, row, *args, **kwds):
        return 'test'

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

