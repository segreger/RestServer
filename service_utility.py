# -*- coding: utf-8 -*-

from RestApi.get_data import *
from RestApi.portalmanager import *
from RestApi.dext_utility import *
from Graph import *
from tabletools import *


class RestManager(JsonData):
    def __init__(self,**kw):
        super().__init__(**kw)
    def get_source(self,nameclass):
        """
        по имени класса получает список подклассов
        """
        uid=self.get_class_by_name(nameclass)['uid']
        return self.get_children(uid)

    def update_objdb(self,g, ontoname,lst_baseclass):
        """cсоздакт объекты объектной базы в соответствии с графом g

        Args:
            g (Graph): граф
            ontoname (str): онтология. где создаются объекты
            lst_baseclass (_type_): список контент-типов, подклассы которых создаются, узел графа - объект, имеющий свойство contenttype
            
        """
        base_uid=dict([(baseclass,self.get_source(baseclass)['baseclass']['uid']) for baseclass in lst_baseclass])
        container=self.get_ontoitem('DextOntology',ontoname)
        container_uid=container['uid']
        container_url=container['url']
        # Создаем классы Служба и Подразделение
        for k,v in g.nodes.items():
            title=v.name
            if title != 'empty_class':
                indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':base_uid[v.contenttype],'title':k+' '+title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
                self.create_subclass(indata)
                self.change_class_property1(agent,'DextOntoClass', title , 'hasMetatype', v.contenttype)
    def change_class_property1(self,portal_type, classname, property_name, target_name):
        """
        меняет свойство системное свойство объекта:SubClassOf, hasMetatype, range и т.п
        portal_type - строка имени контент типа
        classname - строка имя элемента, у которого меняется свойство
        property_name - имя свойства
        target_name - имя элемента, на которое ссылается свойство

        """
        target_data=self.get_class_by_name(target_name)
        target_id=target_data['url']
        base=[{'@id':target_id}]#получили инормацию для range связи
        url='http://localhost:8080/Plone/'
        #d_json={'@type': portal_type, 'title': classname}
        #cls_data=agent.create_class(url,d_json)
        cls_data=self.get_class_by_name(classname)
        cls_url=cls_data['url']
        requests.patch(cls_url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={property_name:base }, auth=('admin', 'admin'))
    """ замена на PortalManager"
    def plone_subclass(agent,context_uid,container_uid,title, desc):
        '''создает подкласс класса с uid=context_uid в онтологии с uid=container_uid

        Args:
            agent (JsonData): агент доступа к серверу
            context_uid (str): uid родительского класса
            container_uid (str):uid онтологии, где создается подкласс
            title (str): имя подкласса
            desc (str): описание подкласса
        '''

        indata={'selonto':container_uid,'context_uid':context_uid,'title':title,'desc':desc,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
        agent.create_subclass(indata)
    """

def create_ref(filename,name_id, name_plant, name_ref='родитель'):
    """
    формирует словарь подчиненностей подразделений
	@filename - имя excel-файла
	@name_id - название столбца таблицы номера подразделения
	@name_plant - название столбца таблицы названия подразделения
    """
    df=pd.read_excel(filename)
    #print(df)
    df[name_id] = df[name_id].astype('string')
    df[name_ref] = df[name_ref].astype('string')
    df[name_id] = df[name_id].str.replace('.','_')
    df[name_ref] = df[name_ref].str.replace('.','_')
    for name in [name_plant]:
        df[name] = df[name].str.replace('\n', '')
        df[name] = df[name].str.replace('\t', ' ')
        df[name] = df[name].str.replace(' {2,}', ' ', regex=True)
        df[name] = df[name].str.strip()
    
    id=df[name_id].tolist()
    name=df[name_plant].tolist()
    """
    t = ((1, 'a'),(2, 'b'))
    dict(map(reversed, t))
    """
    dict_name=dict([(id[i],[name[i], name_ref[i]]) for i in range(len(id))])
    """
    df[name_id] = df[name_id].astype('string')
    df[name_ref] = df[name_ref].astype('string')
    df[name_id] = df[name_id].str.replace('.','_')
    df[name_ref] = df[name_ref].str.replace('.','_')
    
    lst_id=df[name_id].tolist() #ключ подразделения
    lst_n=df[name_plant].tolist()#название подразделения
    lst_ref=df[name_ref]
    d_df=dict([(lst_id[i].strip(),lst_n[i].strip()) for i in range(len(lst_id))])
    

    #d_df=dict(zip(df[name_id].tolist(),df[name_plant].tolist()))
    """
    #print('dict_name',dict_name)
    dict_relation={}
    g = df.groupby(name_ref)
    for (i, sub_df) in g:
        sub_df[name_id] = sub_df[name_id].astype('string')
        sub_df['fullname']=sub_df[name_id]+ ' '+sub_df[name_plant]
        lst=sub_df['fullname'].tolist()
        if i !='root':
            dict_relation[dict_name[i][0]]=lst
        else:
            dict_relation['empty_class']=lst


    
    """
    df['source_title']=df[name_id]+ ' '+df[name_plant]
    df['родитель'] = df[name_ref].astype('string')
    d=df.to_dict('records')
    for i in d:
        if i['родитель'].strip() !='root':
            target_title=i['родитель'].strip()+' '+d_df[i['родитель'].strip()].strip()
            i['target_title']=target_title
        else:
            i['target_title']=empty_class().id
    return d
    """
    return dict_relation

