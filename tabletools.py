# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def cleare_df(filename, sheet_name,collist):
    df=pd.read_excel(filename,sheet_name)
    print(df)
    for col in collist:
        df[col] = df[col].astype('string')
        #df[col] = df[col].str.strip()
        #df[col] = df[col].str.replace('.','_')
        
        df[col] = df[col].str.replace(' {2,}', ' ', regex=True)
        
    return df

def cleare_dataframe(df,collist):
    for col in collist:
        df[col] = df[col].astype('string')
        #df[col] = df[col].str.strip()
        #df[col] = df[col].str.replace('.','_')
        
        df[col] = df[col].str.replace(' {2,}', ' ', regex=True)
        
    return df
def table_encode(df, collist):
    for col in collist:
        df[col].str.encode('utf-8')
    return df
"""
base_url='http://localhost:8080/Plone/'
#agent=JsonData(base_url)    
filename='RestApi/Структура предприятия.xlsx'
collist=['№ квадрата', 'Должность','Подчиненность']
df_dep=table_encode(cleare_df(filename, collist),collist)
df_dep['Тип'] = ['служба' if 'Служба' in x else 'подразделение' for x in df_dep['Должность']]
"""
