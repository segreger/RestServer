# -*- coding: utf-8 -*-
from zope.interface import Interface, implements
import zope.i18nmessageid
from zope import interface, schema
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from plone.supermodel import model
from onto.ontotypes.interfaces import dexMessage as _
from .dext_utility import *
from plone.dexterity.content import Container
from zope.schema.fieldproperty import FieldProperty
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.vocabularies.catalog import CatalogSource
from plone.formwidget.contenttree import ObjPathSourceBinder
class IBaseProperty(model.Schema):
    '''
    '''
    range = RelationList( 
            title=_(u"Range"), 
            description=_(u"Range"), 
            value_type=RelationChoice(
                title=u'Range',
                source=CatalogSource(),
                ),
            required=False, 
        ) 
   

class IProperty(IBaseProperty):
    '''
    '''
    domain = RelationList( 
            title=_(u"Domain"), 
            description=_(u"Domain"), 
            value_type=RelationChoice(
                title=u'Domain',
                source=CatalogSource(),
                ),
            required=False, 
        )

class IDextClassObjectProperty(model.Schema):
    '''
    '''
    title = schema.TextLine(
            title=_(u"Имя свойства"),
        )
    nameproperty = RelationList( 
            title=_(u"Родительская связь"), 
            description=_(u"Parent DextObjectProperty"), 
            value_type=RelationChoice(
                source=CatalogSource(),
                ),
            required=False, 
        )
    widget(
        'range',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Folder','DextOntology','DextOntoClass']
        }
    )
    range = RelationList( 
            title=_(u"Связь с классом"), 
            description=_(u"Range"), 
            value_type=RelationChoice(
                source=CatalogSource(),
                ),
            required=False, 
        ) 

class IDextDataProperty(IProperty):
    '''

    '''

class IDextObjectProperty(IProperty):
    '''

    ''' 

class IDextSubProperty(IProperty):
    '''
    '''

 

class IDextClassDataProperty(model.Schema):
    '''
    '''
    title = schema.TextLine(
            title=_(u"Имя связи"),
        )    
    nameproperty = RelationList( 
            title=_(u"Parent DextDataProperty"), 
            description=_(u"Parent DextDataProperty"), 
            value_type=RelationChoice(
                source=CatalogSource(),
                ),
            required=False, 
        ) 

    range = RelationList( 
            title=_(u"Range"), 
            description=_(u"Range"), 
            value_type=RelationChoice(
                source=CatalogSource(),
                ),
            required=False, 
        )
    value = schema.TextLine(
            title=_(u"Value"),
        )

class DextClassObjectProperty(Container):
    implements(IDextClassObjectProperty)
    title = FieldProperty(IDextClassDataProperty['title'])
    #sub_dataproperty_of = FieldProperty(IDextIndDataProperty['sub_dataproperty_of'])
    nameproperty = FieldProperty(IDextClassDataProperty['nameproperty'])
    range = FieldProperty(IDextClassDataProperty['range'])

    def __init__(self,title='',nameproperty=None, range=None):
        self.title=title
        self.nameproperty = nameproperty
        #self.sub_datapropty_of = sub_dataproperty_of
        self.range = range
    def setObjectProperty(self, range):
        range_cls= ObjByUID(range)
        updaterange(self,[range_cls],'range')


        

class DextClassDataProperty(object):
    implements(IDextClassDataProperty)
    title = FieldProperty(IDextClassDataProperty['title'])
    #sub_dataproperty_of = FieldProperty(IDextIndDataProperty['sub_dataproperty_of'])
    nameproperty = FieldProperty(IDextClassDataProperty['nameproperty'])
    range = FieldProperty(IDextClassDataProperty['range'])
    value = FieldProperty(IDextClassDataProperty['value'])

    def __init__(self,title='',nameproperty=None, range=None, value=None):
        self.title=title
        self.nameproperty = nameproperty
        #self.sub_datapropty_of = sub_dataproperty_of
        self.range = range
        self.value = value



		
class IDextIndDataProperty(IDextClassDataProperty):
    '''
    '''
    value = schema.TextLine(
            title=_(u"Name abstract element"),
        )



class IDextIndObjectProperty(model.Schema):
    '''
    '''
    nameproperty = RelationList( 
            title=_(u"Parent DextObjectProperty"), 
            description=_(u"Parent DextObjectProperty"), 
            value_type=RelationChoice(
                source=CatalogSource(),
                ),
            required=False, 
        )
    range = RelationList( 
            title=_(u"Range"), 
            description=_(u"Range"), 
            value_type=RelationChoice(
                source=CatalogSource(),
                ),
            required=False, 
        )
    



class DextIndObjectProperty(object):
    implements(IDextIndObjectProperty)
    #title = FieldProperty(IDextIndObjectProperty['title'])
    #domain = FieldProperty(IDextIndObjectProperty['domain'])
    #sub_objectpropty_of = FieldProperty(IDextIndObjectProperty['sub_objectproperty_of'])
    nameproperty = FieldProperty(IDextIndObjectProperty['nameproperty'])
    range = FieldProperty(IDextIndObjectProperty['range'])

    def __init__(self, nameproperty=None, orange=None):
        self.nameproperty = nameproperty
        self.orange = orange

        

class DextIndDataProperty(object):
    implements(IDextIndDataProperty)
    #title = FieldProperty(IDextIndDataProperty['title'])
    #sub_dataproperty_of = FieldProperty(IDextIndDataProperty['sub_dataproperty_of'])
    nameproperty = FieldProperty(IDextIndDataProperty['nameproperty'])
    range = FieldProperty(IDextIndDataProperty['range'])
    value = FieldProperty(IDextIndDataProperty['value'])

    def __init__(self, title=None, nameproperty_of=None, range=None, value=None):
        self.title=title
        self.nameproperty = nameproperty
        #self.sub_datapropty_of = sub_dataproperty_of
        self.range = range
        self.value = value
