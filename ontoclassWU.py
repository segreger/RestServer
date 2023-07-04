# -*- coding: utf-8 -*-
import pdb
import json
import requests
from .get_data import *
"""
from onto.utility.global_utility import *
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import addContentToContainer, createContent
from Acquisition import aq_inner
from zope import component
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog
from zope.lifecycleevent import modified
from zope.component.hooks import getSite
from z3c.relationfield import RelationValue
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from onto.ontotypes.interfaces import IWorkUnit
from plone.protect import PostOnly
from plone.protect import protect
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import _createObjectByType
from search_utility import *
"""
"""
source_url='http://localhost:8080/Plone/proekty/proekt-proizvodstvo/struktura-organizacii'
source_login='admin'
source_passw='admin'
source_host=HostInfo(source_url,source_login, source_passw)
target_url='http://ontogovorun.ru:8090/Plone/proekt/struktura-organizacii'
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_host=HostInfo(target_url,target_login, target_passw)
"""

def dextempty_class():
    portal = getPortal()
    folder_onto=getDextByNameAndPath(u'Проекты', portal,'Folder')
    ontotitle=u'онтология инфоэлементов'
    dext_onto=getDextByNameAndPath(ontotitle, folder_onto,'DextOntology')
    empty_cls=getDextByNameAndPath(u'empty_class', dext_onto,'DextOntoClass')
    #empty_cls=getDextByNameAndPath(u'пустой класс',portal,'DextOntoClass')
    return empty_cls


def getObjFromRList(range):
    """
    по списку RelationValues возвращает список объектов
    """
    intids = getUtility(IIntIds)
    rangelist=[]
    if range:
        rvalues = [RelationValue(intids.getId(c)).to_object for c in range]
    else:
        rvalues = [RelationValue(intids.getId(c)).to_object for c in [dextempty_class()]]
    for r in rvalues:
        if isinstance(r,RelationValue):
            obj=r.to_object
            if obj:
                rangelist.append(obj)
            else:
                cl=dextempty_class()
                rangelist.append(cl)    
    return rangelist
source_login='admin'
source_passw='admin'
login_target='admin'
passw_target='ykgI2Krwt1Uz'

class DextWorkUnit(object):
    
    def __init__(self,cls,url,host_agent):
        source_login='admin'
        source_passw='admin'
        login_target='admin'
        passw_target='ykgI2Krwt1Uz'
        self.wunit={}
        self.url=url
        self.cls=cls
        self.content_type=''
        self.host_agent=host_agent
        if self.cls:
            self.context=self.cls
            self.title=self.cls.title
        else:
            response=requests.get(self.url, headers={'Accept': 'application/json'}, auth=self.host_agent.host.auth)
            rs=prop_from_request(response.json())
            self.content_type=rs['type']
            self.uid=rs['UID']
            self.title=rs['title']
    
    
    def getWUnit(self):
        if self.content_type=='DextOntology':return DextOntologyWU('',self.url,self.host_agent).getWUnit()
        elif self.content_type=='DextOntoClass':return DextOntoClassWU('',self.url,self.host_agent).getWUnit()
        elif self.content_type=='DextClassObjectProperty':return DextClassObjectPropertyWU('',self.url,self.host_agent)
        elif self.content_type=='DextClassDataProperty':return DextClassDataPropertyWU('',self.url,self.host_agent).getWUnit()
        elif self.content_type=='DextOntology':return DextOntologyWU('',self.url,self.host_agent).getWUnit()
        else:return {}
    


class DextOntologyWU(DextWorkUnit):
    def __init__(self,cls,url,host_agent):
        super(DextOntologyWU, self).__init__(cls,url, host_agent)
        self.children={}
        self.content_type='DextOntology'

    def getWUnit(self):
        #lst_items=get_folder_content(self.url, self.host_agent)
               
        lst_items=self.host_agent.getfoldercontentbyname(self.title)
        for i in lst_items:
            
            
            kw=prop_from_request(i)
            obj=DextWorkUnit('',kw['url'],self.host_agent).getWUnit()
            self.children[obj.title.strip()]=obj
        return self
    def get_root(self):
        return self.root


