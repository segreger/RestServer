# -*- coding: utf-8 -*-
from get_data import JsonData
import requests 
data=JsonData('http://localhost:8080/Plone/')
classname='Элемент структуры производства'
classname1='Директор по производству'
classname2='Тип задания'
out=data.get_class_by_name(classname2)
ouid=out['uid']
children=data.get_children(ouid)

#print(out['@type'])
def create_class():

    base=[{'@id':out['@id']}]
    url='http://localhost:8080/Plone/'
    d_json={'@type': 'DextOntoClass', 'title': 'MyDocument'}
    cls_data=data.create_class(url,d_json)
    #cls_data=data.get_class('MyDocument')
    cls_url=url+'/'+cls_data['@id']
    requests.patch(cls_url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'subClassOf':base }, auth=('admin', 'admin'))


