# -*- coding: utf-8 -*-
from ontomodeler_lib import *
   
#source_url='http://localhost:8080/Plone/proekty/yadro-sistemy/'
#адрес папки для которой производится копирование. Адрес должен заканчиваться символом '/'
#source_url='http://localhost:8080/Plone/proekty/sistema-upravleniya-znaniyami/'
#source_url='http://localhost:8080/Plone/proekty/redaktor-ontologii-ontoeditor'
#source_url='http://localhost:8080/Plone/proekty/sistema-proektirovaniya-gui'
#source_url='http://localhost:8080/Plone/proekty/proekt-reshatelya-zadachi'
#адрес папки, в которую помещаюся копии. Папка должна существовать и ее адрес должен оканчиваться символом '/'
#target_url='http://ontogovorun.ru:8090/Plone/ontomodeler/yadro-sistemy/'
#target_url='http://ontogovorun.ru:8090/Plone/ontomodeler/sistema-upravleniya-znaniyami/'
#target_url='http://ontogovorun.ru:8090/Plone/ontomodeler/redaktor-ontologii-ontoeditor'
#target_url='http://ontogovorun.ru:8090/Plone/ontomodeler/sistema-proektirovaniya-gui'
#target_url='http://ontogovorun.ru:8090/Plone/ontomodeler/proekt-reshatelya-zadachi'
source_login='admin'
source_passw='admin'
target_login='admin'
target_passw='ykgI2Krwt1Uz'
"""
('http://localhost:8080/Plone/proekty/informacionnyi-fond/','http://ontogovorun.ru:8090/Plone/ontomodeler/informacionnyi-fond'),
     ('http://localhost:8080/Plone/proekty/sistema-upravleniya-proektami','http://ontogovorun.ru:8090/Plone/ontomodeler/sistema-upravleniya-proektami'),
     ('http://localhost:8080/Plone/proekty/portal-upravleniya-uchebnym-processom','http://ontogovorun.ru:8090/Plone/ontomodeler/portal-upravleniya-uchebnym-processom')
('http://localhost:8080/Plone/proekty/sistema-upravleniya-proektami/','http://ontogovorun.ru:8090/Plone/ontomodeler/sistema-upravleniya-proektami/')
('http://localhost:8080/Plone/proekty/portal-upravleniya-uchebnym-processom/','http://ontogovorun.ru:8090/Plone/ontomodeler/portal-upravleniya-uchebnym-processom/')
('http://localhost:8080/Plone/proekty/informacionnyi-fond/','http://ontogovorun.ru:8090/Plone/ontomodeler/informacionnyi-fond/'),
"""


url=[('http://localhost:8080/Plone/proekty/yadro-sistemy/','http://ontogovorun.ru:8090/Plone/ontomodeler/yadro-sistemy/'),
     ('http://localhost:8080/Plone/proekty/redaktor-ontologii-ontoeditor/','http://ontogovorun.ru:8090/Plone/ontomodeler/redaktor-ontologii-ontoeditor/'),
     ('http://localhost:8080/Plone/proekty/sistema-upravleniya-znaniyami/','http://ontogovorun.ru:8090/Plone/ontomodeler/sistema-upravleniya-znaniyami/'),
     ('http://localhost:8080/Plone/proekty/sistema-proektirovaniya-gui/','http://ontogovorun.ru:8090/Plone/ontomodeler/sistema-proektirovaniya-gui/'),
     ('http://localhost:8080/Plone/proekty/proekt-reshatelya-zadachi/','http://ontogovorun.ru:8090/Plone/ontomodeler/proekt-reshatelya-zadachi/'),
     ('http://localhost:8080/Plone/proekty/oo-hranilische/','http://ontogovorun.ru:8090/Plone/ontomodeler/oo-hranilische/'),
     ('http://localhost:8080/Plone/proekty/virtualnaya-sreda/','http://ontogovorun.ru:8090/Plone/ontomodeler/virtualnaya-sreda/'),
     ('http://localhost:8080/Plone/proekty/informacionnyi-fond/','http://ontogovorun.ru:8090/Plone/ontomodeler/informacionnyi-fond/'),
    ]

