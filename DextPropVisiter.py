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


class DextOPropVisiter(Visiter):
    zope.interface.implements(IVisiter)
    def __init__(self,obj):
        self.obj=obj
        self.output=[]
        
    def children(self):
        output=[]
        back=backref(self.obj, filter='ClassObjectProperty')
        if back:
            for op in back:output=insert_out(output, op)
        else:
            output=insert_out(output, self.empty_class)
        return output


class DextClassOPropVisiter(Visiter):
    zope.interface.implements(IVisiter)
    def __init__(self,obj):
        self.obj=obj
        self.output=[]
        self.inf_unit=DextClassObjectPropertyWU('',self.obj.UID())
        self.wunit=self.inf_unit.getWUnit()
    def children(self):
        #out=self.inf_unit.getRelationRange()
        out=self.wunit.getRelationRange()
        for op in out:
            if op:
                #self.output=insert_out(self.output, op)
                self.output=insert_outmeta(self.output, 'rangeclass:'+op.title_or_id(), op)
            else:
                cl=dext_empty_class()
                self.output=insert_outmeta(self.output, 'rangeclass:'+cl.title_or_id(), cl)
        return self.output

class DextClassDPropVisiter(Visiter):
    zope.interface.implements(IVisiter)
    def __init__(self,obj):
        self.obj=obj
        self.output=[]
        self.inf_unit=DextClassDataPropertyWU('',self.obj.UID())
        self.wunit=self.inf_unit.getWUnit()
    def children(self):
        out=self.inf_unit
        prop_name=out.prop_name
        if out.value:
            value=out.value
        else:
            value=' '
        self.output=insert_outmeta(self.output, value, self.obj)
        return self.output
    def DefNameAndValue(self,kw):
        output=insert_outmeta(output, self.obj.title_or_id()+'='+wunit['value'], out)
        return output


