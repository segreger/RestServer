
'''
задать подкласс класса Команда 
создать класс команды

создать "Обращение к агенту_ "  подкласс Обращение к агенту из Онтологии решателя задач
установить отношение hasMetaclass вызов set_metaclass(target_agent,ontoname,nameclass)
свойство "вызов агента" установить в "Обращение к агенту_ "

Обращение к агенту
    агент -> Агент subClass Интерфейсный контроллер OntoEditor subClass Агент OntoEditor  subclassOf Агент
                краткое имя : StringType
    параметры 
        Параметры вызова агента

    парааметры -> Параметры вызова агента
                        UID_папаметры -> UID_collection
                                                        context_uid
                                                        container_uid
                        Value_параметры -> Value_коллекция
                                                            mode
                                                            inst_type


'''
############################## Создание команды
"""
source_classname='Подразделение_команда'
target_classname='новое подразделение'
copy_agent.equal_class(source_classname,target_classname)
"""

############################### Создание Обращения к агенту

"""
source_classname='Обращение к агенту'
target_classname='Обращение к агенту Новое подразделение'
copy_agent.equal_class(source_classname,target_classname)
"""
############################### Cоздание цепочки наследования с проверкой и создание свойств
"""
source_classname='Агент'
target_classname='Агент OntoEditor'
copy_agent.equal_class(source_classname,target_classname)

source_classname='Агент OntoEditor'
target_classname='Интерфейсный контроллер OntoEditor'

copy_agent.equal_class(source_classname,target_classname)
"""

# создаем класс команды как подкласс и устанавливаем связь класс-подкласс
"""
ontoname='Производство_Онтология задач'
baseclass='Производство_команда'
lst_agent=['Структура подразделений']
setSubclass(ontoname,baseclass,target_agent,lst_agent)
"""
# 
"""
ontoname='Производство_Обращение к агенту'
baseclass='Обращение к агенту'
lst_agent=['Обращение к агенту Структура подразделений']
setSubclass(ontoname,baseclass,target_agent,lst_agent)
"""
#Создаем класс Агент Структура подразделений как подкласс и устанавливаем связь класс-подкласс
"""
ontoname='Производство_агенты '
baseclass='Интерфейсный контроллер OntoEditor'
lst_agent=['Агент Структура подразделений']
setSubclass(ontoname,baseclass,target_agent,lst_agent)
"""

# устанавливаем связь 'Структура подразделений.вызов агента =Обращение к агенту Структура подразделений'
"""
copy_agent.set_prop_range('Структура подразделений','Обращение к агенту Структура подразделений', 'вызов агента')
"""

"""
# устанавливаем связь 'Обращение к агенту Структура подразделений.агент = Агент Структура подразделений'
copy_agent.set_prop_range('Обращение к агенту Структура подразделений', 'Агент Структура подразделений','агент')
"""
"""
setSubclass('Производство_Обращение к агенту','Параметры вызова агента',target_agent,['Параметры вызова агента Структура подразделений' ])
setSubclass('Производство_Обращение к агенту','UID_collection',target_agent,['UID_collection вызова агента Структура подразделений' ])
setSubclass('Производство_Обращение к агенту','Value_коллекция',target_agent,['Value_коллекция вызова агента Структура подразделений' ])
copy_agent.set_prop_range('Обращение к агенту Структура подразделений', 'Параметры вызова агента Структура подразделений','параметры')
"""
#copy_agent.set_prop_range('Параметры вызова агента Структура подразделений', 'UID_collection вызова агента Структура подразделений','UID_параметры')
#copy_agent.set_prop_range('Параметры вызова агента Структура подразделений', 'Value_коллекция вызова агента Структура подразделений','Value_параметры')

##################### Должность ##################################
"""
ontoname='Производство_Онтология задач'
baseclass='Должность_команда'
lst_agent=['Должностная структура']
setSubclass(ontoname,baseclass,target_agent,lst_agent)
"""
############################### Создание Обращения к агенту
"""

source_classname='Обращение к агенту'
target_classname='Обращение к агенту Должностная структура'
copy_agent.equal_class(source_classname,target_classname)
setSubclass(ontoname,baseclass,target_agent,lst_agent)



"""
#Создаем класс Агент Должностная структура как подкласс и устанавливаем связь класс-подкласс
"""
ontoname='Производство_агенты '
baseclass='Интерфейсный контроллер OntoEditor'
lst_agent=['Агент Должностная структура']
setSubclass(ontoname,baseclass,target_agent,lst_agent)
"""

# устанавливаем связь 'Должностная структура.вызов агента =Обращение к агенту Должностная структура'
"""
copy_agent.set_prop_range('Должностная структура','Обращение к агенту Должностная структура', 'вызов агента')

# устанавливаем связь 'Обращение к агенту Должностная структура.агент = Агент Структура подразделений'
copy_agent.set_prop_range('Обращение к агенту Должностная структура', 'Агент Должностная структура','агент')

setSubclass('Производство_Обращение к агенту','Параметры вызова агента',target_agent,['Параметры вызова агента Должностная структура' ])
setSubclass('Производство_Обращение к агенту','UID_collection',target_agent,['UID_collection вызова агента Должностная структура' ])
setSubclass('Производство_Обращение к агенту','Value_коллекция',target_agent,['Value_коллекция вызова агента Должностная структура' ])
copy_agent.set_prop_range('Обращение к агенту Должностная структура', 'Параметры вызова агента Должностная структура','параметры')

copy_agent.set_prop_range('Параметры вызова агента Должностная структура', 'UID_collection вызова агента Должностная структура','UID_параметры')
copy_agent.set_prop_range('Параметры вызова агента Структура подразделений', 'Value_коллекция вызова агента Должностная структура','Value_параметры')
"""

