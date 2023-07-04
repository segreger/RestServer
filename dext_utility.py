# -*- coding: utf-8 -*-
import pdb
import json




#from onto.utility.base_utility import *
#***************Base uility**********************************************


''' 


def empty_obj():
    ecls=getObjectByName(u'пустой объект')
    return ecls


def empty_oprop():
    op=getOntoItemByName('empty_oprop','DextClassObjectProperty')
    return op
'''
def listontologys():
    '''

    '''
    catalogtool = getCatalogtool()
    res1=[i.getObject() for i in catalogtool.searchResults({'portal_type':'DextOntology'})]
    l1=[(i.title_or_id(),i.UID()) for i in res1 if res1]
    f=dict(l1)
    return f
def getNewId():
    import random
    """
    """
    # возвращает новый ид для добавления объекта
    str = 'abcdefghijklmnopqastuvwxyzABCDEFGHIJKLMNOPQSTUVWXYZ1234567890'
    nId = [ random.choice(str) for i in xrange(16) ]
    nId = "".join( nId )
    return nId

def get_fromdict(name, kw):
    if name in kw.keys() and kw[name]:
        return kw[name]
    else:
        return None

def get_fromreq(name, request):
    return get_fromdict(name, request)

def get_fromform(request,name):
    form=request.form
    return get_fromdict(name, form)

def response_json(request, onto_data):
    request.response.setHeader('content-type', 'application/json; charset=utf-8')
    response_body = onto_data
    response_http = json_call(response_body)
    request.response.setHeader('content-length', len(response_http))
    return response_http
def toUTF(oname):
    if not isinstance(oname, unicode) and oname:
      oname = unicode(oname, 'utf-8', 'replace')
    return oname
def json_call(onto_data):
    x=json.dumps(onto_data)
    return x

def json_resp(data, request):
    #request.response.setHeader('content-type', 'application/json; charset=utf-8')
    response_body = data
    response_http = json.dumps(response_body)
    request.response.setHeader('content-length', len(response_http))
    return response_http

def get_json(url):
    "возвращает словарь 'имя онтологии':'uid онтологии'"
    response = requests.get(url)
    return response.json()


"""
def CommandsForClass(kw):
    #pdb.set_trace()
    ref=kw['reflist']
    ouid=kw['ouid']
    request=kw['request']
    list_comm=[]
    onto_objs=[]
    cls=ObjByUID(ouid)
    if ref and onto_objs:
        onto_objs=cls.ontoCommand(ref,mode='listclass')
        onto_data={}
        for i in onto_objs:
            if isinstance(i, OntoClass):
                onto_data['command_name']=i.title_or_id()
                for j in ListDataProp(i.title_or_id()):
                    onto_data[j.title_or_id()]=j.getDefault_value()
                list_comm.append(onto_data)
                onto_data={}
        response_body = list_comm
        #response_http = json.dumps(response_body)
        #self.request.response.setHeader('content-length', len(response_http))
        #return response_http
    else:
        response_body = []
        #response_http = json.dumps(response_body)
        #self.request.response.setHeader('content-length', len(response_http))
        #return response_http
    json_resp(response_body, request)

"""




##############################################################
def getObjPropByParent(nameclass):
    """
    Возвращает словарь {title: list object for Range} всех ClassObjrctProperty для лерева классов
    """
    #pdb.set_trace()
    
    dict_meta={}
    dict_class={}
    dict_par={}
    dict_prop={}
    par_list=[]
    meta_list=[]
    context_class=[]
    cls=getClassByName(toUTF(nameclass))
    context_class.append(cls)
    dict_class=ListRangeItems(context_class)
    meta_list=MetatypeList(nameclass)
    if meta_list:
        dict_meta=ListRangeItems(meta_list)
     
    if ClassParentsList(nameclass):
        par_list=ClassParentsList(nameclass)
        dict_par=ListRangeItems(par_list)

    if context_class:
        dict_class=ListRangeItems(context_class)


    return DeleteParentProp1(dict_meta, dict_prop, dict_class)


def getDataPropByParent(nameclass):
    """
    Возвращает словарь {title: list object for Range} всех ClassDataProperty для лерева классов
    """
    dict_meta={}
    dict_class={}
    dict_par={}
    dict_prop={}
    par_list=[]
    meta_list=[]
    context_class=[]
    context_class.append(getClassByName(nameclass))
    dict_class=ListDRangeItems(context_class)
    meta_list=MetatypeList(nameclass)

    if meta_list:
        dict_meta=ListDRangeItems(meta_list)
    if ClassParentsList(nameclass):
        par_list=ClassParentsList(nameclass)
        dict_par=ListDRangeItems(par_list)

    return DeleteParentProp1(dict_meta, dict_prop, dict_class)

