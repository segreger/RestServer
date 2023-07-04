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

class DextOIndVisiter(Visiter):
    zope.interface.implements(IVisiter)
    def __init__(self,obj):
        self.obj=obj
        self.output=[]
    def children(self):
        if self.ListChidren():
            out=self.ListChidren()
        else:
            out= []
        return out

    def ListChidren(self):
        if self.obj.getObjectProps():
            for op in self.obj.getObjectProps():self.output=insert_out(self.output, op)
        if self.obj.getDataProps():
            for dp in self.obj.getDataProps():self.output=insert_out(self.output, dp)
        return self.output

class DextIndOPropVisiter(Visiter):
    zope.interface.implements(IVisiter)
    def __init__(self,visiter):
        self.obj=visiter.obj
        self.output=visiter.output
    def children(self):
        if self.obj.getRange():
            out=self.obj.getRange()
        else:
            out= [empty_obj()]
        for op in out:
            self.output=insert_out(self.output, op)
        return self.output

class DextIndDPropVisiter(Visiter):
    zope.interface.implements(IVisiter)
    def __init__(self,visiter):
        self.obj=visiter.obj
        self.output=visiter.output
    def children(self):
        if self.obj.getRange():
            out=[self.obj.getRange()]
        else:
            out= [empty_obj()]
        for op in out:
            self.output=insert_value(self.output, self.obj.getValue(), self.obj)
        return self.output