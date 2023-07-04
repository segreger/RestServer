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

class TempOClass(object):
	def __init__(self,title, uid, url, portal_type):
		self.title=title
		self.absolute_url=uid
		self.portal_type=portal_type
		self._absolute_url=url
	def UID(self):
		return self.uid
	def title_or_id(self):
		return self.title
	def portal_type(self):
		return self.portal_type
	def absolute_url(self):
		return self._absolute_url

class TempOProp(object):
	def __init__(self,title, range, uid, url, portal_type):
		self.title=title
		self.uid=uid
		self.range=range
		self._absolute_url=url
		self.portal_type=portal_type
	def UID(self):
		return self.uid
	def title_or_id(self):
		return self.title
	def portal_type(self):
		return self.portal_type
	def absolute_url(self):
		return self._absolute_url

class Visiter(object):
	zope.interface.implements(IVisiter)
	def __init__(self,obj):
		self.obj=obj
		self.output=[]