def DeleteParentProp1(meta_prop, dict_prop, class_prop):
    """
    заменяет объектное  и data свойство родителя свойством класса и расширяет словарь родителя словарем класса
    """
    if dict_prop:
        for k,v in dict_prop.items():
            meta_prop[k]=v
    if class_prop:
        for k,v in class_prop.items():
            meta_prop[k]=v 
    return meta_prop  

def DeleteParentProp(par_prop, class_prop):
    """
    заменяет объектное  и data свойство родителя свойством класса и расширяет словарь родителя словарем класса
    """
    for k,v in class_prop.items():
       par_prop[k]=v
    return par_prop
def ListRangeItems(par_list):
    op={}
    for i in par_list:
        if isinstance(i, OntoClass):
            for j in i.ListObjectProps():
                rangeitem=[]
                if j.getRange():
                    rangeitem=[(r.title_or_id(), r.absolute_url(), r.UID(), j.UID()) for r in j.getRange() if r]
                else:
                    rangeitem=[('', '', '', j.UID())]
                op[j.title_or_id()]=rangeitem
        if isinstance(i, OntoIndividual):
            for j in i.getObjectProps():
                rangeitem=[]
                if j.getRange():
                    rangeitem=[(r.title_or_id(), r.absolute_url(), r.UID(), j.UID()) for r in j.getRange() if r]
                else:
                    rangeitem=[('', '', '', j.UID())]
                op[j.title_or_id()]=rangeitem
    return op
def ListDRangeItems(par_list):
    op={}
    for i in par_list:
        if isinstance(i, OntoClass):
            for j in i.getDataProps():
                rangeitem=[]
                if j.getRange():
                    rangeitem=[(r.title_or_id(), r.absolute_url(), j.getId(), j.getDefault_value(), j.title_or_id(), j.UID()) for r in j.getRange()]
                else:
                    rangeitem=[('', '', j.getId(),j.getDefault_value(),j.title_or_id(),j.UID())]
                op[j.title_or_id()]=rangeitem

    return op


###########################################################################
# Функции, возвращающие списки элементов
#######################################################################
def ListDataProp(nameclass):
    ocls=getClassByName(nameclass)
    dp=''
    if ocls:
        dp=ocls.getDataProps()
    if dp:
        return dp
    else:
        return 0

def ParentsList(context):
    p_list=[]
    tec=context
    item=context
    lst=[]
    if isinstance(tec, OntoClass):
        p_list.append(context)    
        while tec.getSubClassOf():
            item=tec.getSubClassOf()[0]
            p_list.append(item)
            #p_list.extend(KindList(item))
            #p_list.extend(MetatypeList(item.title_or_id()))
            tec=item
        meta=MetatypeList(tec.title_or_id())
        p_list.extend(meta)
        lst=List_reverse(p_list)
    return lst


def List_reverse(lst):
    out=[]
    while lst:
        out.append(lst.pop())
    return out


    

def KindList(context):
    p_list=[]
    tec=context
    item=context
    if isinstance(tec, OntoClass): 
        while tec.getHasKindOf():
            item=tec.getHasKindOf()[0]
            p_list.append(item)
            tec=item
    return p_list

def MetatypeList(nameclass):
    p_list=[]
    tec=getClassByName(nameclass)
    item=tec
    if isinstance(tec, OntoClass) and tec.getHasMetatype():
        """
        while tec.getHasMetatype():
        """    
        item=tec.getHasMetatype()[0]
        p_list.append(item)
        tec=item

    return p_list

def ClassParentsList(nameclass):
    p_list=[]

    tec=getClassByName(nameclass)

    if isinstance(tec, OntoClass) and tec.getSubClassOf():
        """
        while tec and tec.getSubClassOf():
        """
        for item in tec.getSubClassOf():
            p_list.append(item)
            tec=item
    return p_list



def getOnto(ontoid):
    '''

    '''
    catalogtool=getCatalogtool()
    lobj=[i.getObject() for i in catalogtool.searchResults({'portal_type':"Ontology"})]
    if lobj:
        for item in lobj:
            if item.getId()==ontoid:
                return item
    return 0

def backref(context, filter=''):
    refCatalog = getRefcatalog()
    uid_catalog = getUidcatalog()
    par=context
    if isinstance(par, DextOntoClass) or isinstance(par, DextOntoIndividual):

        bref=refCatalog.getBackReferences(par)
        lobj=[ref.getSourceObject() for ref in bref]
        if filter=='DextOntoClass':
            return [ref for ref in lobj if isinstance(ref, DextOntoClass)]
        if filter=='DextClassObjectProperty':
            return [ref for ref in lobj if isinstance(ref, DextClassObjectProperty)]
        else:
            return lobj
    if isinstance(par, DextObjectProperty):
        bref=refCatalog.getBackReferences(par)
        lobj=[ref.getSourceObject() for ref in bref]
        if filter=='dextOntoClass':
            return [ref for ref in lobj if isinstance(ref, DextOntoClass)]
        if filter=='ClassObjectProperty':
            return [ref for ref in lobj if isinstance(ref, DextClassObjectProperty)]
        else:
            return lobj    
    else:
        return []


