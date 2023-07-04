# -*- coding: utf-8 -*-
from Graph import *
from RestApi.get_data import *
from tabletools import *
from service_utility import *
class ShiftGraph(Graph):
    """
    Граф сотрудников со связями подчинения

    Args:
        Graph (_type_): _description_
    """
    def __init__(self,df):
        super().__init__(df)
    def set_nodes(self):
        lst_names=self.df['Фамилия'].tolist()
        for i in lst_names:
            g.dict_name[i]=i
class Man:
    lastname:str

class Dolgn:
    def __init__(self,**kw):
        self.id_dolgn=kw['№ квадрата']
        self.name=kw['Должность']
        self.manname=kw['Фамилия']
        self.chif=kw['Подчиненность']
        self.level=kw['Уровень']
        self.children=[]
        
    def prnInfo(self):
        print('******************')
        print("Должность")
        print(self.name)
        print('id')
        print(self.id_dolgn)
        print('сотрудник')
        print(self.manname)
        print('Подчиненность')
        print(self.chif)
        print('level=')
        print(self.level)
    def get_children(self,df):
        g = df.groupby('Подчиненность')
        for (i, sub_df) in g:
            if i==self.id_dolgn:
                lst=sub_df['Должность'].tolist()
                self.children=lst

"""
    def __str__(self):
        out="Должность" +self.name+"\n"+'id='+self.id_dolgn+'\n'+'сотрудник='+self.manname+'\n'+'Подчиненность='+self.chif+'\n'+'level='+self.level
        return out
"""
def create_man(agent,baseclass, onto, g):
    context_uid=get_source(agent,baseclass)['baseclass']['uid']
    container=agent.get_ontoitem('DextOntology',onto)
    container_uid=container['uid']
    container_url=container['url']
        #g=Graph(filename,'№ квадрата', 'Должность','Подчиненность')
    for k,v in g.dict_name.items():
        title=k
        print('title',title)
        indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
        agent.create_subclass(indata)
        change_class_property1(agent,'DextOntoClass', title , 'hasMetatype', baseclass)


#Граф для подразделений и служб
filename='RestApi/data/Доработанные таблицы.xlsx'
collist=['Подразделение', 'Наименование подразделения','Подчиненность']
sheet_name='Структура предприятия'
df=pd.read_excel(filename,sheet_name)
for col in collist:
    df[col] = df[col].astype('string')
    df[col] = df[col].str.strip()
df['Родитель'] = [x.split('.')[0] if len(x.split('.'))==2 and x.split('.')[-1]=='0' else x for x in df['Подчиненность']]
df=table_encode(df,collist)
df = df.drop('Подчиненность', axis=1)

df['Тип'] = ['служба' if 'Служба' in x else 'подразделение' for x in df['Наименование подразделения']]

g=DepGraph(df,'Подразделение', 'Наименование подразделения','Родитель','Тип')
# rename column
#df2 = df.rename({'a': 'X', 'b': 'Y'}, axis='columns')
# delete column
#df = df.drop('column_name', axis=1)
filename1='RestApi/data/Доработанные таблицы.xlsx'
collist1=['№ квадрата','Должность','Фамилия','Подчиненность','Уровень']
sheet_name1='Должностная таблица'
df1=pd.read_excel(filename1,sheet_name1)
for col in collist1:
    df1[col] = df1[col].astype('string')
    df1[col] = df1[col].str.strip()
    for i in range(6):
        df1[col] = df1[col].str.replace(' {2,}', ' ', regex=True)

df_total=pd.merge(df, df1,right_on='№ квадрата', left_on='Подразделение')

lst_dep=df_total['Наименование подразделения'].tolist()
lst_dolg=df_total['Должность'].tolist()
lst_man=df_total['Фамилия'].tolist()
"""
for i in range(len(lst_dep)):
    print(lst_dep[i])
    print(lst_dolg[i])
    print(lst_man[i])
    print()
"""
base_url='http://localhost:8080/Plone/'
agent=JsonData(base_url) 
"""
container=agent.get_ontoitem('DextOntology','Библиотека подразделений_демо')
container_uid=container['uid']
container_url=container['url']
dict_dep=get_folder_content(container_url)
for name in lst_dep:
    if name in dict_dep.keys():
        print(name)
"""
ontoname='Библиотека подразделений_демо'
baseclass='Подразделение'
baseclass1='Служба'
context_uid=get_source(agent,baseclass)['baseclass']['uid']
context_uid1=get_source(agent,baseclass1)['baseclass']['uid']
container=agent.get_ontoitem('DextOntology','Библиотека подразделений_демо')
container_uid=container['uid']
container_url=container['url']
# Создаем классы Служба и Подразделение
"""
for k,v in g.nodes.items():
    title=v.name
    if title != 'empty_class':
        if v.dep_type=='служба':
            indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid1,'title':k+' '+title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
        elif v.dep_type=='подразделение':
            indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':k+' '+title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}    
        agent.create_subclass(indata)
        change_class_property1(agent,'DextOntoClass', title , 'hasMetatype', baseclass)
        
"""
# ******* устанавливаем свойства классов ****
server_class_dict=get_folder_content(container_url)
#set_relation(agent,g,server_class_dict, 'подчиненность')
set_relation_value(agent,g,server_class_dict, 'идентификатор')
 