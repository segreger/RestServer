# -*- coding: utf-8 -*-
from ontomodeler_lib import *
import requests
import json
from get_data import *
from ontoclassWU import *
from dataclasses import dataclass
from ploneserver_utility import *

#parent_class_uid=target_mng.host_agent.get_class_by_name('DextOntoClass','Сотрудник')['uid']
def set_metaclass(target_agent,ontoname,nameclass):

    parent_data=target_mng.host_agent.get_class_by_name('DextOntoClass',nameclass)
    parent_url=parent_data['url']
    target_onto=target_mng.host_agent.get_class_by_name('DextOntology',ontoname)
    base=[{'@id':parent_url}]#получили инормацию для range связи
    if target_onto:
        res_source=DextWorkUnit('',target_onto['url'],target_mng.host_agent).getWUnit()
        lst_title=[(i.title,i.url) for i in res_source.children.values()]
        
        for item in lst_title:
            title=item[0]
            target_cls=target_mng.host_agent.get_class_by_name('DextOntoClass', item[0])
            if target_cls:
                
                #change_class_property(target_mng.host_agent,'DextOntoClass', title, 'hasMetatype', 'Сотрудник')
                cls_url=item[1]
                print(title, cls_url)
                #requests.patch(cls_url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':range_url }, auth=target_mng.host_agent.auth)
                requests.patch(cls_url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'hasMetatype':[parent_url]}, auth=target_host.auth)

def equal_class(g,ontoname):
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




#container=target_agent.get_ontoitem('DextOntology',ontoname)

#change_class_property(agent,portal_type, classname, property_name, target_name):
def n():
    """
	меняет свойство системное свойство объекта:SubClassOf, hasMetatype, range и т.п
	класс для range свойства создается
	portal_type - строка имени контент типа
	classname - строка имя элемента, у которого меняется свойство
	property_name - имя свойства
	target_id - uid элемента, на которое ссылается свойство

	"""
source_login='admin'
source_passw='admin'
target_login='admin'
target_passw='ykgI2Krwt1Uz'

target_url='http://ontogovorun.ru:8090/Plone/proekt/'
target_host=HostInfo(target_url,target_login, target_passw)
target_agent=JsonData(target_host)
target_mng=ModelManager(target_agent)

ontoname='Библиотека подразделений' 
nameclass='Подразделение'
#set_metaclass(target_agent,ontoname,nameclass)   