url1=[('http://localhost:8080/Plone/proekty/proekt-proizvodstvo/','http://ontogovorun.ru:8090/Plone/proekt/'),]
url2=[('http://localhost:8080/Plone/proekty/proekt-reshatelya-zadachi/','http://ontogovorun.ru:8090/Plone/ontomodeler/proekt-reshatelya-zadachi/')]
url3=[('http://localhost:8080/Plone/proekty/redaktor-ontologii-ontoeditor/','http://ontogovorun.ru:8090/Plone/ontomodeler/redaktor-ontologii-ontoeditor/'),]

"""    
for source_url,target_url in url1:
    source_host=HostInfo(source_url,source_login, source_passw)
    source_agent=JsonData(source_host)
    target_host=HostInfo(target_url,target_login, target_passw)
    target_agent=JsonData(target_host)
    source_mng=ModelManager(source_agent)
    target_mng=ModelManager(target_agent)
    copy_agent=ModelCopyAgent(source_mng,target_mng)
    
    #copy_agent.list_ontology_copy() #Создаем копии онтологий

    # 2 этап создаем копии классов
    #source_mng.get_listonology()
    #lst_onto=source_mng.lst_onto
    
    #copy_agent.list_class_copy(source_mng.lst_onto) #создаем копии классов
    #3 этап создаем связи
    #удаление связей
    #copy_agent.prop_for_target(lst_onto)
    #установка ссылок
    #copy_agent.range_for_target(lst_onto)
    #copy_agent.delete_props('Соответствие_Педагог_список объектов')
"""

target_url='http://ontogovorun.ru/proekt/'
target_host=HostInfo(target_url,target_login, target_passw)
target_agent=JsonData(target_host)
target_mng=ModelManager(target_agent)
"""
ontoname='Производство_агенты'
baseclass='Интерфейсный контроллер OntoEditor'
#baseclass1='Служба'
context_uid=get_source(target_agent,'DextOntoClass',baseclass)['baseclass']['uid']
#context_uid1=get_source(agent,baseclass1)['baseclass']['uid']
container=target_agent.get_ontoitem('DextOntology',ontoname)
container_uid=container['uid']
#container_url=container['url']
# Создаем классы Служба и Подразделение
lst_agent=['Агент Редактировать должность']
for title in lst_agent:
    indata={'inst_type':'DextOntoClass','selonto':container_uid,'context_uid':context_uid,'title':title,'desc':title,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
    target_agent.create_subclass(indata)
    change_class_property1(target_agent,'DextOntoClass', title , 'hasMetatype', baseclass)
        
# ******* устанавливаем свойства классов ****
#server_class_dict=get_folder_content(container_url)
#set_relation(agent,g,server_class_dict, 'подчиненность')
#set_relation_value(agent,g,server_class_dict, 'идентификатор')
"""
ontoname='Библиотека сотрудников'
target_onto=target_mng.host_agent.get_class_by_name('DextOntology',ontoname)
print(target_onto)
"""
if target_onto:
    lst_title=[i.title for i in res_source.children.values()]
    for title in lst_title:
        target_cls=target_mng.host_agent.get_class_by_name('DextOntoClass', title)
        if target_cls:
            print(title)
"""
#container=target_agent.get_ontoitem('DextOntology',ontoname)

#change_class_property(agent,portal_type, classname, property_name, target_name):
def n():
    """
	меняет свойство системное свойство объекта:SubClassOf, hasMetatype, range и т.п
	класс для range свойства создается
	portal_type - строка имени контент типа
	classname - строка имя элемента, у которого меняется свойство
	property_name - имя свойства
	target_id - uid элемента, на которое ссылается свойство

	"""