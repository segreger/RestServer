# -*- coding: utf-8 -*-
import zope.i18nmessageid
from zope import interface, schema
from zope.interface import Interface, implements
#from five import grok
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from zope.schema.fieldproperty import FieldProperty
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from plone.app.vocabularies.catalog import CatalogSource
#from DextOntoInd import *
from DextOntoProperty import *
from onto.ontotypes.interfaces import dexMessage as _ 
from plone.dexterity.content import Container


class IDextOntoClass(Interface):
    rootclass=schema.Bool(
        title=u'root class',
        required=False,
        )
    subClassOf = RelationList(
    	title=_(u"subClassOf"), 
        description=_(u"subClassOf"), 
        value_type=RelationChoice(
            title=u'subClassOf',
            source=CatalogSource(),
            ),
        required=False, 
        )
    hasKindOf = RelationList( 
        title=_(u"hasKindOf"), 
        description=_(u"hasKindOf"), 
        value_type=RelationChoice(
            title=u'hasKindOf',
            source=CatalogSource(),
            ),
        required=False, 
        )
    hasMetatype = RelationList( 
        title=_(u"hasMetatype"), 
        description=_(u"hasMetatype"), 
        value_type=RelationChoice(
            title=u'hasMetatype',
            source=CatalogSource(),
            ),
        required=False, 
        )

class DextOntoClass(Container):
    implements(IDextOntoClass)
    def getPath(self):
        print('path')




class ITextRowDextOntoClass(Interface):
    nameclass=schema.TextLine(
            title=_(u"nameclass"),
        )
    rootclass=schema.TextLine(
            title=_(u"rootclass"),
        )
    subClassOf = schema.TextLine(
            title=_(u"subClassOf"),
        )
    
    hasKindOf = schema.TextLine(
            title=_(u"hasKindOf"),
        )
    hasMetatype = schema.TextLine(
            title=_(u"hasMetatype"),
        )
    """
    subClassOfUID = schema.TextLine(
            title=_(u"subClassOfUID"),
        )
    hasKindOfUID = schema.TextLine(
                title=_(u"hasKindOfUID"),
            )    

    hasMetatypeUID = schema.TextLine(
            title=_(u"hasMetatypeUID"),
        )
    """
    #rootclass =schema.Bool(
    #        title=_(u"label_globally_enabled",  default=u"Globally enable comments"),
    #        description=_(u"help_globally_enabled",  default=u"If selected "),
    #        required=False,
    #        default=False,
    #    ),

class TextRowDextOntoClass():
    implements(ITextRowDextOntoClass)
    nameclass = FieldProperty(ITextRowDextOntoClass['nameclass'])
    rootclass = FieldProperty(ITextRowDextOntoClass['rootclass'])
    subClassOf = FieldProperty(ITextRowDextOntoClass['subClassOf'])
    hasKindOf = FieldProperty(ITextRowDextOntoClass['hasKindOf'])
    hasMetatype = FieldProperty(ITextRowDextOntoClass['hasMetatype'])
    """
    subClassOfUID = FieldProperty(ITextRowDextOntoClass['subClassOfUID'])
    hasKindOfUID = FieldProperty(ITextRowDextOntoClass['hasKindOfUID'])
    hasMetatypeUID = FieldProperty(ITextRowDextOntoClass['hasMetatypeUID'])
    """
    def __init__(self, nameclass=None,subClassOf=None, hasKindOf=None, hasMetatype=None,subClassOfUID=None, hasKindOfUID=None, hasMetatypeUID=None,rootclass=None):
        self.nameclass=nameclass
        self.subClassOf = subClassOf
        self.hasKindOf = hasKindOf
        self.hasMetatype = hasMetatype
        """
        self.subClassOfUID = subClassOfUID
        self.hasKindOfUID = hasKindOfUID
        self.hasMetatypeUID = hasMetatypeUID
        """
        self.rootclass=rootclass
        


class DClassListField(schema.List):
    "We need to have a unique class for the field list so that we can apply a custom adapter."
    pass



class IListDextOntoClass(Interface):
    classes= DClassListField(title=u'List of classes',
        value_type=schema.Object(title=u'DextOntoClass', schema=ITextRowDextOntoClass),
        required=True)

class RowClassDClassListField(schema.List):
    "We need to have a unique class for the field list so that we can apply a custom adapter."
    pass
class IListRowDextOntoClass(Interface):
    classes= DClassListField(title=u'List of classes',
        value_type=schema.Object(title=u'DextOntoClass', schema=ITextRowDextOntoClass),
        required=False)