class DextOntoClassWU(DextWorkUnit):
    def __init__(self,cls,url, host_agent):
        
        super(DextOntoClassWU, self).__init__(cls,url,host_agent)
        self.children={}
        self.host_agent=host_agent
        self.content_type='DextOntoClass'
    def getWUnit(self):
        ch=self.host_agent.get_children(self.uid)
      
        child=ch['oproperty']+ch['dproperty']
        
        for i in child:
            #kw=prop_from_request(i)
            obj=DextWorkUnit('',i['url'],self.host_agent).getWUnit()
            self.children[obj.title.strip()]=obj

        return self

    def getWUProperty(self,prop_type):
        oplist=[]
        dict_prop={}
        """
        for op in getDextItemByPath(self.context,prop_type):
            PrnVal('op.UID()' ,op.UID())
            yield op.UID()
        """

        #return [oprop.UID() for oprop in getDextItemByPath(self.context,prop_type)]
        return [uid for uid in getDextItemUIDByPath(self.context,prop_type)]

        
         
    def ListDRangeItems(self):
        return [i.UID() for i in self.context.getDataProps()]


    def ListDPropWU(self):
        return [DextClassDataPropertyWU('',i) for i in self.dprop1]
    def ListOPropWU(self):
        return [DextClassObjectPropertyWU('',i) for i in self.oprop]

    def getPropWUByName(self, source,nameop=''):
        #nameop=DelSpaceToUTF(nameop)
        for k,v in source.items():
            if toUTF(nameop)==k:
                return v 
        else:
            return ''

    def getDictObjectProps(self):
        lst=self.ListOPropWU()
        source=dict([(toUTF(i.prop_name),i) for i in lst if i])
        return source
    def getDictObjectPropsUID(self):
        lst=self.ListOPropWU()
        source=dict([(toUTF(i.prop_name),i.uid) for i in self.ListOPropWU() if i])
        return source
    def getObjectPropWUByName(self, nameop=''):
        lst=[]
        source=dict([(toUTF(i.prop_name),i) for i in self.ListOPropWU() if i])
        return self.getPropWUByName( source,toUTF(nameop))

    def getDataPropWUByName(self, namedp=''):
        """
        возвращает ClassDataPropertyWU с указанным именем
        """
        nameop= DelSpaceToUTF(namedp)
        dprops = [WorkUnit(i).getWUnit(i) for i in self.dprop1]
        source = dict([(dprop.prop_name, dprop) for dprop in dprops])
        return source[namedp]
    def getDataPropWUByName_Value(self, namedp=''):
        """
        возвращает значение ClassDataPropertyWU с указанным именем
        """
        #unamedp= DelSpaceToUTF(namedp)
        unamedp= DelSpaceToUTF(namedp)
        dprops = [DextClassDataPropertyWU('',i) for i in self.dprop1]
        source = dict([(DelSpaceToUTF(dprop.prop_name), dprop.value) for dprop in dprops])
        if source and unamedp in source.keys():
            return source[unamedp] 
        else:
            return ''



    def getDProps(self,dictname):
        out={}

        for k,v in dictname.items():
            out[k]=self.getDataPropWUByName_Value(v)
        return out



    def getDictOPropsByName(self):
        out=dict([(DelSpaceToUTF(DextClassObjectPropertyWU('',i).prop_name),DextClassObjectPropertyWU('',i)) for i in self.oprop if i])
        return out
    def getDictDPropsByName(self):
        #return dict([(DextClassDataPropertyWU('',i).prop_name,DextClassDataPropertyWU('',i).value) for i in self.dprop1 if i])              
        return dict([(DextClassDataPropertyWU('',i).prop_name,DextClassDataPropertyWU('',i).value) for i in self.dprop1 if i])              


class DextClassObjectPropertyWU(DextWorkUnit):
    def __init__(self,cls,url,host_agent):
        super(DextClassObjectPropertyWU, self).__init__(cls,url,host_agent)
        self.content_type='DextClassObjectProperty'
        self.url=url
        self.range=[]
        response=requests.get(self.url, headers={'Accept': 'application/json'}, auth=self.host_agent.host.auth)
        out=json.loads(response.text)
        key_lst=["@id","@type","UID","description","id",'title','range']
        kw={}
        
        for k,v in out.items():
                       
            if k in key_lst:
                if k=='@id':
                    k='url'
                if k[0]=='@':
                    k=k[1:]
            kw[k]=v
        if 'range' in list(kw.keys()):
            if kw['range']:
                for r in kw['range']:
                    if r:
                        self.range.append(r['title']) 
        
              
        #self.range=kw['range']
        self.title=kw['title']
        """
        self.op_uid=self.context.nameproperty or ''
        self.prop_name=self.context.title
        self.orange=self.wu_rangeitem()
        self.uid=self.context.UID()
        self.dict_props=self.getDictProps()
        """
    def getDictProps(self):
        temp = {}
        if self.cls:
            temp['domain'] = self.cls.UID()
        else:
            temp['domain'] = ''
        temp['name'] =self.prop_name
        temp['nameproperty'] = self.parent_prop()
        temp['orange']=self.rangeitem()
        temp['uid']=self.context.UID()
        temp['cls']=self.context
        return temp

    def getWUnit(self):
        return self
    def wu_rangeitem(self):
        rlst=self.rangeitem()
        if rlst:
            rangeitem=[DextWorkUnit('',r[2]).getWUnit() for r in rlst]
        else:
            rangeitem=[DextWorkUnit(r,'').getWUnit() for r in dextempty_class()]
        return rangeitem


    def rangeitem(self):
        intids = getUtility(IIntIds)
        rangelist=[]
        if self.range  and isinstance(self.range[0],RelationValue):
            rvalues=self.range
        elif self.range  and not isinstance(self.range[0],RelationValue):
            rvalues = [RelationValue(intids.getId(c)).to_object for c in self.range]
        elif not self.range:
            rvalues = [RelationValue(intids.getId(c)).to_object for c in [dextempty_class()]]
     
        for r in rvalues:
            if isinstance(r,RelationValue):
                obj=r.to_object
                if obj:
                    rangelist.append((obj.title_or_id(), obj.absolute_url(), obj.UID(), self.op_uid))
                else:
                    cl=dextempty_class()
                    rangelist.append((cl.title_or_id(), cl.absolute_url(), cl.UID(), self.op_uid))

            else:
                rangelist.append((r.title_or_id(), r.absolute_url(), r.UID(), self.op_uid))
        return rangelist

    def parent_prop(self):
        intids = getUtility(IIntIds)
        if self.op_uid:
            values = [RelationValue(intids.getId(c)).to_object for c in self.op_uid][0]
            return values.to_object.UID()
        else:
            values='None'
        return values
    
    def getRelationRange(self):
        values=[]
        intids = getUtility(IIntIds)
        if self.range:
            rvalues=[]
            for r in self.range:
                if isinstance(r,RelationValue) and r.to_object:
                    ob=r.to_object
                    if not ob:
                        ob=dextempty_class()
                if isinstance(r,RelationValue) and not r.to_object:
                        ob=dextempty_class()
                if r and not isinstance(r,RelationValue):
                    ob=r
                rvalues.append(ob)

        else:
            rvalues=[dextempty_class()]
        return rvalues



