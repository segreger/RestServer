from get_data import *
from utility import *
import numpy as np
import pandas as pd
#перегон таблицы excel  в библиотеку классов
#класс Элемент структуры производства



            
    
#url='http://localhost:8080/Plone/proekty/proekt-proizvodstvo/struktura?batch_size=0'
#dict_class=get_folder_content(url)
#dict_class['pustoi-klass']=empty_class()
def create_df0():
    base_url='http://localhost:8080/Plone/'
    agent=JsonData(base_url)
    refs=create_ref('Таблица.xlst','№ квадрата', '')
    namelst=[d['source_title'] for d in refs]
    dict_class=get_ontology_content_from_listnames(agent,namelst)


#deps_df=pd.read_excel('Кадры1.xlsx')
#refs=create_ref()
#print(refs)
#set_relation()
def set_relation(refs):
    """
    устанавливаем связи подчиненност
    """
    for d  in refs:

        source=dict_class[d['source_title']]
        target=dict_class[d['target_title']]
        prop=get_class_prop(source.url,'подчиненность')
        base=[{'@id':target.url}]
        print(source.title, target.title, prop['@id'])
        requests.patch(prop['@id'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':target.url }, auth=('admin', 'admin'))



