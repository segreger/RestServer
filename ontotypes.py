class DextWorkUnit(object):
    def __init__(self,cls,ouid):
        self.ouid=ouid
        self.uid=ouid
        self.wunit={}

        if cls:
            self.context=cls
            self.ouid=cls.UID()
        else:
            self.context=ObjByUID(ouid)
            self.ouid=ouid
        self.wunit={}
        self.description=self.context.Description()
        self.nameclass=self.context.title_or_id()
        self.absolute_url=self.context.absolute_url()
        self.portal_type =self.context.portal_type

    def update(self, in_dict):
        self.wunit.update(in_dict)

    def getWUnit(self):
        if self.context.portal_type=='DextOntoClass':return DextOntoClassWU('',self.ouid).getWUnit()
        if self.context.portal_type=='DextClassObjectProperty':return DextClassObjectPropertyWU('',self.ouid).getWUnit()
        if self.context.portal_type=='DextClassDataProperty':return DextClassDataPropertyWU('',self.ouid).getWUnit()

        return {}


class DextOntologyWU(DextWorkUnit):
    def __init__(self,cls,ouid):
        super(DextOntologyWU, self).__init__(cls,ouid)

    def getWUnit(self):
        self.wunit['classes']=getDictDextItemByPath(self.context,"DextOntoClass")
        return self.wunit


class DextOntoClassWU(DextWorkUnit):
    def __init__(self,cls,ouid):
        super(DextOntoClassWU, self).__init__(cls,ouid)
        self.oprop=self.getWUProperty('DextClassObjectProperty')
        self.dprop1=self.getWUProperty('DextClassDataProperty')
        self.cdata=[]
        self.codata=[]
    def getWUnit(self):
        self.nameclass=self.context.title_or_id()
        self.uid=self.context.UID()
        dict_prop={}
        oplist=[]
        self.oprop=self.getWUProperty('DextClassObjectProperty')
        self.dprop1=self.getWUProperty('DextClassDataProperty')
        self.cdata=[]
        self.codata=[]
        return self

    def getWUProperty(self,prop_type):
        oplist=[]
        dict_prop={}
        """
        for op in getDextItemByPath(self.context,prop_type):
            PrnVal('op.UID()' ,op.UID())
            yield op.UID()
        """

        return [oprop.UID() for oprop in getDextItemByPath(self.context,prop_type)]

        
         
    def ListDRangeItems(self):
        return [i.UID() for i in self.context.getDataProps()]


    def ListDPropWU(self):
        return [DextClassDataPropertyWU('',i) for i in self.dprop1]
    def ListOPropWU(self):
        return [DextClassObjectPropertyWU('',i) for i in self.oprop]

    def getPropWUByName(self, source,nameop=''):
        #nameop=DelSpaceToUTF(nameop)
        for k,v in source.items():
            if toUTF(nameop)==k:
                return v 
        else:
            return ''

    def getDictObjectProps(self):
        lst=self.ListOPropWU()
        source=dict([(i.prop_name,i) for i in lst if i])
        return source

    def getObjectPropWUByName(self, nameop=''):
        nameop=toUTF(nameop)
        #if nameop=='nextListItem':
        #    pdb.set_trace()
        PrnVal('nameop',nameop)
        PrnVal('cls',toUTF(self.nameclass))
        lst=[]
        """
        for i in self.getWUProperty('DextClassObjectProperty'):
            PrnVal('i',i)
            obj=DextClassObjectPropertyWU('',i)
            PrnVal('obj',obj)
            lst.append(obj)
        """
        #lst=[DextClassObjectPropertyWU('',i) for i in self.getWUProperty('DextClassObjectProperty')]
        #PrnVal('lst',lst)
        source=dict([(i.prop_name,i) for i in self.ListOPropWU() if i])
        PrnDict(source)
        return self.getPropWUByName( source,nameop)

    def getDataPropWUByName(self, namedp=''):
        """
        возвращает ClassDataPropertyWU с указанным именем
        """
        nameop= DelSpaceToUTF(namedp)
        dprops = [WorkUnit(i).getWUnit(i) for i in self.dprop1]
        source = dict([(dprop.prop_name, dprop) for dprop in dprops])
        return source[namedp]
    def getDataPropWUByName_Value(self, namedp=''):
        """
        возвращает значение ClassDataPropertyWU с указанным именем
        """
        #unamedp= DelSpaceToUTF(namedp)
        unamedp= DelSpaceToUTF(namedp)
        dprops = [DextClassDataPropertyWU('',i) for i in self.dprop1]
        source = dict([(DelSpaceToUTF(dprop.prop_name), dprop.value) for dprop in dprops])
        if source and unamedp in source.keys():
            return source[unamedp] 
        else:
            return ''



    def getDProps(self,dictname):
        out={}

        for k,v in dictname.items():
            out[k]=self.getDataPropWUByName_Value(v)
        return out



    def getDictOPropsByName(self):
        out=dict([(DelSpaceToUTF(DextClassObjectPropertyWU('',i).prop_name),DextClassObjectPropertyWU('',i)) for i in self.oprop if i])
        return out
    def getDictDPropsByName(self):
        #return dict([(DextClassDataPropertyWU('',i).prop_name,DextClassDataPropertyWU('',i).value) for i in self.dprop1 if i])              
        return dict([(DextClassDataPropertyWU('',i).prop_name,DextClassDataPropertyWU('',i).value) for i in self.dprop1 if i])              


