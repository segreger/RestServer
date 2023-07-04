# -*- coding: utf-8 -*-
import requests
import json
#from get_data import *
from .ontoclassWU import *

#import pandas as pd
#import nympy as np

def create_res(url,lst_title,contenttype,value):
    login='admin'
    passw='ykgI2Krwt1Uz'
    
    #url='http://ontogovorun.ru:8090/Plone/proekt'
    for title in lst_title:
        
        if contenttype=='DextClassDataProperty':
            responce=requests.post(url, headers={'Accept': 'application/json',
                 'Content-Type': 'application/json'}, json={'@type': 'DextClassDataProperty', 'title': title,'value':value}, auth=(login, passw))
        else:
            responce=requests.post(url, headers={'Accept': 'application/json',
                 'Content-Type': 'application/json'}, json={'@type': contenttype, 'title': title}, auth=(login, passw))
        print(responce.status_code)
        
def get_itemlist(source_host,target_host, contenttype):
    """
    получает как параметр объект класса HostInfo
    """
    url_source=source_host.url
    source_auth=source_host.auth
    response=requests.get(url_source, headers={'Accept': 'application/json'}, auth=source_host.auth)
    #allonto=response.json()
    out=json.loads(response.text)
    """
    url_target=target_host.url
    login_target='admin'
    passw_target='ykgI2Krwt1Uz'
    """
    target_auth=target_host.auth 
    
    """  
    # создание копий классов 
    for c in out['items']:
        print(c['title'])
        

        #requests.post(url, headers={'Accept': 'application/json',
        #         'Content-Type': 'application/json'}, json={'@type': 'DextOntoClass', 'title': c['title']}, auth=(login_target, passw_target))
    """    
    #создание копий связей
    for obj in out['items']:
        ref_cls=obj['@id']
        ref_response=requests.get(ref_cls, headers={'Accept': 'application/json'}, auth=source_auth)
        out_ref=json.loads(ref_response.text)
        for ref in out_ref['items']:
           
            requests.post(target_host.url, headers={'Accept': 'application/json',
                    'Content-Type': 'application/json'}, json={'@type': contenttype, 'title': c['title']}, auth=target_auth)
            
    return 1
def create_cls():
    """
            title=v.name_plant
        if title != 'empty_class':
            if v.dep_type=='служба':
                indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid1,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
            elif v.dep_type=='подразделение':
                indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}    
            agent.create_subclass(indata)
   """
   
#lst_title=["Задания библиотека","Производство_Онтология задач","Производство_агенты","Производство_Обращение к агенту","Онтология заданий"]#
#create_res()
"""
#lst_cls=get_itemlist('http://localhost:8080/Plone/proekty/proekt-proizvodstvo/struktura-organizacii/struktura','admin', 'admin')
source_url='http://localhost:8080/Plone/proekty/proekt-proizvodstvo/struktura-organizacii'
source_login='admin'
source_passw='admin'
source_host=HostInfo(source_url,source_login, source_passw)
target_url='http://ontogovorun.ru:8090/Plone/proekt/struktura-organizacii'
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_host=HostInfo(target_url,target_login, target_passw) 
"""

# сравнение списка классов источника и цели


def create_dp_target_copy(prop, contenttype):
    if prop.range:
        range_title=prop.range[0]['title']
        if range_title=='StringType':
            value='_'
        elif range_title=='IntegerType':
            value='0'
        #print(title,prop.range[0])
        create_res(target_cls['url'], [title], prop.content_type, value)

def create_op_target_copy(target_agent, prop, contenttype):
    if prop.range:
        
        if contenttype=='DextClassDataProperty':
            range_title=prop.range[0]['title']
        elif contenttype=='DextClassObjectProperty':
            print(contenttype, prop.range[0])
            range_title=prop.range[0]
            print('range_title',range_title)
        target_cls=target_agent.get_class_by_name('DextOntoClass', range_title)
        if not target_cls and range_title:
            return range_title
        else: return ''

"""
res=DextWorkUnit('',source_url).getWUnit()
for k,v in res.children.items():
    serv_class=serv_agent.get_class_by_name(k)
    print(serv_class)
    
    if serv_class:
        print(serv_class['url'])
        for title, obj  in v.children.items():
            print (title, obj.content_type)
            print(serv_class['url'])
            #response=requests.post(serv_class['url'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'@type': obj.content_type, 'title': title}, auth=target_host.auth)
            response=requests.post(serv_class['url'], headers={'Accept': 'application/json',
                 'Content-Type': 'application/json'}, json={'@type': obj.content_type, 'title': title}, auth=(target_login, target_passw))
            
            # print response
            print(response)
            # print request status_code
            print(response.status_code)

"""
                