def getObjectForClass(context):
    return SubClassRef(context, 'ind')
def getSubClassesForClass(context):
    return SubClassRef(context, 'subclass')
def getSubTypesForClass(context):
    return SubClassRef(context, 'metaclass')    
def SubClassRef(context, name_ref):
    ref={'subclass':'sub_class_of', 'ind':'source_class','metaclass':"has_metatype"}
    out=[]
    refCatalog = getRefcatalog()
    uid_catalog = getUidcatalog()
    item=context
    references = refCatalog.getBackReferences(item.UID(), relationship=ref[name_ref])
    out =[ref.getSourceObject() for ref in references]
    if name_ref=='sub_class_of':
        out2=[ref for ref in out if isinstance(ref, DextOntoClass)]
        return out2
    else:
        return out

def MetaClassRef(classname, ontoid):
    out=[]
    cls=getClassByNamePath(classname, ontoid)
    refCatalog = getRefcatalog()
    if isinstance(cls, OntoClass):
        references = refCatalog.getBackReferences(cls.UID(), relationship="has_metatype")
        out = [ref.getSourceObject() for ref in references]
    return out

def MetaClassRefbyUID(class_uid):
    out=[]
    refCatalog = getRefcatalog()
    references = refCatalog.getBackReferences(class_uid, relationship="has_metatype")
    out = [ref.getSourceObject() for ref in references]
    return out

def getListRangeObject(ouid):
    inds=[]
    refCatalog = getRefcatalog()  
    uid_catalog = getUidcatalog()
    #список индивидуалов
    if ouid:
        itemUID=ouid
        list_rangeitem = [k.getObject() for k in uid_catalog(UID=itemUID)]
        if list_rangeitem:
            rangeitem=list_rangeitem[0]
            if rangeitem.getRange():
                crange=rangeitem.getRange()[0].UID()
                references = refCatalog.getBackReferences(crange, relationship="source_class")
                inds = [ref.getSourceObject() for ref in references]
                      
    return inds

def getListInd(ouid):
    #refCatalog = getRefcatalog()
    references = back_references(ObjByUID(ouid), "source_class")
    #refCatalog.getBackReferences(ouid, relationship="source_class")
    #inds = [ref.getSourceObject() for ref in references]
    #return inds
    return references

def ListFieldTypes(attr):
    """
    получает список классов, наследующих класс с именем @rootfield
    """
    #cls=getClassByName(attr['rootclass'])
    onto=getDextByNameAndPath(attr['ontolocation'], attr['folder_onto'],'DextOntology')
   
    if onto:
        onto_classes=DextOntologyWU(onto,'').getWUnit().wunit['classes']
        cls_obj=getDextByNameAndPath(attr['rootclass'], onto,'DextOntoClass')

        if cls_obj:
            ch_cls=back_references(cls_obj, 'subClassOf')

            return ch_cls
        else:
            return 0

def OPropByNameList(ouid,refname):
    """
    список Range класов у о.свойства
    """
    cls=ObjByUID(ouid)
    commands1=[]
    mainop=''
    if cls:
        op=getClassObjectPropertyByName(refname)
        if op:
            for o in op:
                if o.getRange():commands1.extend(o.getRange())
        else:
            return 0 
    return commands1

#######################################################################################
#  функции, возвращающие элементы
#######################################################################################

def getOntoRepos(obj_uid):
    obj=ObjByUID(obj_uid)
    return ParentFolder(obj)

def ParentFolder(obj):
    par_onto = aq_parent(obj)
    return par_onto
def getClassByNameInOnto(classname, onto_cls):
    '''

    '''
    catalogtool = getCatalogtool()
    res=catalogtool.searchResults({'portal_type':'OntoClass', 'Title':classname,'path':onto_cls.getPath()})
    obj_list = [i.getObject() for i in res]
    if len(obj_list)==1:
        return obj_list[0]
    else:
        return 0

def getClassByNamePath(classname, ontoid):
    '''

    '''
    onto_cls=getOnto(ontoid)
    catalogtool = getCatalogtool()
    res=catalogtool.searchResults({'portal_type':'OntoClass','path':onto_cls.getPath()})
    obj_list = dict([(unicode(i.getObject().title_or_id(), 'utf-8', 'replace'),i.getObject()) for i in res])
    if not isinstance(classname, unicode):
        classname = unicode(classname, 'utf-8', 'replace')
    if classname in obj_list.keys():
        return obj_list[classname]
    else:
        return 0





