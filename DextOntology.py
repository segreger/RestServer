from zope.interface import Interface, implements
from zope import schema
from onto.ontotypes.interfaces import dexMessage as _ 
from plone.dexterity.content import Container
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.vocabularies.catalog import CatalogSource
import json


class IDextOntology(Interface):
    root = RelationList(
        title=_(u"root class"), 
        description=_(u"root class"), 
        value_type=RelationChoice(
            title=u'root class',
            source=CatalogSource(),
            ),
        required=False, 
        )
class DOntologyListField(schema.List):
    ""
    pass    
class IListDextOntology(Interface):
    ontos= DOntologyListField(title=u'List of classes',
        value_type=schema.Object(title=u'DextOntology', schema=IDextOntology),
        required=True)

class DextOntology(Container):
    implements(IDextOntology)
    def getPath(self):
        print('path')



