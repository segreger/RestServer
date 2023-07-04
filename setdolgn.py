# -*- coding: utf-8 -*-
import random
from Graph import *
from RestApi.get_data import *
from tabletools import *
from service_utility import *

from RestApi.ontomodeler_lib import *
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
        self.id_dolgn=kw['ID']
        self.name=kw['Должность']
        self.manname=kw['Фамилия']
        self.chif=kw['Родитель']
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

class DolgNode(Node):
    def __init__(self,name,id_node, man,ref,level):
        super().__init__(name,id_node)
        self.name=name
        self.id_node=id_node
        self
    def __str__(self):
        out=''
        out+='name='+self.name+'\n'
        out+='=id_node='+self.id_node+'\n'
        if self.value:
            out+='value='+self.value +'\n'
        for c in self.children:
            out+=c+'\n'
        return out


class DolgGraph(Graph):
    def __init__(self,df,collist):
        #['№ квадрата','Должность','Фамилия','Подчиненность','Уровень']
        super().__init__(df)
        self.df=df
        self.dolg_id=collist[0]
        self.dolg_name=collist[1]
        self.dolg_ref=str(collist[3])
        self.man=collist[2]
        self.level=collist[4]
        self.nodes={}#Словарь всех узлов,ключ - имя узла
        self.edges=[]# список ребер между объектами Node
        self.nodes=dict([(i['ID'],Dolgn(**i) ) for i in self.df.to_dict('records')])
        
        for n in self.nodes.values():
            n.name =  n.id_dolgn + ' ' +n.name

        
        g = self.df.groupby(self.dolg_ref)
        #добавляем узлы, имеющих подчиненных
        for (i, sub_df) in g:
            if not i=='76.1':
                lst=sub_df[self.dolg_id].tolist()
                node=self.nodes[i]
                node.children=lst
                
        for k,v in self.nodes.items():
            for t in v.children:
                rel=Relation(t,k)
                self.edges.append(rel)
        d_target,d_source={},{}


               

    def __str__(self):
        out=''
        for n,v in self.nodes.items():
            out=out+'\n'+v.name+'\n'
            for i in v.children:
                out=out+'\t'+i+'\n'
        return out
    
    def get_root(self):
        for k,v in self.nodes.items():
            if  v.id_dolgn=='1':
                return v
    
    


def create_man(agent,baseclass, onto, g):
    context_uid=get_source(agent,baseclass)['baseclass']['uid']
    container=agent.get_ontoitem('DextOntology',onto)
    container_uid=container['uid']
    container_url=container['url']
        #g=Graph(filename,'№ квадрата', 'Должность','Подчиненность')
    for k,v in g.nodes.items():
        title=v.manname
        print(v.name, title)
        indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
        agent.create_subclass(indata)
        change_class_property1(agent,'DextOntoClass', title , 'hasMetatype', baseclass)

target_url='http://ontogovorun.ru/proekt/'
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_host=HostInfo(target_url,target_login, target_passw)
target_agent=JsonData(target_host)
target_mng=ModelManager(target_agent)
filename1='RestApi/data/New Доработанные таблицы.xlsx'
collist=['№ квадрата','Должность','Фамилия','Подчиненность','Уровень']
sheet_name1='Должностная таблица'
df1=pd.read_excel(filename1,sheet_name1)
for col in collist:
    df1[col] = df1[col].astype('string')
    df1[col] = df1[col].str.strip()
    for i in range(6):
        df1[col] = df1[col].str.replace(' {2,}', ' ', regex=True)
df1['Родитель'] = [x.split('.')[0] if len(x.split('.'))==2 and x.split('.')[-1]=='0' else x for x in df1['Подчиненность']]
df1 = df1.drop('Подчиненность', axis=1)
df1['ID'] = [x.split('.')[0] if len(x.split('.'))==2 and x.split('.')[-1]=='0' else x for x in df1['№ квадрата']]
df1 = df1.drop('№ квадрата', axis=1)
collist1=['ID','Должность','Фамилия','Родитель','Уровень']
df1=table_encode(df1,collist1)

g=DolgGraph(df1,collist1)
base_url='http://ontogovorun.ru/'



#Создание должностей


# Создаем классы Служба и Подразделение

def set_subclasses(g,target_agent):
    ontoname='Библиотека должностей'
    baseclass='Должность'
    context_uid=get_source(target_agent,'DextOntoClass',baseclass)['baseclass']['uid']

    container=target_agent.get_ontoitem('DextOntology',ontoname)
    container_uid=container['uid']
    container_url=container['url']
    for k,v in g.nodes.items():
        title=v.name
        indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
        #agent.create_subclass(indata)
        change_class_property(target_agent,'DextOntoClass', title , 'hasMetatype', baseclass)
    print('Game over')        


# ******* устанавливаем свойства классов ****
def set_prop_range(g,target_agent):
    ontoname='Библиотека должностей'
    baseclass='Должность'
    context_uid=get_source(target_agent,'DextOntoClass',baseclass)['baseclass']['uid']

    container=target_agent.get_ontoitem('DextOntology',ontoname)
    container_uid=container['uid']
    container_url=container['url']
    server_class_dict=get_folder_content(container_url,target_agent)
    set_relation(target_agent,g,server_class_dict, opopname)
    set_relation_value(target_agent,g,server_class_dict, dpopname)
    print('Game over')  

def set_man(g,target_agent):
    ontoname='Библиотека сотрудников'
    baseclass='Сотрудник'
    context_uid=get_source(target_agent,'DextOntoClass',baseclass)['baseclass']['uid']

    container=target_agent.get_ontoitem('DextOntology',ontoname)
    container_uid=container['uid']
    container_url=container['url']

    #create_man(agent,baseclass, ontoname, g)
    set_dolg_man_rel(g,target_agent,'сотрудник')
    print('Game over')

#Создание должностей
"""
ontoname='Библиотека должностей'
baseclass='Должность'
context_uid=get_source(agent,baseclass)['baseclass']['uid']

container=agent.get_ontoitem('DextOntology',ontoname)
container_uid=container['uid']
container_url=container['url']

# Создаем классы Служба и Подразделение
server_class_dict=get_folder_content(container_url)

for k,v in g.nodes.items():
    name=k+' '+v.name
    out = agent.get_class_by_name(name)
    if not out:
        print(name)
"""