def ObjectAllPropList(ouid):

    """
    по UID индивидуала возвращает словарь:
    ключ  'DataProp' - список объектов IndDataProperty индивидуала
    ключ  'ObjectProp' - список объектов IndObjectProperty индивидуала
    """
    uid_catalog=getUidcatalog()
    #список индивидуалов
    if ouid:
        itemUID=ouid
        list_rangeitem = [k.getObject() for k in uid_catalog(UID=itemUID)]
        if list_rangeitem:
            rangeitem=list_rangeitem[0]
            OntoObjects1 = rangeitem.listFolderContents(contentFilter={'portal_type' : 'IndDataProperty'})
            OntoObjects2 = rangeitem.listFolderContents(contentFilter={'portal_type' : 'IndObjectProperty'})
            return {'DataProp':OntoObjects1,'ObjProp':OntoObjects2}
        else:
            return 0 
    else:
        return 0
def DataPropWithValue(nameobj):
    obj=getIndByName(nameobj)
    dplist=obj.getDataProps()
    dpdict={}
    for i in dplist:
        par_prop=i.getDataProperty()
        if par_prop:
            rng_type=par_prop.getRange()[0]
            rng_title=rng_type.title_or_id()
            rng_url=rng_type.absolute_url()
        else:
            rng_type='**'
            rng_title='**'
            rng_url='**'
        v= i['value']
        dpid=i.getId()
        ttl=i.title_or_id()
        dpdict[ttl]=(rng_title, rng_url, dpid, v, ttl, i.UID())
        #имя_свойства, [(имя объекта Range, url объекта Range, id свойства,Default_value свойства, имя_свойства, UID свойства)]

    return dpdict
def getDataPropWithValue(obj):
    dplist=obj.getDataProps()
    dpdict={}
    for i in dplist:
        par_prop=i.getDataProperty()
        if par_prop:
            rng_type=par_prop.getRange()[0]
            rng_title=rng_type.title_or_id()
            rng_url=rng_type.absolute_url()
        else:
            rng_type='**'
            rng_title='**'
            rng_url='**'
        v= i['value']
        dpid=i.getId()
        ttl=i.title_or_id()
        dpdict[ttl]=(rng_title, rng_url, dpid, v, ttl, i.UID())
        #имя_свойства, [(имя объекта Range, url объекта Range, id свойства,Default_value свойства, имя_свойства, UID свойства)]

    return dpdict

def CommmandsForClass(kw):
    reflist=kw['reflist']
    ouid=kw['ouid']
    if reflist:
        list_comm=[]
        onto_objs=[]
        cls=ObjByUID(ouid)
        if isinstance(cls, OntoClass):            
            onto_objs=cls.ontoCommand(reflist,mode='listclass')
        if not isinstance(cls, OntoClass):onto_objs=[]
        if onto_objs:
            onto_data={}
            list_prop=[]
            for i in onto_objs:
                if isinstance(i, OntoClass):
                    prop={}
                    prop['command_name']=i.title_or_id()
                    prop['absolute_url']=i.absolute_url()
                    for j in ListDataProp(i.title_or_id()):
                        prop[j.title_or_id()]=j.getDefault_value()
        return list_comm

def getFileBody(kw):
        id_file=kw['id_file']
        files = ObjByUID(id_file)
        #pdb.set_trace()
        data = files.get_data()
        rows=data.split('\n')
        list_rows=[]
        #group_name=unicode(context.title_or_id(),'utf-8')
        for row in rows:
            if row and ';' in row:
                words=row.split(';')
                obj={}
                obj['name']=words[0]
                obj['desc']=words[1]
                list_rows.append(obj)
            else:
                list_rows.append(row)
        return {'list_rows':list_rows}
def getParentPropertyList(ouid,filter=''):
    p_dict={}
    cob_list=[]
    cls_list=[]
    op_list=[]
    if 'nameproperty' in WorkUnit(ouid).getWUnit().keys() and WorkUnit(ouid).getWUnit()['nameproperty']:
        prop_obj=WorkUnit(ouid).getWUnit()['nameproperty']
    else:
        prop_obj=''
    if isinstance (prop_obj,list):
        for item in prop_obj:
            if isinstance (item,ClassObjectProperty):
                cob_list.append(item)
                ouid=item.UID()
            if isinstance (item,OntoClass):
                cls_list.append(item)
                ouid=''
            if isinstance (item,ObjectProperty):
                op_list.append(item)
                ouid=''
    if isinstance (prop_obj,ClassObjectProperty):
        cob_list.append(prop_obj)
    if isinstance (prop_obj,OntoClass):
        cls_list.append(prop_obj)
    if isinstance (prop_obj,ObjectProperty):
        return getParentPropertyList(prop_obj.UID(),filter='OntoClass')
    if filter=='OntoClass':
        return cls_list
    if filter=='ClassObjectPropery':
        return cob_list
    if filter=='ObjectPropery':
        return op_list 

