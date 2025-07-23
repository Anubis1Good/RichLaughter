import numpy as np
import pandas as pd
from strategies.work_strategies.BaseTA import BaseTABitget
from ForBots.Indicators.classic_indicators import add_slice_df,add_ema,add_enter_price2close,add_rsi,add_dzz_peaks,add_donchan_channel
from ForBots.Indicators.rare_indicators import add_dynamic_trend_lines_slope_reversed,add_segmented_regression_from_end
from ForBots.Indicators.ml_indicators import add_find_similar_pattern_lite,add_linear_regression_last_row,add_ideal_pos

class STAML2_CHAOS(BaseTABitget):
    """ period=60,min_points=2,divider=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=2,divider=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.divider = divider
    def preprocessing(self, df):
        df = add_dynamic_trend_lines_slope_reversed(df,self.min_points,self.divider)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['trend_up_combined'] < row['trend_down_combined']:
            if row['trend_down_combined'] < row['close']:
                return 'short_pw'
            if row['trend_up_combined'] > row['close']:
                return 'long_pw'
            
class STAML2_FLUX(BaseTABitget):
    """period=60,threshold=0.1,min_points=2,divider=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,threshold=0.1,min_points=2,divider=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.divider = divider
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_dynamic_trend_lines_slope_reversed(df,self.min_points,self.divider)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['trend_up_combined'] < row['trend_down_combined']:
            if row['trend_down_combined'] < row['close']:
                if row['trend_mean_slope'] < self.threshold:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
            if row['trend_up_combined'] > row['close']:
                if row['trend_mean_slope'] > -self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
                
class STAML2_LEGACY(BaseTABitget):
    """period=60,threshold=0.1,min_points=5,multiplier=1"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,threshold=0.1,min_points=5,multiplier=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.threshold = threshold
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_segmented_regression_from_end(df,self.period,self.multiplier,self.min_points)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['upper_channel'] < row['close']:
            if row['regression_slope'] < self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
        if row['lower_channel'] > row['close']:
            if row['regression_slope'] > -self.threshold:
                return 'long_pw'
            else:
                return 'close_short_pw'
                
class STAML2_TRADITION(BaseTABitget):
    """period=60,min_points=5,multiplier=1"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=5,multiplier=1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_segmented_regression_from_end(df,self.period,self.multiplier,self.min_points)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['upper_channel'] < row['close']:
            return 'short_pw'
        if row['lower_channel'] > row['close']:
            return 'long_pw'
        
class STAML2_NEWAVE(BaseTABitget):
    """period=60,min_points=5,multiplier=1,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=5,multiplier=1,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.multiplier = multiplier
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_segmented_regression_from_end(df,self.period,self.multiplier,self.min_points)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['upper_channel'] < row['close']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
        if row['lower_channel'] > row['close']:
            if row['rsi'] < self.threshold:
                return 'long_pw'

class STAML2_BALANCE(BaseTABitget):
    """ period=60,min_points=2,divider=30,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=2,divider=30,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.divider = divider
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_dynamic_trend_lines_slope_reversed(df,self.min_points,self.divider)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['trend_up_combined'] < row['trend_down_combined']:
            if row['trend_down_combined'] < row['close']:
                if row['rsi'] > 100-self.threshold:
                    return 'short_pw'
            if row['trend_up_combined'] > row['close']:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
            
class STAML2_GOLDENMEAN(BaseTABitget):
    """ period=60,min_points=2,divider=30,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=2,divider=30,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.divider = divider
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_dynamic_trend_lines_slope_reversed(df,self.min_points,self.divider)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['trend_up_combined'] < row['trend_down_combined']:
            if row['trend_down_combined'] < row['close']:
                if row['rsi'] > 100-self.threshold:
                    return 'short_pw'
                else:
                    return 'close_long_pw'
            if row['trend_up_combined'] > row['close']:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
            

class STAML2_SID(BaseTABitget):
    """period=200,window=10,forecast_length=5,threshold=30,percent_threshold=0.1
    \n
    """
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=200,window=10,forecast_length=5,threshold=30,percent_threshold=0.1):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.window = window
        self.forecast_length = forecast_length
        self.threshold = threshold
        self.percent_threshold = percent_threshold
    def preprocessing(self, df):
        df = add_rsi(df,self.window)
        df = add_find_similar_pattern_lite(df,self.window,self.period,forecast_length=self.forecast_length)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, period=self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row is None:
            return None
        delta_fc = (row['forecast_high'] - row['forecast_low'])/10
        if row['close'] > row['forecast_high'] - delta_fc :
            if row['per_fs'] > self.percent_threshold and row['rsi'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'
        if row['close'] < row['forecast_low'] + delta_fc :
            if row['per_fs'] > self.percent_threshold and row['rsi'] < self.threshold:
                return 'long_pw'
            else:
                return 'close_short_pw'
            

class STAML2_KAMIKAZE(BaseTABitget):
    """period=60,threshold=30"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_linear_regression_last_row(df,self.period)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['regression_angle'] < -self.threshold:
            return 'short_pw'
        if row['regression_angle'] > self.threshold:
            return 'long_pw'
        
