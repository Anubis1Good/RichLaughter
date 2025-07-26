import os
import pandas as pd
import re

dollar_step = 7.8

futures_fee_funcs = {
    'base': lambda total,count: total - count*2,
    r'BR..$': lambda total,count: total*100*dollar_step - count*2,
    r'ED..$': lambda total,count: total*10000*dollar_step - count*2,
    r'EURRUBF': lambda total,count: total*1000 - count*2,
    r'IMOEXF': lambda total,count: total*10 - count*2,
    r'MM..$': lambda total,count: total*10 - count*2,
    r'NG..$': lambda total,count: total*1000*dollar_step - count*2,
    r'RM..$': lambda total,count: total*2*dollar_step - count*2,
    r'RI..$': lambda total,count: total*2*dollar_step*0.1 - count*2,
    r'CNYRUBF': lambda total,count: total*1000 - count*2,
    r'CR..$': lambda total,count: total*1000 - count*2,
    r'GD..$': lambda total,count: total*10*dollar_step - count*2,
    r'USDRUBF': lambda total,count: total*1000 - count*2,
    r'SV..$': lambda total,count: total*100*dollar_step - count*2,
    r'PD..$': lambda total,count: total*10*dollar_step - count*2,
    r'PT..$': lambda total,count: total*10*dollar_step - count*2,
    r'UC..$': lambda total,count: total*1000*10.94 - count*2,
    r'SF..$': lambda total,count: total*10*dollar_step - count*2,
    r'NA..$': lambda total,count: total*dollar_step*0.1 - count*2,
    r'CC..$': lambda total,count: total*10 - count*2,
    r'SBERF': lambda total,count: total*100 - count*2,
    r'GAZPF': lambda total,count: total*100 - count*2,
    r'IB..$': lambda total,count: total*10*dollar_step - count*2,
}

def get_func_vtb_fee(name):
    for fff in futures_fee_funcs:
        if re.match(fff,name):
            return futures_fee_funcs[fff]
    return futures_fee_funcs['base']

main_folder = 'TestNewResults\ChildTest'

inner_folders = os.listdir(main_folder)

for inner_folder in inner_folders:
    inner_folder_path = os.path.join(main_folder,inner_folder)
    xls_folder_path = os.path.join(inner_folder_path,'xls')
    files = os.listdir(xls_folder_path)
    df_total = pd.DataFrame()
    for file in files:
        file_path = os.path.join(xls_folder_path,file)
        df_file = pd.read_excel(file_path,'total')
        if df_total.empty:
            df_total = df_file
        else:
            df_total = pd.concat([df_total,df_file])
    vtb_twf_func = get_func_vtb_fee(inner_folder.split('_')[0])
    df_total["vtb"] = vtb_twf_func(df_total["total"],df_total["count"])
    # Получаем список столбцов без "vtb"
    cols = [col for col in df_total.columns if col != "vtb"]

    # Вставляем "vtb" на вторую позицию
    cols.insert(2, "vtb")

    # Применяем новый порядок
    df_total = df_total.reindex(columns=cols)
    df_total = df_total.sort_values('total_abs_fee',ascending=False)
    df_total = df_total.reset_index(drop=True)
    if 'Unnamed: 0' in df_total.columns:
        df_total = df_total.drop('Unnamed: 0',axis=1)
    full_name_doc = os.path.join(inner_folder_path, inner_folder + '.xlsx')
    with pd.ExcelWriter(full_name_doc, engine='xlsxwriter') as writer:  
        df_total.to_excel(writer, sheet_name='total')
        worksheet = writer.sheets['total']
        workbook = writer.book
        for i, col in enumerate(df_total.columns,start=1):
            width = max(df_total[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, width)
            worksheet.conditional_format(1, i, len(df_total), i, {
                'type': 'cell',
                'criteria': 'less than',
                'value': 0,
                'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
            })
            worksheet.conditional_format(1, i, len(df_total), i, {
                'type': '3_color_scale',
                'min_color': '#DA9694',
                'mid_color': '#FFFFFF',
                'max_color': '#00B0F0'
            })