def CreateSubDict(k,list_key):
    """
    приводит структуру словаря в соответствие с заданным списком ключей
    """
    subk={}
    """
    for k,v in k.items():
        if k in list_key:
            subk[k]=v
        else:
            subk[k]=''
    """
    for i in list_key:
        if i in k.keys():
            subk[i]=k[i]
        else:
            subk[i]=''
    return subk

class BaseView(object):
    def __init__(self, context,request):
        self.context = context
        self.request = request
        self.urltool = getToolByName(self, "portal_url")
        self.catalogtool = getToolByName(self, "portal_catalog")
        self.refcatalog = getToolByName(self, "reference_catalog")
        self.portal = self.urltool.getPortalObject()
        self.response = []
    def getWorkUnit(self,ext_context=''):
        if ext_context:
            #получает UID внещнего класса
            wunit=WorkUnit(ext_context, '').getWUnit()
            wunit.update({'mode':get_fromreq('mode', self.request)})
        else:
            wunit=self.wunit
        return wunit
    def getContextClass(self,context, request):
        return viewContextClass(context, request)
    def list_ontologys(self):
        lst=listontologys()
        return lst
    def list_types(self):
        #pdb.set_trace()
        total_parent_oprop=[]
        total_const=[]
        res=[]
        c=self.getContextClass(self.context, self.request)
        if isinstance(c, OntoClass) and c.getHasKindOf():
            lst=c.getHasKindOf()
            return self.ClsToDictSubCls(lst)
        if isinstance(c, ClassObjectProperty):
            parent_oprop=getParentPropertyList(c.UID(),filter='ObjectPropery')
            parent_clsoprop=getParentPropertyList(c.UID(),filter='ClassObjectPropery')
            total_parent_oprop.extend(parent_oprop)
            total_parent_oprop.extend(parent_clsoprop)
            if total_parent_oprop:
                for op in total_parent_oprop:
                    lst=getParentPropertyList(op.UID(),filter='OntoClass')
                    total_const.extend(lst)
                res.append({'op_uid':op.UID(),'kinddict':self.ClsToDictSubCls(total_const)})
                return res
            else:
                return [{'op_uid':'','kinddict':{'name':'Empty',"dictitems":{}, "select items":''}}]
        else:
            return {'name':'Empty',"dictitems":{}, "select items":''}
    def ClsToDictSubCls(self,lst):
        if lst and len(lst)>1:
            for k in lst:
                l=[(unicode(str(i.title_or_id()), 'utf-8'),self.ClassAsClassif(i)) for i in lst if lst]
            f=dict(l)
            return {'name':'ClassesWithSubClasses',"dictitems":f, "select items":''}
        if lst and len(lst)==1:
            obj=lst[0]
            if isinstance(obj,OntoClass):
                f=self.ClassAsClassif(obj)
                return {'name':'OneClassWithSubclasses',"dictitems":f, "select items":''}
            if isinstance(obj,OntoIndividual):
                parent_obj=obj.getSourceClass()[0]
                f=self.ClassAsClassif(parent_obj)
                return {'name':'OneClassWithObjects',"dictitems":f, "select items":obj.UID()}
        else:
            return {'name':'Empty',"dictitems":{}, "select items":''}
    def ClassAsClassif(self,obj):
        if isinstance(obj,OntoClass) and SubClassRef(obj, 'subclass'):
            item=obj
            lst1=SubClassRef(item, 'subclass')
            l=[i.UID() for i in lst1 if lst1]
            f={unicode(str(item.title_or_id()), 'utf-8'):l}
            return f
        if isinstance(obj,OntoClass) and not SubClassRef(obj, 'subclass'):
            item=obj
            lst1=SubClassRef(item, 'ind')
            l=[i.UID() for i in lst1 if lst1]
            f={unicode(str(item.title_or_id()), 'utf-8'):l}
            return f 
    def list_types_pack(self, item):
        lst1=SubClassRef(item, 'subclass')
        l=[(unicode(str(i.title_or_id()), 'utf-8'),i.UID()) for i in lst1 if lst1]
        l_dict=dict(l)
        return l_dict

    def TwoLevelCollection(self,base_item,base_item_agent,coll_item_agent):
        """
        base_item - объект, на основе которого строится коллекция
        base_item_agent - агент, создающий коллекцию на основе base_item 
        coll_item_agent -агент, применяемый к каждому элементу коллекции
        """
        pass




    def seeError(self,macro_module,data,tpl):
        print( "**************Template error***********************")
        #PrnVal('data',data)
        #PrnVal('macro_module',macro_module)
        #PrnVal('tpl',tpl)
        print("**************End Template error***********************")



#************************dext utility******************************************