def set_relation(agent,graph,server_class_dict, propname):
    """
    устанавливаем связи подчиненност
    """
    
    for edg  in graph.edges:
        if edg.target:
            source_title=graph.nodes[edg.source].name
            target_title=graph.nodes[edg.target].name
            source=agent.get_ontoitem('DextOntoClass',source_title)
            print('source=',source)
            target=agent.get_ontoitem('DextOntoClass',target_title)
            print('target=',target)
            #print('target_url=',target['url'])
            if source and target:

                prop=get_class_prop(source['url'], propname)
                print('prop',prop['@id'])
                #base=[{'@id':target['url']}]
                requests.patch(prop['@id'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':target['url'] }, auth=agent.auth)
                



def set_relation_value(agent,graph,server_class_dict, propname):
    """
    устанавливаем данные DextClassDatProperty
    """
    for node  in graph.nodes.values():
        if node.name:
            print('node',node.name)

            source=agent.get_ontoitem('DextOntoClass',node.name)
            print('source=',source)
            prop=get_class_prop(source['url'], propname)
            value=node.id_node
            requests.patch(prop['@id'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'value':value }, auth=('admin', 'admin'))

def service_ref(agent,graph):
    """
    создаем узлы служб графа подразделений

    Args:
        graph (Graph):граф подразделений и связей подчиненностей
    """
    ontoname='Библиотека подразделений_демо'
    baseclass='Подразделение'
    baseclass1='Служба'
    context_uid=get_source(agent,baseclass)['baseclass']['uid']
    context_uid1=get_source(agent,baseclass1)['baseclass']['uid']
    container=agent.get_ontoitem('DextOntology','Библиотека подразделений_демо')
    container_uid=container['uid']
    container_url=container['url']
    
    
    #g=Graph(filename,'№ квадрата', 'Должность','Подчиненность')
    for k,v in g.dict_name.items():
        title=v.name_plant
        if title != 'empty_class':
            if v.dep_type=='служба':
                indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid1,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
            elif v.dep_type=='подразделение':
                indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}    
            agent.create_subclass(indata)
            change_class_property1(agent,'DextOntoClass', title , 'hasMetatype', baseclass)




def set_depatments_from_table():
    """
    Создаются подкласссы типа Подразделение и Служба и связи подчинения между ними на основе таблицы Excel
    """
    base_url='http://localhost:8080/Plone/'
    agent=JsonData(base_url)    
    filename='RestApi/Структура предприятия.xlsx'
    collist=['№ квадрата', 'Должность','Подчиненность']
    df_dep=table_encode(cleare_df(filename, collist),collist)
    df_dep['Тип'] = ['служба' if 'Служба' in x else 'подразделение' for x in df_dep['Должность']]
    g=DepGraph(df_dep,'№ квадрата', 'Должность','Подчиненность','Тип')
    container=agent.get_ontoitem('DextOntology','Библиотека подразделений_демо')
    container_url=container['url']
    
    #print(server_class_dict)
    # ****** Создаем классы на сервере ****
    service_ref(agent,g)
    # ******* устанавливаем свойства классов ****
    server_class_dict=get_folder_content(container_url)
    set_relation(agent,g,server_class_dict, 'подчиненность')
    set_relation_value(agent,g,server_class_dict, 'идентификатор')
    print('GAME OVER')


def get_slgb_from_table(filename):
    collist=['№ квадрата', 'Должность','Подчиненность']
    df_dep=table_encode(cleare_df(filename, collist),collist)
    df_dep['Тип'] = ['служба' if 'Служба' in x else 'подразделение' for x in df_dep['Должность']]
    g=DepGraph(df_dep,'№ квадрата', 'Должность','Подчиненность','Тип')
    return g

def set_dolg_man_rel(g,agent,propname):
    for n  in g.nodes.values():
        source_title=n.name
        target_title=n.manname
        print(source_title,'->',target_title)
        source=agent.get_ontoitem('DextOntoClass',source_title)
        print('source=',source)
        target=agent.get_ontoitem('DextOntoClass',target_title)
        print('target=',target)
        #print('target_url=',target['url'])
        if isinstance(source, dict) and 'url' in source.keys():
            prop=get_class_prop(source['url'], propname)
            #print('prop',prop['@id'])
            #base=[{'@id':target['url']}]
            requests.patch(prop['@id'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':target['url'] }, auth=agent.auth)
            
def setSubclass(ontoname,baseclass,copy_agent,lst_agent):
    """
    ontoname - имя онтологии, где создаются классы
    baseclass - имя родительского класса
    target_agent - создающий агент
    lst_agent - список имен создаваемых классов
    """
    
    obj=copy_agent.target_mng.host_agent.get_source('DextOntoClass',baseclass)
    print('baseclass',baseclass,obj,'obj')
    context_uid=obj['baseclass']['uid']
    #context_uid1=get_source(agent,baseclass1)['baseclass']['uid']
    container=copy_agent.target_mng.host_agent.get_ontoitem('DextOntology',ontoname)
    container_uid=container['uid']
    #container_url=container['url']
    # Создаем классы Служба и Подразделение

    for title in lst_agent:
        x=copy_agent.target_mng.host_agent.get_ontoitem('DextOntoClass',title)
        if not x:
            indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
            #copy_agent.target_mng.host_agent.create_subclass(indata)
            url=copy_agent.target_mng.host_agent.base_url+'getjson'
            par={'submitted': 'True','inst_type':'DextOntoClass','mode':'subclass_add1'}
            par.update(indata)
            print('*****************create subclass*******','\n','par',par)
            requests.post(url,params=par, headers={'Accept': 'application/json'}, auth=copy_agent.target_mng.host_agent.auth)

            copy_agent.change_class_property(baseclass, 'hasMetatype', title)
            print('class {} создан'.format(title))
        else:
            print('class {} уже существует'.format(title))
