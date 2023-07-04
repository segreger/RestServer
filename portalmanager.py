# -*- coding: utf-8 -*-
from .get_data import*
class PortalManager:
    """
    сервис управления графами на сервере Plone
    """
    def __init__(self,agent):
        self.agent=agent
    def add_subclass(self, classname, ontoname, title, desc):
        """
	    создает подкласс класса с uid=context_uid в онтологии с uid=container_uid

        Args:
            agent (JsonData): агент доступа к серверу
            context_uid (str): uid родительского класса
            container_uid (str):uid онтологии, где создается подкласс
            title (str): имя подкласса
            desc (str): описание подкласса
        """

        data=get_source(self.agent,classname)
        context_uid=data['baseclass']['uid']
        container=self.agent.get_ontoitem('DextOntology',ontoname)
        container_uid=container['uid']
        indata={'selonto':container_uid,'context_uid':context_uid,'title':title,'desc':desc,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
        self.agent.create_subclass(indata)
        change_class_property1(agent,'DextOntoClass', title , 'hasMetatype', classname)
