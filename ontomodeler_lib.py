# -*- coding: utf-8 -*-
import pdb
import requests
import json
#from get_data import *
from .ontoclassWU import *
from dataclasses import dataclass
from .ploneserver_utility import *


@dataclass
class ModelManager:
    host_agent:JsonData
    
        
    def get_listonology(self):
        allonto=get_folder_content(self.host_agent.host.url,self.host_agent)
        self.dict_onto=dict([(item['title'],{'title':item['title'],'content_type':item['@type'],'url':item['@id']}) for item in allonto])
        self.lst_onto=self.dict_onto.keys()
        
        
    def create_ontologys(self,lst_title):
        for ontoname in lst_title:
            create_res(lst_title, "DextOntology")
    def create_res(self,url,lst_title,contenttype,value):

        for title in lst_title:
            target=target_mng.host_agent.get_class_by_name(title,contenttype)
            if not target:
                if contenttype=='DextClassDataProperty':
                    responce=requests.post(url, headers={'Accept': 'application/json',
                    'Content-Type': 'application/json'}, json={'@type': 'DextClassDataProperty', 'title': title,'value':value}, auth=self.host_agent.host.auth)
                else:
                    responce=requests.post(url, headers={'Accept': 'application/json',
                    'Content-Type': 'application/json'}, json={'@type': contenttype, 'title': title}, auth=self.host_agent.host.auth)

            
                    


