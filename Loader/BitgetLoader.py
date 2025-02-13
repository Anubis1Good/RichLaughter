import pandas as pd

def bitget_loader(raw_file):
    df = pd.read_csv(raw_file)
    if not 'middle' in df.columns:
        df['middle'] = df.apply(lambda row: (row['high']+row['low'])/2,axis=1)
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0',axis=1)
    return df