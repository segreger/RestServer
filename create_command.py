from RestApi.ontomodeler_lib import *
from service_utility import *
from config_server import *
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_url='http://ontogovorun.ru/'
target_host=HostInfo(target_url,target_login, target_passw)
target_agent=JsonData(target_host)
target_mng=ModelManager(target_agent)
copy_agent=ModelCopyAgent(target_mng,target_mng)

############################## Создание команды

# создаем класс команды как подкласс и устанавливаем связь класс-подкласс
'''
ontoname='Производство_Онтология задач'
baseclass='Задача_команда'
lst_agent=['Создать подзадачу']
setSubclass(ontoname,baseclass,copy_agent,lst_agent)

'''


################################ Создание Обращения к агенту
'''
ontoname='Производство_Обращение к агенту'
baseclass='Обращение к агенту'
lst_agent=['Обращение к агенту Создать подзадачу']
#copy_agent.equal_class(source_classname,target_classname)
setSubclass(ontoname,baseclass,copy_agent,lst_agent)
'''



#Создаем класс Агент Должностная структура как подкласс и устанавливаем связь класс-подкласс
'''
ontoname='Производство_агенты '
baseclass='Интерфейсный контроллер OntoEditor'
lst_agent=['Агент Создать подзадачу']
setSubclass(ontoname,baseclass,copy_agent,lst_agent)

'''
# устанавливаем связь 'Должностная структура.вызов агента =Обращение к агенту Должностная структура'

#copy_agent.set_prop_range('Создать подзадачу','Обращение к агенту Создать подзадачу', 'вызов агента')

# устанавливаем связь 'Обращение к агенту Должностная структура.агент = Агент Структура подразделений'
#copy_agent.set_prop_range('Обращение к агенту Создать подзадачу', 'Агент Создать подзадачу','агент')
"""
setSubclass('Производство_Обращение к агенту','Параметры вызова агента',copy_agent,['Параметры вызова агента Создать подзадачу' ])
setSubclass('Производство_Обращение к агенту','UID_collection',copy_agent,['UID_collection вызова агента Создать подзадачу' ])
setSubclass('Производство_Обращение к агенту','Value_коллекция',copy_agent,['Value_коллекция вызова агента Создать подзадачу' ])
copy_agent.set_prop_range('Обращение к агенту Создать подзадачу', 'Параметры вызова агента Создать подзадачу','параметры')

copy_agent.set_prop_range('Параметры вызова агента Создать подзадачу', 'UID_collection вызова агента Создать подзадачу','UID_параметры')
copy_agent.set_prop_range('Параметры вызова агента Структура подразделений', 'Value_коллекция вызова агента Создать подзадачу','Value_параметры')
"""
lst_model=[{'ontoname':'Производство_Онтология задач', 'baseclass':'KWCommand', 'lst_agent':['Показатели']},
           {'ontoname':'Производство_Обращение к агенту','baseclass':'Обращение к агенту', 'lst_agent':['Обращение к агенту Показатели']},
           {'ontoname':'Производство_агенты','baseclass':'Интерфейсный контроллер OntoEditor', 'lst_agent':['Агент Показатели']},

          ]
lst_model1=[{'ontoname':'Производство_Обращение к агенту', 'baseclass':'Параметры вызова агента', 'lst_agent':['Параметры вызова агента Показатели']},
           {'ontoname':'Производство_Обращение к агенту','baseclass':'UID_collection', 'lst_agent':['UID_collection вызова агента Показатели']},
           {'ontoname':'Производство_Обращение к агенту','baseclass':'Value_коллекция', 'lst_agent':['Value_коллекция вызова агента Показатели']},

          ]
"""
for m in lst_model1:
    ontoname=m['ontoname']
    baseclass=m['baseclass']
    lst_agent=m['lst_agent']
    setSubclass(ontoname,baseclass,copy_agent,lst_agent)
"""
lst_egd_model=[{'source_classname':'Показатели','target_classname':'Обращение к агенту Показатели', 'source_propname':'вызов агента'},
               {'source_classname':'Обращение к агенту Показатели','target_classname':'Агент Показатели', 'source_propname':'агент'},
               {'source_classname':'Обращение к агенту Показатели','target_classname':'Параметры вызова агента Показатели', 'source_propname':'параметры'},
               {'source_classname':'Параметры вызова агента Показатели','target_classname':'UID_collection вызова агента Показатели', 'source_propname':'UID_параметры'},
               {'source_classname':'Параметры вызова агента Показатели','target_classname':'Value_коллекция вызова агента Показатели', 'source_propname':'Value_параметры'},
               ]
for m in lst_egd_model:
    source_classname=m['source_classname']
    target_classname=m['target_classname']
    source_propname=m['source_propname']
    copy_agent.set_prop_range(source_classname,target_classname, source_propname)

