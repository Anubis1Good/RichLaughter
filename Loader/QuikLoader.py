import pandas as pd
def get_direction(row):
    if row['open'] < row['close']:
        return 1
    return -1
def quik_loader(raw_file):
    df = pd.read_csv(raw_file,sep='\t')
    df = df.drop_duplicates()
    df['direction'] = df.apply(get_direction,axis=1)
    df = df.reset_index()
    df = df.drop(['index','datetime','open','close'],axis=1)
    df['x'] = df.index
    return df