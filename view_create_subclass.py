from RestApi.ontomodeler_lib import *
from service_utility import *
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_url='http://ontogovorun.ru/'
target_host=HostInfo(target_url,target_login, target_passw)
target_agent=JsonData(target_host)
target_mng=ModelManager(target_agent)
copy_agent=ModelCopyAgent(target_mng,target_mng)
"""
ontoname='Производство_агенты'
baseclass='Интерфейсный контроллер OntoEditor'
lst_agent=['Агент Просмотр задач']
#baseclass1='Служба'
"""
def setSubclass(ontoname,baseclass,copy__agent,lst_agent):
    """
    ontoname - имя онтологии, где создаются классы
    baseclass - имя родительского класса
    target_agent - создающий агент
    lst_agent - список имен создаваемых классов
    """
    context_uid=get_source(copy_agent.target_mng.host_agent,'DextOntoClass',baseclass)['baseclass']['uid']
    #context_uid1=get_source(agent,baseclass1)['baseclass']['uid']
    container=copy_agent.target_mng.host_agent.get_ontoitem('DextOntology',ontoname)
    container_uid=container['uid']
    #container_url=container['url']
    # Создаем классы Служба и Подразделение

    for title in lst_agent:
        indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
        copy_agent.target_mng.host_agent.create_subclass(indata)
        copy_agent.change_class_property(baseclass, 'hasMetatype', title)