@dataclass
class ModelCopyAgent:
    source_mng:ModelManager
    target_mng:ModelManager
    
    def __post_init__(self):
        self.exept=['Рабочие проекты','Задания библиотека','Структура организации']
        self.active_onto=['Производство_агенты']
    
        
        
    def list_ontology_copy(self):
        source_mng.get_listonology()
        target_url=self.target_mng.host_agent.host.url

        target_mng.get_listonology()
        
        res_lst=[i for i in source_mng.lst_onto if not i in target_mng.lst_onto]

        target_mng.create_res(target_url,res_lst,'DextOntology','')
    def list_class_search(self,lst_onto):
        for ontoname in lst_onto:
            
            source_onto=source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
            res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()
            target_onto=target_mng.host_agent.get_class_by_name('DextOntology',ontoname)
            lst_title=[i.title for i in res_source.children.values()]
            for title in lst_title:
                target_cls=target_mng.host_agent.get_class_by_name('DextOntoClass', title)
                
                if not target_cls:
                    print(target_cls)
                    print(title+' not exist')
                else:
                    res_target=DextWorkUnit('',target_cls['url'],source_mng.host_agent).getWUnit()
                    print('Class '+target_cls['title']+' in '+target_cls['container_title'])
                    print(res_target.children)
                
                    
     
        
    def list_class_copy(self,lst_onto):
        for ontoname in lst_onto:
            if  ontoname in self.active_onto:
                

                
                
                source_onto=source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
                if 'url'in source_onto.keys():
                    res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()
                    target_onto=target_mng.host_agent.get_class_by_name('DextOntology',ontoname)
                    if target_onto:
                        lst_title=[i.title for i in res_source.children.values()]
                        for title in lst_title:
                            target_cls=target_mng.host_agent.get_class_by_name('DextOntoClass', title)
                            if not target_cls:
                                
                                print(title+' not exist')
                                print('ontoname',ontoname)
                                print(target_onto)
                                
                                target_mng.create_res(target_onto['url'],[title], "DextOntoClass",'')
                    else:
                        print("target ontology not exist")
                else:
                    print('url not exist')
                    print(source_onto)
    def equal_class(self,source_classname,target_classname):

        """
        сравниваются свойства двух классов

        при несовпадении свойства создаются

        
        """
        #source_cls и target_cls - результат поиска классов по имени:
        source_cls=self.source_mng.host_agent.get_class_by_name('DextOntoClass', source_classname)
        res_source=DextWorkUnit('',source_cls['url'],self.source_mng.host_agent).getWUnit()
        target_cls=self.target_mng.host_agent.get_class_by_name('DextOntoClass', target_classname)
        res_target=DextWorkUnit('',target_cls['url'],self.target_mng.host_agent).getWUnit()

        source_props=res_source.children.keys()
        target_props=res_target.children.keys()
        for p in source_props:
            if p not in target_props:
                print( '{} not has {}'.format(target_classname, p))
                self.create_props(source_classname,target_classname)
                print('Create prop {} in class {}'.format(p, target_classname))
        self.set_props_range(source_classname,target_classname)        
    
    def change_class_property(self,source_classname, property_name, target_classname):

        target_data=self.target_mng.host_agent.get_class_by_name('DextOntoClass',target_classname)
        #print('target_data',target_data)
        target_id=target_data['url']
        
        base=[{'@id':target_id}]#получили инормацию для range связи
        cls_data=self.source_mng.host_agent.get_class_by_name('DextOntoClass',source_classname)
        #print('cls_data',cls_data)
        if cls_data:
            cls_url=cls_data['url']
            requests.patch(cls_url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={property_name:base }, auth=self.target_mng.host_agent.auth)


    def prop_for_target(self,lst_onto):
        if True:
            
            for ontoname in lst_onto:
                if ontoname in self.active_onto:
                                      
            
                    
                    source_onto=self.source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
                    
                    res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()
                    
                    for class_name in list(res_source.children.keys()):
                        
                        self.create_props(class_name)
        
    def create_props(self,source_classname,target_classname):
        self.nonerange=[]
        source_cls=self.source_mng.host_agent.get_class_by_name('DextOntoClass', source_classname)
        res_source=DextWorkUnit('',source_cls['url'],self.source_mng.host_agent).getWUnit()
        target_cls=self.target_mng.host_agent.get_class_by_name('DextOntoClass', target_classname)
        res_target=DextWorkUnit('',target_cls['url'],self.target_mng.host_agent).getWUnit()
        target_props=res_target.children
        """
        if not target_cls:
            response=requests.post(target_onto['url'], headers={'Accept': 'application/json',
                'Content-Type': 'application/json'}, json={'@type': 'DextOntoClass', 'title': title}, auth=(target_login, target_passw))
        else:
        """
        for title,prop in res_source.children.items():
            #target_prop=target_mng.host_agent.get_class_by_name(prop.content_type, title)
            if not title in target_props.keys():
                value=''

                if prop.content_type=='DextClassObjectProperty':
                    create_res(target_cls['url'],[title],prop.content_type,'')
                elif prop.content_type=='DextClassDataProperty' and prop.range:
                    #target_range=target_agent.get_class_by_name('DextOntoClass',prop.range[0])
                    range_title=prop.range[0]
                    if range_title=='StringType':
                        value='_'
                    elif range_title=='IntegerType':
                        value='0'
                    create_res(target_cls['url'], [title], prop.content_type, value)
                elif prop.content_type=='DextClassDataProperty':
                    #target_range=target_agent.get_class_by_name('DextOntoClass',prop.range[0])
                    if not prop.range:
                        range_title='StringType'
                    else:
                        range_title=prop.range[0]
                    if range_title=='StringType':
                        value='_'
                    elif range_title=='IntegerType':
                        value='0'
                    create_res(target_cls['url'], [title], prop.content_type, value)        
                if prop.content_type=='DextClassObjectProperty' or prop.content_type=='DextClassDataProperty':
                    nonename=create_op_target_copy(self.target_mng.host_agent, prop, prop.content_type)
                    if nonename and nonename not in self.nonerange:
                        self.nonerange.append(nonename)
            else:
                target_prop=target_props[title]
                if prop.range:
                    #target_pro=get_class_prop(target_cls['url'],title)
                    if len(prop.range)==1:
                        range_title=prop.range[0]
                        range_cls=self.target_mng.host_agent.get_ontoitem('DextOntoClass',range_title)
                        
                        if range_cls and target_prop.url:
                            out=requests.patch(target_prop.url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':range_cls['url'] }, auth=self.target_mng.host_agent.auth)

                        elif len(prop.range)>1:
                            range_url=[self.target_mng.host_agent.get_ontoitem('DextOntoClass',i)['url'] for i in prop.range][0]
                            requests.patch(target_prop['@id'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':range_url }, auth=self.target_mng.host_agent.auth)
  

    def del_prop_for_target(self,lst_onto):
        if True:
            
            for ontoname in lst_onto:
                if ontoname in self.active_onto:
                                      
            
                    
                    source_onto=self.source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
                    
                    res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()
                    
                    for class_name in list(res_source.children.keys()):
                        print('delete prop class_name',class_name)
                        self.delete_props(class_name)
    
    
    def delete_props(self,class_name):
        self.nonerange=[]
        source_cls=source_mng.host_agent.get_class_by_name('DextOntoClass', class_name)
        res_source=DextWorkUnit('',source_cls['url'],source_mng.host_agent).getWUnit()
        target_cls=target_mng.host_agent.get_class_by_name('DextOntoClass', class_name)
        
        res_target=DextWorkUnit('',target_cls['url'],target_mng.host_agent).getWUnit()
        
        target_props=res_target.children
        
        for title,prop in res_source.children.items():

            if  title in target_props.keys():
                out=target_mng.host_agent.delete_item(prop.url)

    
    def range_for_target(self,lst_onto):
        for ontoname in lst_onto:
            if ontoname in self.active_onto:
                
                source_onto=self.source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
                
                res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()
                
                for class_name in list(res_source.children.keys()):
                    
                    self.set_props_range(class_name)
    
    def set_props_range(self,source_classname,target_classname):
        source_cls=self.source_mng.host_agent.get_class_by_name('DextOntoClass', source_classname)
        res_source=DextWorkUnit('',source_cls['url'],self.source_mng.host_agent).getWUnit()
        target_cls=self.target_mng.host_agent.get_class_by_name('DextOntoClass', target_classname)
        res_target=DextWorkUnit('',target_cls['url'],self.target_mng.host_agent).getWUnit()
        

        for title,prop in res_source.children.items():
            
            target_prop=self.target_mng.host_agent.get_class_by_name(prop.content_type, title)
            value=''
            
            if target_prop and 'url' in target_prop.keys():
                if prop.range:
                    #target_pro=get_class_prop(target_cls['url'],title)
                    if len(prop.range)==1:
                        range_title=prop.range[0]
                        range_cls=self.target_mng.host_agent.get_ontoitem('DextOntoClass',range_title)
                        
                        if range_cls and target_prop['url']:

                            out=requests.patch(target_prop['url'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':range_cls['url'] }, auth=self.target_mng.host_agent.auth)

                        elif len(prop.range)>1:
                            range_url=[self.target_mng.host_agent.get_ontoitem('DextOntoClass',i)['url'] for i in prop.range][0]
                            requests.patch(target_prop['@id'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':range_url }, auth=target_mng.host_agent.auth)
    
    
    def set_prop_range(self,source_classname,target_classname, source_propname):
        source_cls=self.source_mng.host_agent.get_class_by_name('DextOntoClass', source_classname)
        res_source=DextWorkUnit('',source_cls['url'],self.source_mng.host_agent).getWUnit()
        target_cls=self.target_mng.host_agent.get_class_by_name('DextOntoClass', target_classname)
        #res_target=DextWorkUnit('',target_cls['url'],self.target_mng.host_agent).getWUnit()
        source_props_dict=res_source.children
        if source_propname in source_props_dict.keys():
            prop=source_props_dict[source_propname] #DextObjectClassProperty or DextDataClassProperty
            #target_prop=self.target_mng.host_agent.get_class_by_name(prop.content_type, target_propname)
                            
            if prop and prop.url:
                out=requests.patch(prop.url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':target_cls['url']}, auth=self.target_mng.host_agent.auth)
                """
                if out=='201':
                    print('Свойство {}.{} ссылается на {}'.format(source_propname,source_classname,target_classname))
                else:
                    print('Ошибка записи')
                """


                                
          
        
def ontomodel_copy(lst_title):
        for title,obj in res_source.children.items():

            target_cls=target_agent.get_class_by_name('DextOntoClass',obj.title)
            if not target_cls:
                response=requests.post(target_onto['url'], headers={'Accept': 'application/json',
                        'Content-Type': 'application/json'}, json={'@type': 'DextOntoClass', 'title': title}, auth=(target_login, target_passw))

def equal_class(copy_agent,source_cls,target_cls):

    """
    сравниваются свойства двух классов
    source_cls и target_cls - результат поиска классов по имени:
    source_cls=source_mng.host_agent.get_class_by_name('DextOntoClass', class_name)
    res_source=DextWorkUnit('',source_cls['url'],source_mng.host_agent).getWUnit()
    target_cls=target_mng.host_agent.get_class_by_name('DextOntoClass', class_name)
    res_target=DextWorkUnit('',target_cls['url'],target_mng.host_agent).getWUnit()
    при несовпадении свойства создаются

    source_mng=ModelManager(source_agent)
    target_mng=ModelManager(target_agent)
    copy_agent=ModelCopyAgent(source_mng,target_mng)
    
    """

    source_props=target_cls.children.keys()
    target_props=target_cls.children.keys()
    for p in source_props:
        if p not in target_props:
            print( '{} not has {}'.format(target_cls.title, p))
            copy_agent.create_props(source_cls.title)
            print('Create prop {} in class {}'.format(p, target_cls.title))
    
def equal_classes(source_mng,target_mng, lst_onto):
    for ontoname in lst_onto:
        
        
        source_onto=source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
        res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()
        """
        target_onto=target_mng.host_agent.get_class_by_name('DextOntology',ontoname)
        
        if target_onto:
            #print(target_onto)
            res_target=DextWorkUnit('',target_onto['url'],target_mng.host_agent).getWUnit()
            l1=set(list(res_source.children.keys()))
            l2=set(list(res_target.children.keys()))
            if l1-l2:
                print(ontoname, l1-l2)
        else:
            print('Ontology {} not found'.format(ontoname))
        
        """
        target_onto=target_mng.host_agent.get_class_by_name('DextOntology',ontoname)
        
        if target_onto:
            #print(target_onto)
            res_target=DextWorkUnit('',target_onto['url'],target_mng.host_agent).getWUnit()           
        
        for source_cls in res_source.children.values():
            
            source_props=source_cls.children.keys()
            if source_cls.title in res_target.children.keys():
                """
                target_cls=res_target.children[source_cls.title]
                target_props=target_cls.children.keys()
                
                #for p in source_props:
                #    if p not in target_props:
                #        print( '{} not has {}'.format(target_cls.title, p))
                copy_agent.create_props(source_cls.title)
                target_out=target_mng.host_agent.get_class_by_name('DextOntoClass',source_cls.title) 
                if target_out:
                    print('Create {}'.format(target_out['title']))
                """
            
            else:
                print('{} not in {}'.format(source_cls.title ,ontoname))
                target_mng.create_res(target_onto['url'],[source_cls.title], "DextOntoClass",'')
                
            """    
            copy_agent.create_props(source_cls.title)
                target_out=target_mng.host_agent.get_class_by_name('DextOntoClass',source_cls.title) 
                if target_out:
                    print('Create {}'.format(target_out['title']))
            """ 

def get_listclasses(source_mng,ontoname):
    source_onto=source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
    res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()
    lst_cls_title=[i.title for i in res_source.children.values()]
        #for title in lst_cls_title:
        #    copy_agent.create_props(title) 
    return  lst_cls_title   