class DextClassObjectPropertyWU(DextWorkUnit):
    def __init__(self,cls=None,ouid=''):
        self.cls=cls
        super(DextClassObjectPropertyWU, self).__init__(cls,ouid)
        self.range=self.context.range
        self.op_uid=self.context.nameproperty or ''
        self.prop_name=self.context.title
        self.orange=self.wu_rangeitem()
        self.uid=self.context.UID()
        self.dict_props=self.getDictProps()
    def getDictProps(self):
        temp = {}
        if self.cls:
            temp['domain'] = self.cls.UID()
        else:
            temp['domain'] = ''
        temp['name'] =self.prop_name
        temp['nameproperty'] = self.parent_prop()
        temp['orange']=self.rangeitem()
        temp['uid']=self.context.UID()
        temp['cls']=self.context
        return temp

    def getWUnit(self):
        return self
    def wu_rangeitem(self):
        rlst=self.rangeitem()
        if rlst:
            rangeitem=[DextWorkUnit('',r[2]).getWUnit() for r in rlst]
        else:
            rangeitem=[DextWorkUnit(r,'').getWUnit() for r in dextempty_class()]
        return rangeitem


    def rangeitem(self):
        intids = getUtility(IIntIds)
        rangelist=[]
        if self.range:
            rvalues = [RelationValue(intids.getId(c)).to_object for c in self.range]
        else:
            rvalues = [RelationValue(intids.getId(c)).to_object for c in [dextempty_class()]]
     
        for r in rvalues:
            if isinstance(r,RelationValue):
                obj=r.to_object
                if obj:
                    rangelist.append((obj.title_or_id(), obj.absolute_url(), obj.UID(), self.op_uid))
                else:
                    cl=dextempty_class()
                    rangelist.append((cl.title_or_id(), cl.absolute_url(), cl.UID(), self.op_uid))

            else:
                rangelist.append((r.title_or_id(), r.absolute_url(), r.UID(), self.op_uid))
        return rangelist

    def parent_prop(self):
        intids = getUtility(IIntIds)
        if self.op_uid:
            values = [RelationValue(intids.getId(c)).to_object for c in self.op_uid][0]
            return values.to_object.UID()
        else:
            values='None'
        return values
    
    def getRelationRange(self):
        values=[]
        intids = getUtility(IIntIds)
        if self.range:
            rvalues=[]
            for r in self.range:
                if isinstance(r,RelationValue) and r.to_object:
                    ob=r.to_object
                    if not ob:
                        ob=dextempty_class()
                if isinstance(r,RelationValue) and not r.to_object:
                        ob=dextempty_class()
                if r and not isinstance(r,RelationValue):
                    ob=r
                rvalues.append(ob)

        else:
            rvalues=[dextempty_class()]
        return rvalues



class DextClassDataPropertyWU(DextWorkUnit):
    def __init__(self,cls=None,ouid=''):
        self.cls=cls
        self.uid=ouid
        if self.cls and not ouid:
            self.uid=self.cls.UID()
        if not self.cls and ouid:
            self.cls=ObjByUID(ouid)

        super(DextClassDataPropertyWU, self).__init__(cls,ouid)
        self.range=self.context.range
        self.sbprop_uid=self.context.nameproperty
        self.prop_name=self.context.title
        self.value=self.context.value
        self.id=self.context.id
        self.uid=self.context.UID()
        self.prop_info={}
        self.prop_info['prop_name']=self.prop_name
        self.prop_info['def_value']=self.value
        self.prop_info['prop_uid']=self.uid
        self.prop_info['sbprop_uid']=self.sbprop_uid
        self.prop_info['prop_url']=self.cls.absolute_url()
        #rangelist.append((obj.title_or_id(), obj.absolute_url(),self.id,self.value, self.prop_name, self.uid)) 
        self.wunit['RangeInfo']=self.rangeitem()
        self.wunit['PropInfo']=self.prop_info

    def getWUnit(self):
         return self

    def getDictProps(self):
        temp = {}
        if self.cls:
            temp['domain'] = self.cls.UID()
        else:
            temp['domain'] = ''
        temp['name'] =self.prop_name
        temp['nameproperty'] = self.sbprop_uid
        temp['orange']=self.range
        temp['value']=self.value
        temp['uid']=self.context.UID()
        temp['cls']=self.context
        temp['range']=self.rangeitem()
        return temp

    def rangeitem(self):
        intids = getUtility(IIntIds)
        rangelist=[]
        if self.range:
            rvalues = [RelationValue(intids.getId(c)).to_object for c in self.range]
        else:
            rvalues=[RelationValue(intids.getId(dextempty_class())).to_object]
        for r in rvalues:
            if isinstance(r,RelationValue):
                obj=r.to_object
                rangelist.append((obj.title_or_id(), obj.absolute_url(),obj.UID(),self.id,self.value, self.prop_name, self.uid)) 
            else:
                rangelist.append(('', '',self.id,self.uid, self.value, self.prop_name, self.sbprop_uid))   
        return rangelist


    def parent_prop(self):
        intids = getUtility(IIntIds)
        if self.op_uid:
            values = [RelationValue(intids.getId(c)).to_object for c in op_uid][0]
            return values.UID()
        else:
            values='None'
            return values
    def getRelationRange(self):
        if self.range:
            values=[]
            for c in self.range:
                if isinstance(c,RelationValue):
                    values.append(c.to_object )
                else:
                    values.append(dextempty_class())
        return values