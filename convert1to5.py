import os
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
import pandas as pd


# folder = 'DataForTests\DataFromMOEX'
folder = 'DataForTests\DataFromMoexForStepTests'
# folder = 'DataForTests\otherMOEX'
listdir = os.listdir(folder)
# output_folder = 'DataForTests\DataFromMOEXto5'
output_folder = folder
for f in listdir:
    filepath = os.path.join(folder,f)
    df = pd.read_csv(filepath)
    df = convert_chart1to5(df)
    new_path = os.path.join(output_folder,'5'+f)
    df.to_csv(new_path)