def getAllChildClass(ouid):
    '''
    по UID класса для всех его объектов формирует словарь имя индивидуала:индивидуал 
    '''
    terms = []
    cls=DextOntoClassWU('',ouid)
    if isinstance(cls,DextOntoClassWU):
        terms.append(cls.context)
        ch_cls=back_references(cls.context, 'subClassOf')
        ch_cls1=back_references(cls.context, 'hasMetatype')
        ch_cls.extend(ch_cls1)
        #ch_cls=backref(cls, cls.portal_type)
        for i in ch_cls:
            if isinstance(i,DextOntoClassWU):
                terms.append(i.context)
            else:
                terms.append(i)
    return terms 



def NewDextOnto(container_uid, title, desc):
    """
    создает новый индивидуал
    @container_uid - uid контейнера, где создается объекто
    @context_uid - uid родительского класса
    @title - имя объекта
    @desc - описание объекта
    """
    #container=ObjByUID(container_uid)
    #item = createContentInContainer(container, "DextOntology", title)
    #return item
    newid=getNewId()
    folder=ObjByUID(container_uid)
    #return createResearcherById(folder,newid,title)
    return _createObjectByType("DextOntology", folder, newid)


#________________________конструкторы элементов__________________________

def NewDextClass(container,context_uid, title, desc, meta):
    """
    создает новый класс
    @container -  контейнер, где создается объекто
    @context_uid - uid родительского класса
    @title - имя объекта
    @desc - описание объекта
    @meta:'sub' - устанавливается SubClassOf
               'meta' - устанавливается hasMetatype
    """
    items=[]
    catalogtool = getCatalogtool()
    if container:
        newid=getNewId()
        while newid in container.keys():
            newid=getNewId()
        context = createContent('DextOntoClass', id=newid,title=title)
        container[newid] = context
        context.reindexObject()
        context.reindexObject(idxs='modified')
        return context
    else:
        return 0
def NewDextClassByUID(container_uid,context_uid, title, desc, meta):
    """
    создает новый класс 
    @container_uid -  UID контейнера, где создается объекто
    @context_uid - uid родительского класса
    @title - имя объекта
    @desc - описание объекта
    @meta:'sub' - устанавливается SubClassOf
               'meta' - устанавливается hasMetatype
    """
    items=[]
    catalogtool = getCatalogtool()
    container=ObjByUID(container_uid)
    
    if container:
        newid=getNewId()
        while newid in container.keys():
            newid=getNewId()
        context = createContent('DextOntoClass', id=newid,title=title)
        container[newid] = context
        context.reindexObject()
        context.reindexObject(idxs='modified')
        return context
    else:
        return 0
def NewDextInd(container,context_uid, title, desc):
    """
    создает новый класс
    @container -  контейнер, где создается объекто
    @context_uid - uid родительского класса
    @title - имя объекта
    @desc - описание объекта
    @meta:'sub' - устанавливается SubClassOf
               'meta' - устанавливается hasMetatype
    """
    items=[]
    catalogtool = getCatalogtool()
    if container:
        newid=getNewId()
        while newid in container.keys():
            newid=getNewId()
        context = createContent('DextOntoIndividual', id=newid,title=title)
        container[newid] = context
        context.reindexObject()
        context.reindexObject(idxs='modified')
        return context
    else:
        return 0



def NewDextOProp(container,type_prop, title, desc, option):
    """
    создает новое object propdrty
    @container- контейнер, где создается объекто
    @option -  словарь {'subprop_uid':subprop_uid, 'range':rng}. где
    @subprop_uid - uid родительского класса
    @rng - список uid объектов для Range
    @title - имя объекта
    @desc - описание объекта
    @type_prop - строка, укажывающая тип свойства 
    """
    #site = getSite()
    items=[]
    catalogtool = getCatalogtool()
    if container:
        newid=getNewId()
        while newid in container.keys():
            newid=getNewId()
        context = createContent(type_prop, id=newid,title=title)
        container[newid] = context
        context.reindexObject()
        context.reindexObject(idxs='modified')
        if option and 'range' in option.keys():
            rangelst=option['range']
            if not isinstance(rangelst,list):
                rangelst=[rangelst]
            out=[ObjByUID(i) for i in rangelst if isinstance(i,str)]
            updaterange(context,out,'range')
        if not 'range' in option.keys():
            updaterange(context,[dextempty_class()],'range')
        if option and 'value' in option.keys() and option['value']:
            context.value=option['value']
            context.reindexObject()
            context.reindexObject(idxs='modified')
        return context
    else:
        return 0


#_______________________________________________________________________________________


def relations_by_prop(obj,prop):
    result=[]
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    relations = catalog.findRelations(
        dict(
            to_id=intids.getId(aq_inner(obj)),
            from_attribute=prop
        )
    )
    relations1 = list(relations)
    for rel in relations1:
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result


