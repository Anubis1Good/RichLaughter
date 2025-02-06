import pandas as pd

def bitget_loader(raw_file):
    df = pd.read_csv(raw_file)
    return df