#'Производство_Онтология задач','Производство_агенты','Производство_Обращение к агенту',]
#lst_title=['Онтология заданий','Задания библиотека']
#['Онтология структур'б"Библиотека подразделений","Библиотека должностей","Библиотека подразделений","Библиотека сотрудников"]
#create_res('http://ontogovorun.ru:8090/Plone/proekt/struktura-organizacii', lst_title, "DextOntology")
def ontomodel_copy(lst_title):
    nonerange=[]
    for ontoname in lst_title:
        
        source_onto=source_agent.get_class_by_name('DextOntology',ontoname)
        
        res_source=DextWorkUnit('',source_onto['url']).getWUnit()
        target_onto=target_agent.get_class_by_name('DextOntology',ontoname)
        lst_title=[i.title for i in res_source.children.values()]    
        #create_res(target_onto['url'], lst_title, "DextOntoClass")
        for title,obj in res_source.children.items():
            print(title,obj.children)
            #serv_class=source_agent.get_class_by_name(title,obj.content_type)
            #print(serv_class)
            target_cls=target_agent.get_class_by_name('DextOntoClass',obj.title)
            if not target_cls:
                response=requests.post(target_onto['url'], headers={'Accept': 'application/json',
                        'Content-Type': 'application/json'}, json={'@type': 'DextOntoClass', 'title': title}, auth=(target_login, target_passw))
            else:
                for title,prop in obj.children.items():
                    if prop.content_type=='DextClassObjectProperty':
                        create_res(target_cls['url'],[title],prop.content_type,'')
                    elif prop.content_type=='DextClassDataProperty' and prop.range:
                        #target_range=target_agent.get_class_by_name('DextOntoClass',prop.range[0])
                        range_title=prop.range[0]['title']
                        if range_title=='StringType':
                            value='_'
                        elif range_title=='IntegerType':
                            value='0'
                        create_res(target_cls['url'], [title], prop.content_type, value)
                    
                    if prop.content_type=='DextClassObjectProperty' or prop.content_type=='DextClassDataProperty':

                        nonename=create_op_target_copy(target_agent, prop, prop.content_type)
                        if nonename and nonename not in nonerange:
                            nonerange.append(nonename)
    print(nonerange)
#['empty_class', 'Задача', 'Системный агент СУЗ', 'Спецификация представления семантического узла ', 'Задача системы', 'Спецификация задачи', 'статус задачи СУЗ', 'Комментарий  к задаче', 'Метод СУЗ', 'Обращение к агенту Создать подкласс']
                
              
"""
        if serv_class:
            pass
            
            #Создаем свойства
            print(serv_class['url'])
            for title, obj  in v.children.items():
                #Этап 1 создание классов в онтологии
                print (title, obj.content_type)
                #print(serv_class['url'])
                #response=requests.post(serv_class['url'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'@type': obj.content_type, 'title': title}, auth=target_host.auth)
                response=requests.post(serv_class['url'], headers={'Accept': 'application/json',
                    'Content-Type': 'application/json'}, json={'@type': obj.content_type, 'title': title}, auth=(target_login, target_passw))
                
                # print response
                #print(response)
                # print request status_code
                print(response.status_code)
            #print(obj.title,obj.children)
            
        for obj in res_source.children.values():
            target_cls=target_agent.get_class_by_name('DextOntoClass',obj.title)
            target_cls_wu=DextWorkUnit('',target_cls['url']).getWUnit()
            
            #info_cls=target_agent.get_children(target_cls['uid'])
            #print(info_cls)
            #print('url',target_cls['url'])
        
        for title, prop  in obj.children.items():
            if prop.content_type=='DextClassDataProperty':
                pass
                #create_dp_target_copy(prop, prop.contenttype)
                
                if prop.range:
                    #target_range=target_agent.get_class_by_name('DextOntoClass',prop.range[0])
                    range_title=prop.range[0]['title']
                    if range_title=='StringType':
                        value='_'
                    elif range_title=='IntegerType':
                        value='0'
                    print(title,prop.range[0]['title'])
                    #print (title, prop.content_type)
                    create_res(target_cls['url'], [title], prop.content_type, value)
                
            if prop.content_type=='DextClassObjectProperty' or prop.content_type=='DextClassDataProperty':

                nonename=create_op_target_copy(target_agent, prop, prop.content_type)
                if nonename and nonename not in nonerange:
                    nonerange.append(nonename)
            #print(nonerange)
                
            #target_prop=target_agent.get_class_by_name(prop.content_type,title)
        
"""
"""
url='http://ontogovorun.ru:8090/Plone/proekt/struktura-organizacii/struktura/sluzhba'
#target_cls=target_agent.get_class_by_name('DextOntoClass','Служба')
#res=target_agent.get_children(target_cls['uid'])
response=requests.post(url, headers={'Accept': 'application/json',
                 'Content-Type': 'application/json'}, json={'@type': 'DextClassDataProperty', 'title': 'test1','value':'uu'}, auth=(target_login, target_passw))
print(response.status_code)
res=get_folder_content(url, target_login,target_passw)
print(res)
"""