def back_references(source_object, attribute_name):
    """ 
    Return back references from source object on specified attribute_name 
    """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    d=dict(to_id=intids.getId(aq_inner(source_object)), from_attribute=attribute_name)
    for rel in catalog.findRelations(
                dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute=attribute_name)
            ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and obj not in result and checkPermission('zope2.View', obj):
            result.append(obj)
    return result    
#--------------------------------------------------------------
def create_classes(classes,parent):
    """
    в онтологии типа DextOntology - параметр parent
    создает набор классов из списка classes
  
    """
    for item in classes:
        container_uid=parent
        context_uid=''
        title=item['nameclass']
        rootclass=item['rootclass']
        isexist=getDextByNameAndPath(title, parent,'DextOntoClass')
        if not isexist:
            desc=''
            meta=''
            oclass=NewDextClass(container_uid,context_uid, title, desc, meta)
        if rootclass=='True':
            baseclass=getDextByNameAndPath(title, parent,'DextOntoClass')
            baseclass.rootclass=True
            baseclass.reindexObject()
            baseclass.reindexObject(idxs='modified')            

def createSubClasses(classes,parent,pref=''):
    #intids = component.getUtility(IIntIds)
    intids = getUtility(IIntIds)
    lst_parentclass=[]
    for item in classes:
        container_uid=parent
        context_uid=''
        if pref:
            title=pref+':'+item['nameclass']
        else:
            title=item['nameclass']
        baseclass=getDextByNameAndPath(title, parent,'DextOntoClass')
        if item['subClassOf'] and not item['subClassOf']==u'not data':
            i=item['subClassOf'][0]
            c=getDextByNameAndPath(i, parent,'DextOntoClass')
            if c:
                lst_parentclass.append(c)
                updaterange(baseclass,lst_parentclass,'subClassOf')
                lst_parentclass=[]
        else:
            lst_parentclass=[]
         
def createListRefForClasses(classes,parent,propertylist,classname=''):
    intids = getUtility(IIntIds)
    lst_parentclass=[]
    if classname:
        if classname in classes.keys():
            item=classes[classname]
            for property in propertylist:
                createRefForClass(item[property],parent,property,classname)
    else:
        for title,item in classes.items():
            for property in propertylist:
                createRefForClass(item[property],parent,property,title)


def createRefForClasses(classes,parent,property,classname=''):
    intids = getUtility(IIntIds)
    lst_parentclass=[]
    if classname:
        if classname in classes.keys():
            item=classes[classname]
            createRefForClass(item,parent,property,classname)
    else:
        for title,item in classes.items():
            createRefForClass(item,parent,property,title)
            
def createRefForClass(item,parent,property,classname):
    intids = getUtility(IIntIds)
    lst_parentclass=[]
    if item:
        for i in item:

            target_onto=getDextByNameAndPath(i.parentclass_name, parent,'DextOntology')
            if target_onto:
                c_lst=[getDextByNameAndPath(i.target_name,target_onto,'DextOntoClass')]
            else:
                c_lst=[getDextByNameAndPath(i.target_name,parent,'DextOntoClass')]
    else:
        c_lst=[dextempty_class()]
    baseclass=getDextByNameAndPath(classname, parent,'DextOntoClass')
    if c_lst and baseclass:
        updaterange(baseclass,c_lst,property)        

         
def create_objects(objects,parent):
    """
    "individuals":
    [{"dProps": {},"name": "ggggg","sourceClass": ["учебный объект],"oProps": {}}, ]
    """
    for item in classes:
        container_uid=parent
        context_uid=''
        title=item['name']
        isexist=getDextByNameAndPath(title, parent,'DextIndividual')
        if not isexist:
            oclass=NewDextClass(container_uid,context_uid, title, desc, meta)
 



def getOProp(cls):
    '''
    domain -  = self.context.UID()
    name - имя свойства
    nameproperty - UID родительского свойства
    #self.context - OntoClass
    #res1 - список [title контекста, [список связанныхClassObjectProperty]]
    #par_list - [список родмтельских классов]    '''
    intids = getUtility(IIntIds)
    d1 = []
    res1 = []
    res=WorkUnit(cls.UID()).getWUnit()["codata"]
    for k in res:
        temp = {}
        prop_name=k.title_or_id()
        rang=k.getRange()
        op_uid=k.UID()
        temp['domain'] = cls.UID()
        temp['name'] =prop_name
        temp['nameproperty'] = op_uid
        terms = []
        if rang:
            values = [RelationValue(intids.getId(c)) for c in rang]
        else:
            values=[RelationValue(intids.getId(dextempty_class()))]
        temp['orange'] = values
        d1.append(temp)
       
    return d1
########################## agent for jsonutility ########################################

