# -*- coding: utf-8 -*-
import requests 
import numpy as np
import pandas as pd
import json
from types import SimpleNamespace
from .dext_utility import *
#from utility import *
from dataclasses import dataclass

@dataclass
class HostInfo:
    url:str
    login:str
    password:str
    
    def __post_init__(self):
        self.auth=(self.login,self.password)

class JsonData():
    def __init__(self, host):
        #def __init__(self, url, login, password)
        self.host=host
        self.base_url=host.url
        self.auth=host.auth
        
        self.url=self.base_url+'getjson?listonto=all'
        self.url_onto=self.base_url+'ontomanager?action=getChildren'
        
    
    def get_ontoitem(self, obj_type, obj_name):
        """_summary_
        Возвращает элемент заданного типа и имени
        Args:
            obj_type (_type_): _description_
            obj_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        url=self.base_url+'getjson'

        par={'parent_type':obj_type, 'title':obj_name}

        response=requests.get(url, params=par, headers={'Accept': 'application/json'}, auth=self.auth)

        if response.text:
            out=json.loads(response.text)
        else:
            out={}
        
        return out
    
    def get_request(self,url,par):
        response=requests.get(url, params=par, headers={'Accept': 'application/json'}, auth=self.auth)
        out=json.loads(response.text)
        return out
    
    def get_class_by_name(self,contenttype,classname):
        out=self.get_ontoitem(contenttype,classname)
        return out #['items']
    def get_source(self,contenttype,classname):
        res=self.get_class_by_name(contenttype,classname)
        return self.get_children(res['uid'])
    
    
    def get_children(self,ouid):
        
        if ouid:
            url = self.url_onto+'&ouid='+ouid
            
            response=requests.get(url, headers={'Accept': 'application/json'}, auth=self.auth)
            out = json.loads(response.text)
            
            
            out_class={}
            out_subclass=[]
            out_dproperty=[]
            out_oproperty=[]
            out_ontology=[]
            out_submetaclass=[]
            d={}
            for o in out:
                if isinstance(o,dict):
                    data=o['data'].split(':')
                    rel=o['attr']['rel']
                    if rel=='DextOntoClass' and data[0]=='title':
                        out_class['uid']=o['attr']['id']
                        out_class['url']=o['attr']['url']
                        out_class['title']=data[1]
                    elif rel=='DextOntoClass' and data[0]=='subclass':
                        out_subclass.append({'uid':o['attr']['id'],'title':data[1]})
                    elif  rel=='DextClassDataProperty' and data[0]=='prop':
                        out_dproperty.append({'uid':o['attr']['id'],'url':o['attr']['url'],'title':data[1]})
                    elif  rel=='DextClassObjectProperty' and data[0]=='prop':
                        out_oproperty.append({'uid':o['attr']['id'],'url':o['attr']['url'],'title':data[1]})
                    elif  rel=='DextOntology' and data[0]=='ontology':
                        out_ontology.append({'uid':o['attr']['id'],'title':data[1]})
                    elif data[0]=='submetaclass':
                        out_submetaclass.append({'uid':o['attr']['id'],'title':data[1]})
            d['baseclass']=out_class
            d['subclass']=out_subclass
            d['oproperty']=out_oproperty
            d['dproperty']=out_dproperty
            d['ontology']=out_ontology
            d['submetaclass']=out_submetaclass
            return d
        else:
             return {}
    
    def delete_item(self,url):
        responce=requests.delete(url, headers={'Accept': 'application/json'}, auth=self.auth)
        return responce.status_code
    
    def get_ontoitem_info(self,contenttype,classname):
        out=self.get_class_by_name(contenttype,classname)
        res=self.get_children(out['uid'])
        return res
    
    def create_class(self,url,par):
        response=requests.post(url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json=par, auth=self.auth)
        return json.loads(response.text)
    
    
    def create_subclass(self,kw):
        url=self.base_url+'getjson'
        par={'submitted': 'True','inst_type':'DextOntoClass','mode':'subclass_add1'}
        par.update(kw)
        print('*****************create subclass*******','\n','par',par)
        requests.post(url,params=par, headers={'Accept': 'application/json'}, auth=self.auth)
    
    def get_ontolist(self):
        key_onto=tuple()
        response=requests.get(self.url, headers={'Accept': 'application/json'}, auth=self.auth)
        allonto=json.loads(response.text)

        if len(allonto):
            for i in range(len(allonto)):
                #item=allonto[i]
                self.base=dict([(item['@title'],item['@uid']) for item in allonto])
                key_onto=tuple([i for i in self.base.keys()])
        else:
            key_onto=tuple()
        
        return key_onto
    
    def get_ObjByUID(self,uid):
        url=self.url_onto+'&uid='+uid
        response=requests.get(url, headers={'Accept': 'application/json'}, auth=self.auth)
        obj=json.loads(response.text)
        return obj
    
    def get_range_by_uid(self,uid):
        url=self.url_onto+'&uid='+uid
        response=requests.get(url, headers={'Accept': 'application/json'}, auth=self.auth)
        task=json.loads(response.text)
        df = pd.DataFrame(pd.json_normalize(task))
        df[['type_obj','name']] = df['data'].str.split(pat=':',n=1, expand=True)
        x=df[df['type_obj'].isin(['rangeclass'])][['name','attr.id']]
        range_uid=df['attr.id'].tolist()[0]
        return TempOClass(self,range_uid)
    
    def add_subclass(self,obj):
        """_summary_

        Args:
            obj (_type_): _description_
        """
        d={'op':[{'sbprop_uid':x,'sel':y} for x,y in obj.op_lst],'dp':[{'sbprop_uid':x,'value':y} for x,y in obj.dp_lst]}
    
    
    def getfoldercontentbyname(self,ontoname):
        url=self.base_url+'/'+'getjson'
        par={'ontoname':ontoname}
        response=requests.get(url,params=par, headers={'Accept': 'application/json'}, auth=self.auth)
        if response.text:
            out=json.loads(response.text)
        else:
            out={}
        
        return out
class taskAgent:
	def get_tasklist(self):
		response=requests.get(self.task_url, headers={'Accept': 'application/json'}, auth=('admin', 'admin'))
		task=json.loads(response.text)
		dframe = pd.DataFrame(pd.json_normalize(task))
		dframe[['type_obj','name']] = dframe['data'].str.split(pat=':',n=1, expand=True)
		return dframe

	def get_task_by_uid(self,uid):
		url=self.url_onto+'&uid='+uid
		response=requests.get(url, headers={'Accept': 'application/json'}, auth=('admin', 'admin'))
		task=json.loads(response.text)
		df = pd.DataFrame(pd.json_normalize(task))
		df[['type_obj','name']] = df['data'].str.split(pat=':',n=1, expand=True)
		title=df[df['type_obj'].isin(['title'])][['name']]['name'].tolist()[0]
		x=df[df['type_obj'].isin(['prop'])][['name','attr.id']]
		return {'title':title, 'dframe':x}    
    
class SubOntoClassData:
	def __init__(self,inst_type,op_lst,dp_lst):
		self.inst_type=inst_type,
		self.mode='subclass_add'
		#op_lst список кортежей (uid objectproperty, uid range class)
		#dp_lst список кортежей (uid objectproperty, value - значение сыойства)


class TempOProp(object):
	def __init__(self,title, range, uid, portal_type):
		self.title=title
		self.uid=uid


class TempOClass():

	def __init__(self,agent,uid):
		self.uid=uid 
		self.data=agent
		self.req=self.data.get_task_by_uid(self.uid)
		self.title=self.req['title']
		self.df=self.req['dframe']
		self.req=''
		self.lst_cls=self.df['attr.id'].tolist()
		self.lst_name=self.df['name'].tolist()
		self.props=dict([(self.lst_name[i],self.lst_cls[i]) for i in range(len(self.lst_cls))])
		



class Task(TempOClass):
	def ___init__(self,uid):
		super().__init__(uid)
	def get_pro(self, prop_name=''):
		if prop_name:
			return self.props[prop_name]
		else:
			return self.props
class App():
	def __init__(self):
		self.data=JsonData()
		self.df=self.data.get_tasklist()
		self.df=self.df[self.df['type_obj'].isin(['submetaclass',])]
		self.lst_cls=self.df['attr.id'].tolist() #список uid щбъектов базы
		self.dict_node={}#словарь закаченнных объектов
	def get_data(self):
		dict_task={}
		dict_prop={}
		lst_task=[]
		for i in range(len(self.lst_cls)):
			node=self.lst_cls[i]#uid объекта базы
			if not node in self.dict_node.keys():
				self.dict_node[node]=Task(node)
		for k,v in self.dict_node.items():
			tmp=v.get_pro()
			for title,uid in tmp.items():
				value=self.data.get_ObjByUID(uid)[0]['data']
				if ':' in value:
					value=value.split(':')[1]
				tmp[title]=value
			tmp['name']=v.title
			tmp['task_uid']=k
			#dict_task[v.title]=tmp
			lst_task.append(tmp)
		#self.df_task=pd.DataFrame.from_dict(dict_task, orient='index')
		self.df_task=pd.DataFrame(lst_task)
		
		return self.df_task

def get_task():
	task_df=pd.read_excel('задачи.xlsx')
	
	return task_df

def get_edgs():
	lst_edgs=[{'source':'1p','target':'1а','period':30},{'source':'1p','target':'1б','period':30},
	          {'source':'1p','target':'1в', 'period':30},{'source':'1p','target':'1г','period':30},
	          {'source':'1p','target':'1д','period':30},{'source':'1p','target':'1с','period':30},
	          {'source':'1а','target':'1а1','period':15},{'source':'1а','target':'1а2','period':15},
	          {'source':'1а','target':'1а3','period':15}, {'source':'1с','target':'1с1','period':15},
	          {'source':'1с1','target':'1с1а','period':3}, {'source':'1а2','target':'1а2а','period':3},
	          {'source':'1а2а','target':'1а2а1','period':3},
	          ]
	
	return lst_edgs
def get_key_onto(self):
	"""
	возвращает кортеж  title для всех онтологий
	"""
	base_url='http://localhost:8080/Plone/'
	url=base_url+'getjson?listonto=all'
	url_onto=base_url+'ontomanager?action=getChildren'
	response=requests.get(url, headers={'Accept': 'application/json'}, auth=('admin', 'admin'))
	allonto=response.json()
	for i in range(len(allonto)):
		item=allonto[i]
	base=dict([(item['@title'],{'node_id':item['@title'],'uid':item['@uid'],'children':['*']}) for item in allonto])
	key_onto=tuple([i for i in base.keys()]) 
	return key_onto 


def get_source(agent,contenttype,classname):
    res=agent.get_class_by_name(contenttype,classname)
    
    return agent.get_children(res['uid'])



def change_class_property(agent, source_classname, property_name, target_classname):
    target_data=agent.get_class_by_name('DextOntoClass',target_classname)
    target_id=target_data['url']
    base=[{'@id':target_id}]#получили инормацию для range связи
    cls_data=agent.get_class_by_name('DextOntoClass',source_classname)
    if cls_data:
         cls_url=cls_data['url']
         requests.patch(cls_url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={property_name:base }, auth=agent.auth)



def get_department():
    kadr_df=pd.read_excel('Кадры1.xlsx')
    lst_label=kadr_df['Подразделение'].tolist()
    lst_level=kadr_df['уровень'].tolist()
    return (lst_label, lst_level)


def create_class_from_df():
    deps=pd.read_excel('Кадры1.xlsx')
    lst_label=deps['Подразделение'].tolist()
    lst_id=deps['ID'].tolist()
    classname='Элемент структуры производства'
    data=get_source(agent,classname)
    context_uid=data['baseclass']['uid']
    container_uid=data['ontology'][0]['uid']
    for i in range(len(lst_label)):
        label=str(lst_id[i])+' '+lst_label[i]
        plone_subclass(agent,context_uid,container_uid,label)



class OntoClass:
    def __init__(self, kw):
        self.kw=kw
        for k,v in kw.items():
            self.__setattr__(k,v)
    def __str__(self):
        s=[]
        for k in self.kw.keys():
            s.append(k+'='+str(self.__getattribute__(k))+'\n')
        return ''.join(s)
            
        
        


def dep_ref_from_df(df):
    lst=[]
    out=df.to_dict('records')
    for row in out:
        lst.append((row['Подразделение'],row['родитель']))
    return lst

def empty_class():
    url='http://localhost:8080/Plone/proekty/yadro-sistemy/MXTWwNx0XQZTCFOz/pustoi-klass'
    response=requests.get(url, headers={'Accept': 'application/json'}, auth=('admin', 'admin'))
    req=response.json()
    dict_class={}
    kw=prop_from_request(req)
    obj=OntoClass(kw)
    return obj

def create_OntoclassFromURl(url:str,login:str,passw:str):
    
    """Используя  RestApi создает копию OntoClass 

    Args:
        url (str): _description_
        login (str): _description_
        passw (str): _description_

    Returns:
        _type_: _description_
    """
    response=requests.get(url, headers={'Accept': 'application/json'}, auth=(login. passw))
    req=response.json()
    dict_class={}
    kw=prop_from_request(req)
    return OntoClass(kw)

    

def prop_from_request(req):
    
    key_lst=["@id","@type","UID","description","id",'title']
    kw={}
    
    for k,v in req.items():
        if k in key_lst:
            if k=='@id':
                k='url'
            if k[0]=='@':
                k=k[1:]
        kw[k]=v
    
    return kw

def get_folder_content(url, host_agent):
    """    используя plone.restapi  возвращает словарь классов {'имя DextOntoClass: объект OntoClass}
    ошибка - возвращает только часть данных, возможно нужно обновить версию

    Args:
        url (_type_): _description_
        login (_type_): _description_
        passw (_type_): _description_

    Returns:
        _type_: _description_
        
    """
    
    data={'b-size':-1}
    response=requests.get(url, params=data, headers={'Accept': 'application/json'}, auth=host_agent.host.auth)
    rs=prop_from_request(response.json())
    lst_items=response.json()['items']
    return lst_items

    


def get_ontology_content_from_listnames(agent,namelst):
	"""возвращает словарь {имя класса: объект OntoClass, построенных на основе запросов к серверу Plone

	Args:
		agent (JsonData): объект класса JData
		namelst (list): список имен классов

	Returns:
		_type_: _description_
	"""
	dict_class={}
	for classname in namelst:
		kw=agent.get_class_by_name(classname)
		obj=OntoClass(kw)
		dict_class[obj.title]=obj
		
	dict_class['pustoi-klass']=empty_class()
	return dict_class

def get_class_prop(obj_url,prop_name):
    prop=None
    response=requests.get(obj_url, headers={'Accept': 'application/json'}, auth=('admin', 'admin'))
    out=response.json()
    
    lst_items=out['items']
    for item in lst_items:
        if item['title']==prop_name:
            prop=item
            break
    return prop


#base_url='http://localhost:8080/Plone/'
#agent=JsonData(base_url, 'admin','admin')


