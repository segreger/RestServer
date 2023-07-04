import dash
from dash import html
from dash import dcc
import dash_cytoscape as cyto
from Graph import *
from tabletools import *


filename='RestApi/data/Доработанные таблицы.xlsx'
collist=['Подразделение', 'Наименование подразделения','Подчиненность']
sheet_name='Структура предприятия'
df=pd.read_excel(filename,sheet_name)
for col in collist:
    df[col] = df[col].astype('string')
    df[col] = df[col].str.strip()
df['Родитель'] = [x.split('.')[0] if len(x.split('.'))==2 and x.split('.')[-1]=='0' else x for x in df['Подчиненность']]
df=table_encode(df,collist)
df['Тип'] = ['служба' if 'Служба' in x else 'подразделение' for x in df['Наименование подразделения']]
g=DepGraph(df,'Подразделение', 'Наименование подразделения','Родитель','Тип')