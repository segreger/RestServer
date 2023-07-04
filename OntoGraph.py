# -*- coding: utf-8 -*- import *
import pdb
from Graph import Node, Graph,Relation
from RestApi.get_data import *
from RestApi.ontomodeler_lib import *


import json
import requests
class OntoGraph:
    
    def __init__(self,mng, classname):
        self.classname=classname
        self.nodes={}#Словарь всех узлов,ключ - имя узла
        self.edges=[]# список ребер между объектами Node
        self.dict_name={}
        self.agent=mng.host_agent
        cls=self.agent.get_class_by_name('DextOntoClass',classname)
        self.uid=cls['uid']
        self.root=self.agent.get_children(self.uid)
        self.uid=cls['uid']
        self.title=self.root['baseclass']['title']
        self.uid=self.root['baseclass']['uid']
        self.url=self.root['baseclass']['url']
        self.root_oprops=self.root['oproperty']
        self.lst_prop=[{'title':p['title'],'uid':p['uid']} for p in self.root_oprops]
        self.props=[]
    def getChildren(self):
        for i in self.root_oprops:
            title=i['title']
            uid=i['uid']
            self.props.append({})
class OntoGraphTitle(Graph):
    def __init__(self, mng, classname):
        super().__init__()
        self.classname=classname
        self.agent=mng.host_agent
        self.class_wu=self.get_class_wu()
        #self.nodes[self.classname]=self.class_wu
        self.get_graph()
        self.nodes[self.classname]=self.class_wu
    def get_nodes(self):
        res_source=DextWorkUnit('',source_cls.url, self.agent).getWUnit()
    def get_class_wu(self):
        source_class=self.agent.get_class_by_name('DextOntoClass',self.classname)
        res_source=DextWorkUnit('',source_class['url'],self.agent).getWUnit()
        return res_source

    def get_graph(self):
        for title,prop in self.class_wu.children.items():
            print('title',title)
            if prop.range:
                source=self.class_wu
                if prop.content_type=='DextClassObjectProperty':
                    target_name=prop.range[0]
                elif prop.content_type=='DextClassDataProperty':
                    target_name=prop.range
                if target_name:
                    print('target_name',target_name)
                    target_class=self.agent.get_class_by_name('DextOntoClass',target_name)
                    print(target_class)
                    target_wu=DextWorkUnit('',target_class['url'],self.agent).getWUnit()
                    self.nodes[target_name]=target_wu
                    rel=Relation(title=title, source=source,target=target_wu)
                    self.edges.append(rel)
    def elements(self):
        lst_nodes=[ {'data': {'id': k, 'label': v.title, 'width': '500px','height': '150px',},'classes':'multiline-auto', } for k,v in self.nodes.items()]

        
        lst_edges=[{'data': {'source': edg.source.title, 'target': edg.target.title}} for edg in self.edges]

        return lst_nodes+lst_edges 

    def __str__(self):
        out=''
        for n,v in self.nodes.items():
            out=out+'\n'+v.title+'\n'
            for i in v.children:
                out=out+'\t'+i+'\n'
        return out


class OntoClassNode(Node):
    def __init__(self, mng, uid_class=None,classname=None,**kwargs):
        self.agent=mng.host_agent
        if uid_class:

            self.uid=uid_class
        if classname:
            cls=self.agent.get_class_by_name('DextOntoClass',classname)
            self.uid=cls['uid']
        self.root=self.agent.get_children(self.uid)
        self.uid=cls['uid']
        self.title=self.root['baseclass']['title']
        self.uid=self.root['baseclass']['uid']
        self.url=self.root['baseclass']['url']
        self.root_oprops=self.root['oproperty']
        self.lst_prop=[{'title':p['title'],'uid':p['uid']} for p in self.root_oprops]
        self.props=[]
    def getCildren(self):
        for i in self.root_oprops:
            title=i['title']
            uid=i['uid']
            self.props.append({})






def get_classnode():
    cls_item=agent.get_ontoitem_info(classname)
    props=[]
    for i in cls_item['oproperty']:
        title=i['title']
        uid=i[uid]
        range=agent.get_children(uid)
        root_title=root['baseclass']['title']
        root_uid=root['baseclass']['uid']
        root_url=root['baseclass']['url']

def get_ontology_graph(source_agent,ontoname):
    source_onto=source_mng.host_agent.get_class_by_name('DextOntology',ontoname)
    res_source=DextWorkUnit('',source_onto['url'],source_mng.host_agent).getWUnit()

def get_class_graph(source_mng, classname):
    source_class=source_mng.host_agent.get_class_by_name('DextOntoClass',classname)
    res_source=DextWorkUnit('',source_class['url'],source_mng.host_agent).getWUnit()
    return res_source
     
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_url='http://ontogovorun.ru/'
target_host=HostInfo(target_url,target_login, target_passw)
target_agent=JsonData(target_host)
target_mng=ModelManager(target_agent)

"""
source_cls=get_class_graph(target_mng, 'Подразделение')
res_source=DextWorkUnit('',source_cls.url, target_mng.host_agent).getWUnit()
props={}
props_lst=[]
for title,prop in res_source.children.items():
    props={}
    props[title]=[prop.content_type,prop.range]
    print(props)
    props_lst.append(props)
"""
#cls_node=OntoClassNode(agent, uid_class)
#cls_node=OntoClassNode(target_mng, None,'Подразделение')
#cls_node.getChildren()

