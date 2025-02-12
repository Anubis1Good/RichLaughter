import pandas as pd

def bitget_loader(raw_file):
    df = pd.read_csv(raw_file)
    df['middle'] = df.apply(lambda row: (row['high']+row['low'])/2,axis=1)
    df = df.drop('Unnamed: 0',axis=1)
    return df