class STAML2_TRENDWAVE(BaseTABitget):
    """period=60,min_points=5,multiplier=1,threshold_enter=40,threshold_exit=20"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60,min_points=5,multiplier=1,threshold_enter=40,threshold_exit=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.min_points = min_points
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
    def preprocessing(self, df):
        df = add_segmented_regression_from_end(df,self.period,self.multiplier,self.min_points)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df) 
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['upper_channel'] < row['close']:
            if row['rsi'] > 100-self.threshold_enter and row['regression_slope'] < 0:
                return 'short_pw'
            if row['rsi'] > 100-self.threshold_exit:
                return 'close_long_pw'
        if row['lower_channel'] > row['close']:
            if row['rsi'] < self.threshold_enter and row['regression_slope'] > 0:
                return 'long_pw'
            if row['rsi'] < self.threshold_exit:
                return 'close_short_pw'
            
from sklearn.tree import DecisionTreeClassifier,plot_tree

class STAML2a_(BaseTABitget):
    """period=60, n_std=3"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60, n_std=3,max_depth=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_std = n_std
        self.model = None
        self.max_depth = max_depth
    def get_model(self, X_train, y_train):
        if self.max_depth:
            self.model = DecisionTreeClassifier(max_depth=self.max_depth)
        else:
            self.model = DecisionTreeClassifier()
        self.model.fit(X_train, y_train)
    
    def preprocessing(self, df:pd.DataFrame):
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = add_ideal_pos(df)
        
        # Инициализируем сигнал нулями
        df['signal'] = 0
        train_set = ['close', 'high', 'low']
        
        # Убедимся, что нет пропущенных значений
        df_train = df.copy()
        df_train = df_train.dropna(subset=train_set+['ideal_pos']).copy()
        if not df_train.empty:
            y_train = df_train['ideal_pos']
            X_train = df_train[train_set]
            
            # Обучаем модель
            self.get_model(X_train, y_train)
            # Получаем предсказания и присваиваем их обратно в исходный DataFrame
            df.loc[X_train.index, 'signal'] = self.model.predict(X_train)
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 1:
            return 'long_pw'
        if row['signal'] == 2:
            return 'short_pw'
        return None
    
class STAML2a_PHENOMENON(BaseTABitget):
    """period=60, n_std=3, max_depth=None"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60, n_std=3,max_depth=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_std = n_std
        self.model = None
        self.max_depth = max_depth
    def get_model(self, X_train, y_train):
        if self.max_depth:
            self.model = DecisionTreeClassifier(max_depth=self.max_depth)
        else:
            self.model = DecisionTreeClassifier()
        self.model.fit(X_train, y_train)
    
    def preprocessing(self, df:pd.DataFrame):
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = add_ideal_pos(df)
        
        # Инициализируем сигнал нулями
        df['signal'] = 0
        train_set = ['close', 'high', 'low']
        
        # Убедимся, что нет пропущенных значений
        df_train = df.copy()
        df_train = df_train.dropna(subset=train_set+['ideal_pos']).copy()
        if not df_train.empty:
            y_train = df_train['ideal_pos']
            X_train = df_train[train_set]
            
            # Обучаем модель
            self.get_model(X_train, y_train)
            # Получаем предсказания и присваиваем их обратно в исходный DataFrame
            df.loc[X_train.index, 'signal'] = self.model.predict(X_train)
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 2:
            return 'long_pw'
        if row['signal'] == 1:
            return 'short_pw'
        return None
    
class STAML2a_MARVEL(BaseTABitget):
    """period=60, n_std=3,period_dc=30,max_depth=None"""
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=60, n_std=3,period_dc=30,period_rsi=30,period_adx=30,max_depth=None):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.n_std = n_std
        self.model = None
        self.period_dc = period_dc
        self.period_rsi = period_rsi
        self.period_adx = period_adx
        self.max_depth = max_depth
    def get_model(self, X_train, y_train):
        if self.max_depth:
            self.model = DecisionTreeClassifier(max_depth=self.max_depth)
        else:
            self.model = DecisionTreeClassifier()
        self.model.fit(X_train, y_train)
    
    def preprocessing(self, df:pd.DataFrame):
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = add_ideal_pos(df)
        df = add_donchan_channel(df, self.period_dc)
        df = add_rsi(df,period=self.period_rsi)
        
        # Инициализируем сигнал нулями
        df['signal'] = 0
        train_set = ['close', 'high', 'low', 'max_hb', 'min_hb', 'avarege']
        
        # Убедимся, что нет пропущенных значений
        df_train = df.copy()
        df_train = df_train.dropna(subset=train_set+['ideal_enter']).copy()
        if not df_train.empty:
            y_train = df_train['ideal_enter']
            X_train = df_train[train_set]
            
            # Обучаем модель
            self.get_model(X_train, y_train)
            # Получаем предсказания и присваиваем их обратно в исходный DataFrame
            df.loc[X_train.index, 'signal'] = self.model.predict(X_train)
        df = add_enter_price2close(df)
        df = add_slice_df(df, period=self.period)
        return df
    
    def __call__(self, row, *args, **kwds):
        if row['signal'] == 2:
            return 'long_pw'
        if row['signal'] == 1:
            return 'short_pw'
        return None