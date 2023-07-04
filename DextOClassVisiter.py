# -*- coding: utf-8 -*-
import pdb
from plone.uuid.interfaces import IUUID
import zope.interface
from onto.ontotypes.dext_utility import *
from onto.ontotypes.DextOntology import IDextOntology
from plone.uuid.interfaces import IUUID
from .interfaces import *
from onto.utility.ref_utility import *
from onto.ruleengine.rule_define import *
from plone.app.linkintegrity.utils import *
from DextVisiter import Visiter

class DextOClassVisiter(Visiter):
    zope.interface.implements(IVisiter)
    def __init__(self,obj):
        self.obj=obj
        self.output=[]
        self.class_rule=[]
        self.class_rule.append({'rulename':'info','agent':self.getInfo,'templ':{'obj':self.obj}})
        self.class_rule.append({'rulename':'модуль онтологии','agent':self.getParentOntology,'templ':{'obj':self.obj}})
        self.class_rule.append({'rulename':'список свойств','agent':self.ListChidren,'templ':{'obj':self.obj}})
        self.class_rule.append({'rulename':'список метаклассов','agent':self.ListClassOfMetaclass,'templ':{'obj':self.obj}})
        self.class_rule.append({'rulename':'родительский класс','agent':self.hasParent,'templ':{'obj':self.obj}})
        self.class_rule.append({'rulename':'список классификаторов','agent':self.ListKindOf,'templ':{'obj':self.obj}})
        self.class_rule.append({'rulename':'список подклассов','agent':self.Class_observer,'templ':{'obj':self.obj,'ref_type':'subclass'}})
        self.class_rule.append({'rulename':'список расширений','agent':self.ListChildOfMetaclass,'templ':{'obj':self.obj}})
        self.execrule=ListRuleExecutor()
        self.execrule.add_from_list(self.class_rule)

    
    def children(self):
        output=[]
        r=self.execrule.rules_execute()
        return r

    def getInfo(self,kw):
        obj=kw['obj']
        output=insert_outmeta(self.output, 'title:'+self.obj.title_or_id(), self.obj)
        print('getInfo',output)
        return output

    def getParentOntology(self,kw):
        obj=kw['obj']
        lst=[]
        output=[]
        if obj:
            lst.append(ParentFolder(obj))
            if lst:
                for op in lst:
                    output=insert_outmeta(output, 'ontology:'+op.title_or_id(), op)
        else:
            output=[]
        return output


    def hasParent(self, kw):
        obj=kw['obj']
        output=[]
        if obj and obj.subClassOf:
            for op in obj.subClassOf:
                if op.to_object:
                    output=insert_outmeta(output, 'parent:'+op.to_object.title_or_id(), op.to_object)
        return output


    def ListChidren(self, kw):
        obj=DextWorkUnit(kw['obj'],'').getWUnit()
        output=[]
        out=[TempOProp(p.prop_name, p.range, p.uid, p.absolute_url, p.portal_type) for p in obj.ListOPropWU()]
        #prop_lst=[DextWorkUnit(ObjByUID(p_uid),'').getWUnit() for p_uid in obj.oprop]
        for tmpop in out:
            output=insert_outmeta(output, 'prop:'+tmpop.title, tmpop)
        out=[TempOProp(p.prop_name, p.range, p.uid,p.absolute_url, p.portal_type) for p in obj.ListDPropWU()]
        for tmpop in out:
            output=insert_outmeta(output, 'prop:'+tmpop.title, tmpop)
        if not output:
            tmpop=TempOProp('empty', 'empty', 'empty','empty')
            output=insert_outmeta(output, 'prop:'+tmpop.title, tmpop)
        return output



    def ListMetatype(self, obj):
        output=[]
        if obj and obj.hasMetatype:
            for op in obj.hasMetatype:
                if op:
                    output=insert_outmeta(output, 'meta:'+op.title_or_id(), op)
        return output


    def ListInd(self, kw):
        obj=kw['obj']
        output=[]
        if obj and getListInd(obj.UID()):
            for op in getListInd(obj.UID()):
                if op:
                    output=insert_outmeta(output, op.title_or_id(), op)
        return output

    def ListKindOf(self, kw):
        obj=kw['obj']
        output=[]
        
        if obj and obj.hasKindOf:
            ops = [c.to_object for c in obj.hasKindOf]
            output=[insert_outmeta(output, 'classif:'+op.title_or_id(), op) for op in ops]
        return output

    def Class_observer(self, kw):
        obj=kw['obj']
        ref_type=kw['ref_type']
        output=[]
        out=back_references(obj, 'subClassOf')
        for item in out:
            output=insert_outmeta(output, 'subclass:'+item.title_or_id(), item)
        return output


    def ChecklMetaclass(self,obj,filter_classname):
        if MetatypeList(obj.title_or_id())[0]:
            classname=MetatypeList(obj.title_or_id())[0].title_or_id()
            if not isinstance(classname, unicode):
                classname = unicode(classname, 'utf-8', 'replace')
            if classname==filter_classname:
                return 1
            else:
                return 0
        

    def CheckOProp(self,obj,op,filter_opname):
        if not isinstance(op, unicode):
            classname = unicode(op, 'utf-8', 'replace')
        if not isinstance(filter_opname, unicode):
            filter_opname = unicode(filter_opname, 'utf-8', 'replace')
        if classname ==filter_opname:
            return 1
        else:
            return 0

    def CheckRule(self):
        rule_by_type={}

    def ListClassOfMetaclass(self,kw):
        obj=kw['obj']
        output=[]

        if obj and obj.hasMetatype:
            ops = [c.to_object for c in obj.hasMetatype]
            for op in ops:
                output=insert_outmeta(output, 'clsofmeta:'+op.title_or_id(), op)
        return output


    def ItemByUID(self):
        obj=''
        oid=''
        if 'uid' in self.request.keys():
            oid=self.request['uid']
            obj=ObjByUID(oid)
        return obj
    def list_ontologys(self):
        return listontologys()

    def ListChildOfMetaclass(self,kw):
        obj=kw['obj']
        output=[]
        out=back_references(obj, 'hasMetatype')
        for item in out:
            output=insert_outmeta(output, 'submetaclass:'+item.title_or_id(), item)
        return output
