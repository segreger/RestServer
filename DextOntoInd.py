from zope.interface import Interface, implements
from plone.supermodel import model
from zope import schema
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.vocabularies.catalog import CatalogSource
#from plone.formwidget.contenttree import ObjPathSourceBinder
from onto.ontotypes.interfaces import dexMessage as _
from onto.ontotypes.DextOntoProperty import IDextIndDataProperty, IDextIndObjectProperty

class DPropListField(schema.List):
    "We need to have a unique class for the field list so that we can apply a custom adapter."
    pass


class OPropListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass


class IDextOntoInd(Interface):
    name = schema.TextLine(title=u'NameInd', required=True)
    id_ind = schema.TextLine(title=u'IdInd', required=True)
    sourceClass = schema.TextLine(title=u'sourceClass', required=True)
    dataproperty = DPropListField(title=u'IDexIndDataProperty',
        value_type=schema.Object(title=u'IDextIndDataProperty', schema=IDextIndDataProperty),
        required=True)
    objproperty = OPropListField(title=u'IDextIndObjectProperty',
        value_type=schema.Object(title=u'IDextIndObjectProperty', schema=IDextIndObjectProperty),
        required=True)

class IDextIndividual(model.Schema):
    sourceClass = RelationList(
        title=_(u"sourceClass"), 
        description=_(u"sourceClass"), 
        value_type=RelationChoice(
        source=CatalogSource(),
            ),
        required=False, 
        )
