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

class DextOntologyVisiter(Visiter):
    zope.interface.implements(IVisiter)	
    def __init__(self,obj):
        self.obj=obj
        self.output=[]
    
    def children(self):
        root=[]
        #сделан генератор getOntoObjects
        for o in getDextItemByPath(self.obj,"DextOntoClass"):
            if o.portal_type=='DextOntoClass' and o.rootclass:
                root.append(TempOClass(o.title_or_id(),o.UID(),o.absolute_url(), o.portal_type))
        if root:
            for item in root:
                self.output=insert_out(self.output, item)
        return self.output