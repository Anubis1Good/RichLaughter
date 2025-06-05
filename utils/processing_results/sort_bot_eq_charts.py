import os
import shutil
chart_folder = 'TestOtTrades\cumulative_results_plots\AllTime'
outer_folder_name = 'TestOtTrades\cumulative_results_plots\AllTimeSort'
files = os.listdir(chart_folder)

for file in files:
    inner_folder_name = "_".join(file.split('_')[2:])[:-4]
    full_folder_name = os.path.join(outer_folder_name,inner_folder_name)
    if not os.path.exists(full_folder_name):
        os.makedirs(full_folder_name)
    old_path = os.path.join(chart_folder,file)
    new_path = os.path.join(full_folder_name,file)
    # os.replace(old_path,new_path)
    shutil.copy(old_path,new_path)
print('end')