from Graph import *
class DepNode(Node):
    def __init__(self,name,id_node,dep_type):
        super().__init__(name,id_node)
        self.name=name
        self.id_node=id_node
        self.dep_type=dep_type


    def node_from_row(self,row, list_name):
        self.name=row[list_name[0]]
        self.id_node=row[list_name[2]]
        self.children=row[list_name[3]]
    def __str__(self):
        out=''
        out+='name='+self.name+'\n'
        out+=' id_node='+self.id_node+'\n'
        if self.value:
            out+ 'value='+self.value +'\n'
        for c in self.children:
            out+=c+'\n'
        return out


class DepGraph(Graph):
    def __init__(self,df,name_id,name_plant, name_ref,dep_type):
        super().__init__(df)
        self.df=df
        self.name_id=name_id
        self.name_plant=name_plant
        self.name_ref=name_ref
        self.dep_type=dep_type
        #self.nodes={}#Словарь всех узлов,ключ - имя узла
        self.edges=[]# список ребер между объектами Node
        lst_id=self.df[name_id].tolist()
        lst_name=self.df[name_plant].tolist()
        lst_ref=self.df[name_ref].tolist()
        lst_type=self.df[dep_type].tolist()
        
        #self.dict_name=dict([(lst_id[i],NodeValue(lst_id[i], lst_name[i],lst_ref[i],lst_type[i],'')) for i in range(len(lst_id))])
        self.nodes=dict([(lst_id[i],DepNode(lst_name[i],lst_id[i],lst_type[i])) for i in range(len(lst_id))])
        EmptyValue=NodeValue('empty_class','empty_class','','','')
        #self.dict_name['empty_class']=EmptyValue
        dict_relation={} 
        g = self.df.groupby(name_ref)
        #добавляем узлы, имеющих подчиненных
        for (i, sub_df) in g:
            lst=sub_df[name_id].tolist()
            if i !='root':
                node=self.nodes[i]
                node.children=lst
                
        for k,v in self.nodes.items():
            for t in v.children:
                rel=Relation(t,k)
                self.edges.append(rel)
        
               

    def __str__(self):
        out=''
        for n,v in self.nodes.items():
            out=out+'\n'+v.name+'\n'
            for i in v.children:
                out=out+'\t'+i+'\n'
        return out
    
    def elements(self):
        lst_nodes=[ {'data': {'id': k, 'label': v.name, 'width': '500px','height': '150px',},'classes':'multiline-auto', } for k,v in self.nodes.items()]

        
        lst_edges=[{'data': {'source': edg.source, 'target': edg.target}} for edg in self.edges]

        return lst_nodes+lst_edges