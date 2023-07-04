# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class Node:
    def __init__(self,name='',id_node=''):
        self.name=name
        self.id_node=id_node
        self.value=None
        self.children=[]




class NodeStorage:
    def __init__(self):
        self.nodes=[]
    def search_node(self,name_node):
        for n in self.nodes:
            if  n.name==name_node:
                return n 
            else:
                continue
        return None
class Relation:
    def __init__(self,title,source,target):
        self.title=title
        self.rel_type=''
        self.source=source
        self.target=target

class RelStorage:
    def __init__(self):
        self.rels=[]
    def search_rel(self,rel_type):
        res=[]
        
        for n in self.rels:
            if  n.rel_type==rel_type:
                res.append(n)

        return res
class NodeValue:
    def __init__(self,name_id,name_plant, name_ref,dep_type, level):
        self.name_id= name_id
        self.name_plant=name_plant
        self.name_ref=name_ref
        self.dep_type=dep_type
        self.level=level

    def __str__(self):
        out="Узел " +self.name_plant+"\n"+'id='+self.name_id+'\n'+'ref='+self.name_ref+'\n'+'type='+self.dep_type+'\n'+'level='+self.level
        return out
  

class Graph:
    def __init__(self):
        self.nodes={}#Словарь всех узлов,ключ - имя узла
        self.edges=[]# список ребер между объектами Node
        self.dict_name={}

    def __str__(self):
        out=''
        for n,v in self.nodes.items():
            out=out+'\n'+v.name+'\n'
            for i in v.children:
                out=out+'\t'+i+'\n'
        return out
 