class DextClassDataPropertyWU(DextWorkUnit):
    def __init__(self,cls,url,host_agent):
        super(DextClassDataPropertyWU, self).__init__(cls,url,host_agent)
        self.content_type='DextClassDataProperty'
        response=requests.get(self.url, headers={'Accept': 'application/json'}, auth=(source_login,source_passw))
        out=json.loads(response.text)
        key_lst=["@id","@type","UID","description","id",'title','range']
        kw={}
        for k,v in out.items():
            if k in key_lst:
                if k=='@id':
                    k='url'
                if k[0]=='@':
                    k=k[1:]
            kw[k]=v
        self.range=kw['range'][0]['title']
        self.title=kw['title']
        
        """
        self.range=self.context.range
        self.sbprop_uid=self.context.nameproperty
        self.prop_name=self.context.title
        self.value=self.context.value
        self.id=self.context.id
        self.uid=self.context.UID()
        self.prop_info={}
        self.prop_info['prop_name']=self.prop_name
        self.prop_info['def_value']=self.value
        self.prop_info['prop_uid']=self.uid
        self.prop_info['sbprop_uid']=self.sbprop_uid
        self.prop_info['prop_url']=self.cls.absolute_url()
        #rangelist.append((obj.title_or_id(), obj.absolute_url(),self.id,self.value, self.prop_name, self.uid)) 
        self.wunit['RangeInfo']=self.rangeitem()
        self.wunit['PropInfo']=self.prop_info
        """

    def getWUnit(self):
         return self

    def getDictProps(self):
        temp = {}
        if self.cls:
            temp['domain'] = self.cls.UID()
        else:
            temp['domain'] = ''
        temp['name'] =self.prop_name
        temp['nameproperty'] = self.sbprop_uid
        temp['orange']=self.range
        temp['value']=self.value
        temp['uid']=self.context.UID()
        temp['cls']=self.context
        temp['range']=self.rangeitem()
        return temp

    def rangeitem(self):
        intids = getUtility(IIntIds)
        rangelist=[]
        if self.range:
            #rvalues = [RelationValue(intids.getId(c)).to_object for c in self.range]
            rvalues=self.range
        else:
            rvalues=[RelationValue(intids.getId(dextempty_class())).to_object]
        for r in rvalues:
            if isinstance(r,RelationValue):
                obj=r.to_object
                rangelist.append((obj.title_or_id(), obj.absolute_url(),obj.UID(),self.id,self.value, self.prop_name, self.uid)) 
            else:
                rangelist.append(('', '',self.id,self.uid, self.value, self.prop_name, self.sbprop_uid))   
        return rangelist


    def parent_prop(self):
        intids = getUtility(IIntIds)
        if self.sbprop_uid:
            values = [RelationValue(intids.getId(c)).to_object for c in op_uid][0]
            return values.UID()
        else:
            values='None'
            return values
    def getRelationRange(self):
        if self.range:
            values=[]
            for c in self.range:
                if isinstance(c,RelationValue):
                    values.append(c.to_object )
                else:
                    values.append(dextempty_class())
        return values