def OntoAgent(kw):
    #return listontologys()
    return listontologys()

   
def AllContent(kw):
    id_file=kw['content_type']
    catalogtool = getCatalogtool()
    output={}
    r=[]
    files =catalogtool.searchResults(portal_type = id_file)
    f = [i.getObject()for i in files]
    for item in f:
        output['id']=item.getId()
        output['desc']=item.Description()
        output['title']=item.Title()
        output['url']=item.absolute_url()
        r.append(output)
        output={}
    return r
def getManagerResponse(kw):
    ouid=kw['ouid']
    uid=kw['uid']  
    obs=Observer()
    if ouid:
        return obs(ouid)
    if uid:
        return obs(uid)

def moveContent():
    portal = api.portal.get()
    contact = portal['about']['contact']
    api.content.move(source=contact, target=portal)

def getItemByName(kw):
    name=kw['name']
    itemtype=kw['itemtype']
    out=getOntoItemByName(name,itemtype)
    out1=[{toUTF(item.title_or_id()):{'uid':item.UID(), 'url':item.absolute_url()}} for item in out]
    return out1 
def getPropByName():
    return getDextItemByPath(parent,dext_type)

def doSubClassOf(kw):
    container_name=kw['container_name']
    baseclass_name=kw['baseclass_name']
    subclass_name=kw['subclass_name']
    parent=getOntoItemByName(container_name,'DextOntology')[0]
    lst_baseclass=getDextByNameAndPath(baseclass_name, parent,'DextOntoClass')
    lst_subclass=getDextByNameAndPath(subclass_name, parent,'DextOntoClass')
    if lst_subclass and lst_baseclass:
        if isinstance(lst_baseclass,list):
            baseclass=lst_baseclass[0]
        else:
            baseclass=lst_baseclass
        if isinstance(lst_subclass,list):
            subclass=lst_baseclass[0]
        else:
            subclass=lst_subclass
        contacts =[]
        contacts.append(subclass)
        intids = getUtility(IIntIds)
        values = [RelationValue(intids.getId(c)) for c in contacts]
        baseclass.subClassOf=values
        baseclass.reindexObject()
        baseclass.reindexObject(idxs='modified')
        sub=[r.to_object for r in baseclass.subClassOf]
        return ["subclass add"]
    else:
        return ['baseclass or subclass not found']


def doSubClass(kw):
    site = getSite()
    user = site.getWrappedOwner()
    newSecurityManager(site, user)
    container_name=kw['container_name']
    baseclass_name=kw['baseclass_name']
    subclass_name=kw['subclass_name']
    baseclass=getOntoItemByName(baseclass_name,'DextOntoClass')[0]
    subclass=getOntoItemByName(subclass_name,'DextOntoClass')[0]
    intids = getUtility(IIntIds)
    if baseclass and subclass:
        contacts =[]
        contacts.append(baseclass)
        values = [RelationValue(intids.getId(c)) for c in contacts]
        subclass.subClassOf=values
        subclass.reindexObject()
        subclass.reindexObject(idxs='modified')

def updaterange(obj,rangelst,nameproperty):
    site = getSite()
    user = site.getWrappedOwner()
    newSecurityManager(site, user)
    if rangelst:
        intids = getUtility(IIntIds)
        values = [RelationValue(intids.getId(c)) for c in rangelst if c]
        catalog = component.getUtility(ICatalog)
        
        """
        for value in values:
            if value is None:
                continue
            value.__parent__ = obj
            # also set from_object to parent object
            value.from_object = obj
            # and the attribute to the attribute name
            value.from_attribute = nameproperty
            # now we can create an intid for the relation
            id = intids.register(value)
            # and index the relation with the catalog
            catalog.index_doc(id, value)
        """
       
        if nameproperty=='subClassOf':
            obj.subClassOf=values
        elif nameproperty=='hasMetatype':
            obj.hasMetatype=values
        elif nameproperty=='hasKindOf':
            obj.hasKindOf=values
        elif nameproperty=='range':
            obj.range=values
        elif nameproperty=='sbprop_uid':
            obj.sbprop_uid=values
        elif nameproperty=='nameproperty':
            obj.nameproperty=values
        else:
            obj.__setattr__(nameproperty, values) 

        obj.reindexObject()
        obj.reindexObject(idxs='modified')

def getIterableRangeClass(root,propertyname):
    "Возвращает последовательность range элементов"
    if root:
        root_wu=DextOntoClassWU(root,'').getWUnit()
        lst=root_wu.getObjectPropWUByName(propertyname).orange
        if lst:
            for r in lst:
                yield r
        else:
            r=dextempty_class()
            yield r
def getFestRangeItem(wu_prop_class):
    if wu_prop_class:
        if wu_prop_class.orange:
            return wu_prop_class.orange[0]
        else:
            return ''
    else:
         return ''