import codecs
#from matplotlib.pyplot import axes
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_cytoscape as cyto
from datetime import datetime as dt
from datetime import timedelta



GRID_COLS=6 # число колонок
RECT_WIDTH=55 # ширина прямоугольника
RECT_HEIGHT=25# высота прямоугольника
RECT_X_SPACE=10 # расстояние по горизонтали между прямоугольниками
RECT_Y_SPACE=RECT_HEIGHT+10 # расстояние по вертикали между прямоугольниками
RECT_LAYER_SPACE=15 # расстояние по вертикали между уровнями



def load_list(filename):
	words=[]
	with codecs.open(filename, 'r', 'cp1251') as my_file:
		for line in my_file:
			if line.strip():
				#key, value = line.strip().split(';')
				words.append(tuple(line.strip().split(';')))
	return words


def get_department():
    kadr_df=pd.read_excel('taskdata\Кадры.xlsx')
    lst_label=kadr_df['Подразделение'].tolist()
    lst_level=kadr_df['уровень'].tolist()
    return (lst_label, lst_level)

def get_department_by_level(filename):
    out=[]
    kadr_df=pd.read_excel(filename)
    #lst_label=kadr_df['Подразделение'].tolist()
    #lst_level=kadr_df['уровень'].tolist()
    g = kadr_df.groupby('уровень1')
    for (i, sub_df) in g:
        item={'level':i,
              'count':len(sub_df),
              'id': sub_df['ID'].tolist(), 
              'labels':sub_df['Подразделение'].tolist(), 
              'cols':sub_df['col1'].tolist(),
              'rows':sub_df['row1'].tolist(),
              'width':sub_df['ширина'].tolist(),
              }
        out.append(item)
    #out.reverse()
    return out

def get_elements(filename, mode='rect'):
    """
    создает список узлов подразделений графа организационной стуктуры
    с представлением в виде прямоуголников при mode=='rect' или окружностей при mode='circle'
    """
    diam=30#диаметр окружности узла подразделения
    in_data=get_department_by_level(filename)
    #{'level':i,'count':len(sub_df),'labels':sub_df['Подразделение'].tolist()}
    levels=[]
    nodes=[]
    y0=0
    y=0
    if mode=='circle':
        return get_circle_elements(filename,diam)
    else:

        for item in range(len(in_data)):
            lbl=str(in_data[item]['level'])
            level='lev'+lbl
            levels.append({'data': {'id': level, 'label': 'уровень '+lbl}})

            labels= in_data[item]['labels']
            ids=in_data[item]['id']
            cols=in_data[item]['cols']
            rows=in_data[item]['rows']
            subcol=in_data[item]['width']
            max_row=max(rows)
            """
            GRID_COLS=6 # число колонок
            RECT_WIDTH=55 # ширина прямоугольника
            RECT_HEIGHT=30# высота прямоугольника
            RECT_X_SPACE=10 # расстояние по горизонтали между прямоугольниками
            RECT_Y_SPACE=RECT_HEIGHT+10 # расстояние по вертикали между прямоугольниками
            RECT_LAYER_SPACE=15 # расстояние по вертикали между уровнями
            """
            for i in range(len(labels)):
                y =y0+RECT_Y_SPACE*rows[i]
                x= (RECT_WIDTH+RECT_X_SPACE)*cols[i]
                position= {'x': x, 'y': y}
                node={'data': 
                        {'id': str(ids[i]),
                        'title':str(ids[i])+' '+labels[i],
                        'label':labels[i],
                        'shape_type':'rectangle',
                        'width':str(int(RECT_WIDTH*subcol[i]))+'px',
                        'height':str(RECT_HEIGHT)+'px', 
                        'node_color':'white',
                        'border-color':'black',
                        'row':rows[i],
                        'col':cols[i],
                        },
                    'position':position,
                    'classes':'multiline-auto',
                    }
                nodes.append(node)
        return (levels, nodes)


def get_circle_elements(filename,diam):
    """
    filename - файл с таблицей структуры организации
    diam - диаметр окружности, представляющей подразделение
    """
    out=[]
    kadr_df=pd.read_excel(filename)
    #lst_label=kadr_df['Подразделение'].tolist()
    #lst_level=kadr_df['уровень'].tolist()
    g = kadr_df.groupby('уровень1')
    for (i, sub_df) in g:
        item={'level':i,
              'count':len(sub_df),
              'id': sub_df['ID'].tolist(), 
              'labels':sub_df['ID'].tolist(), 
              'cols':sub_df['col1'].tolist(),
              'rows':sub_df['row1'].tolist(),
              'width':sub_df['ширина'].tolist(),
              }
        out.append(item)
    in_data=out
    #{'level':i,'count':len(sub_df),'labels':sub_df['Подразделение'].tolist()}
    levels=[]
    nodes=[]
    y0=0
    y=0
    for item in range(len(in_data)):
        labels= in_data[item]['labels']
        ids=in_data[item]['id']
        cols=in_data[item]['cols']
        rows=in_data[item]['rows']
        subcol=in_data[item]['width']
        max_row=max(rows)
        """
        GRID_COLS=6 # число колонок
        RECT_WIDTH=55 # ширина прямоугольника
        RECT_HEIGHT=30# высота прямоугольника
        RECT_X_SPACE=10 # расстояние по горизонтали между прямоугольниками
        RECT_Y_SPACE=RECT_HEIGHT+10 # расстояние по вертикали между прямоугольниками
        RECT_LAYER_SPACE=15 # расстояние по вертикали между уровнями
        """
        for i in range(len(labels)):
            y =y0+RECT_Y_SPACE*rows[i]
            x= (RECT_WIDTH+RECT_X_SPACE)*cols[i]
            position= {'x': x, 'y': y}
            node={'data': 
                    {'id': str(ids[i]),
                     'title':str(labels[i]),
                     'label':labels[i],
                     'shape_type':'circle',
                     'width':str(diam)+'px',
                     'height':str(diam)+'px', 
                     'node_color':'white',
                     'row':rows[i],
                     'col':cols[i],
                     },
                   'position':position,
                   'classes':'multiline-auto',
                  }
            nodes.append(node)
 

    return (levels, nodes)


def get_edg_department():
	st_edges=[]
	df=pd.read_excel('задачи.xlsx')
	#df["дата"] = pd.to_datetime(df["дата"], format='%d.%m.%Y')
	#df.sort_values(by=["дата", "время"],ascending=True)
	#df.set_index('дата')
	df.index = pd.to_datetime(df['дата'])#индекс по дате
	lst_target=df['name'].tolist()
	lst_source =df['связанные задания'].tolist()
	lst_period=df['период решения'].tolist()
	lst_color=[get_color(period) for period in lst_period]
	lst_type=df['тип'].tolist()
	return df

def get_color(period):
    period=int(period)
    if period<=3:
        color='rgb(0,255,0)'
    elif period>3 and period<=15:
        color= 'rgb(0,0,255)'
    else:
        color= 'rgb(255,0,0)'
    return '#FFA500'

def get_anime_edgs(n):
    """
    пример формирования списка связей для анимации
    """
    global df

    lst_edges=[]
    n=n+1
    lst_target=df['name'].tolist()
    if n<len(lst_target):
        df1=df.loc[0:n]
        yield df1
    else:
        return df 
	
def get_tasks():
    df=pd.read_excel('задачи.xlsx')
    return df

def localDF(df):
    lst_edges=[]
    lst_target=df['name'].tolist()
    from_v=df['инициатор задания'].tolist()
    to_v=df['получатель'].tolist()
    lst_source =df['связанные задания'].tolist()
    lst_period=df['период решения'].tolist()
    lst_color=[get_color(period) for period in lst_period]
    lst_type=df['тип'].tolist()
    nodes_loc = set()
    cy_edges = []
    cy_nodes = []
    
    for i in range(len(lst_source)):
        source, target, timerange, msg_type = lst_source[i], lst_target[i], lst_period[i], lst_type[i]
        #from_id, to_id = from_v[i], to_v[i]
        
        if 1:#not source == 'root'and not target =='root':
            t_source={"data": {'par':str(from_v[i]),"id": str(source), "label": '', "timerange":timerange, 'node_color':get_color(timerange), },'classes':'task'}
            cy_nodes.append(t_source)
            t_target={"data": {'par':str(to_v[i]), "id": str(target), "label":'', "timerange":timerange, 'node_color':get_color(timerange),},'classes':'task'}
            cy_nodes.append(t_target)
        if msg_type=="запрос": # and not (target=='root' or source =='root'):
            data={'data': {'source': str(source),'target': str(target),'msg_type':msg_type,},'classes':'blackedge'}
            cy_edges.append(data)
            
        elif msg_type=='ответ': #and not (target=='root' or source =='root'):
            data={'data': {'source': str(target),'target': str(source),'msg_type':msg_type,},'classes':'edge'}
            cy_edges.append(data)


            

        #cy_edges.append({'data': {'source': str(from_id),'target': str(to_id),'msg_type':msg_type,},'classes':'edge'})
        

    return (cy_nodes, cy_edges)



def get_edgsFromDF(df):
    """
    cy_nodes - список узлов, где узлы являются задачами
    cy_edges - список связей между задачами

    """
    lst_edges=[]
    #df = pd.read_pickle('task_frame.pkl') #to load 123.pkl back to the dataframe df
    #df=pd.read_excel('задачи.xlsx')
    
    #df["дата"] = pd.to_datetime(df["дата"], format='%d.%m.%Y')
    #df.sort_values(by=["дата", "время"],ascending=True)
    lst_target=df['name'].tolist() # элемент из lst_target определяет текущую задачу

    lst_source =df['связанные задания'].tolist()#элемент из  lst_source определяет роительскую задачу
    # root имя корня дерева задач, соответствует внешнему запросу, возможно нужно это сделать типом задачи или согласовать с типом "внешняя"
    lst_period=df['период решения'].tolist()
    lst_color=[get_color(period) for period in lst_period]
    lst_type=df['тип'].tolist()
    nodes = set()

    cy_edges = []
    cy_nodes = []

    for i in range(len(lst_source)):
        source, target, timerange, msg_type = lst_source[i], lst_target[i], lst_period[i], lst_type[i]

        if source not in nodes:
            nodes.add(source)
            cy_nodes.append({"data": {"id": source, "label": source, "timerange":timerange, 'node_color':get_color(timerange)}})
        if target not in nodes:
            nodes.add(target)
            cy_nodes.append({"data": {"id": target, "label": target, "timerange":timerange, 'node_color':get_color(timerange)}})


        cy_edges.append({
            'data': {
                'source': source,
                'target': target,
                'msg_type':msg_type,
            },
        })
    return cy_edges + cy_nodes
def dep_egds(filename):
    """
    cy_nodes - список узлов, где узлы являются задачами
    cy_edges - список связей между задачами

    """
    df=pd.read_excel(filename)
    lst_edges=[]
    lst_target=df['родитель'].tolist() # элемент из lst_target определяет текущую задачу
    lst_source =df['ID'].tolist()#элемент из  lst_source определяет роительскую задачу
    # root имя корня дерева задач, соответствует внешнему запросу, возможно нужно это сделать типом задачи или согласовать с типом "внешняя"
    nodes = set()

    cy_edges = []
    cy_nodes = []

    for i in range(len(lst_source)):
        source, target = lst_source[i], lst_target[i]
        if source !='root' and target !='root':
            cy_edges.append({
                'data': {
                    'source': source,
                    'target': target,
                },
                'classes':'depedge',
            })
    return cy_edges





def get_fig(df):
    stylesheet = [
        {
            "selector": 'node', #For all nodes
            'style': {
                "opacity": 0.9,
                "label":'data(label)', #Label of node to display
                "background-color":'data(node_color)', #"#07ABA0", #node color
                "color": "#008B80", #node label color
            }
        },
        {
            "selector": 'edge', #For all edges
            "style": {
                "target-arrow-color": "#C5D3E2", #Arrow color
                "target-arrow-shape": "triangle", #Arrow shape
                #"line-color": "#C5D3E2" edge color
                'arrow-scale': 2, #Arrow size
                'curve-style': 'bezier' #Default curve-If it is style, the arrow will not be displayed, so specify it
                }
        },
        {
            'selector': 'запрос',
            'style': {
                'line-color': 'blue'
                }
        },
        {
            'selector': 'ответ',
            'style': {
                'line-color': 'green'
            }
        },
        ]
    layout = html.Div([

        html.Div(children=[
            cyto.Cytoscape(
                id='cytoscape',
                elements=get_edgsFromDF(df),
                style={
                    'height': '95vh',
                    'width': '100%'
                },
                layout={
                    'name': 'breadthfirst'
                },
                stylesheet=stylesheet
            )
        ])
    ])
    return layout

def get_fig1(elements):
    stylesheet = [
        {
            "selector": 'node', #For all nodes
            'style': {
                "opacity": 0.9,
                "label":'data(label)', #Label of node to display
                "background-color":'data(node_color)', #"#07ABA0", #node color
                "color": "white", #node label color
            }
        },
        {
            "selector": 'edge', #For all edges
            "style": {
                "target-arrow-color": "#C5D3E2", #Arrow color
                "target-arrow-shape": "triangle", #Arrow shape
                #"line-color": "#C5D3E2" edge color
                'arrow-scale': 2, #Arrow size
                'curve-style': 'bezier' #Default curve-If it is style, the arrow will not be displayed, so specify it
                }
        },
        {
            'selector': 'запрос',
            'style': {
                'line-color': 'blue'
                }
        },
        {
            'selector': 'ответ',
            'style': {
                'line-color': 'green'
            }
        },
        
        ]

    

    node_style={
                'selector': 'node',
                'style': {
                    'content': 'data(title)',
                    'labelValig': "middle",
                    'shape':'data(shape_type)',
                    'width': 'data(width)',
                    'height': 'data(height)',
                    "border-color": "#E0FFFF",
                    "border-width": "1",
                    "text-valign" : "center",
                    "text-halign" : "center",
                    'font-size':'14px',
                    "background-color":'data(node_color)',
                    'padding': 1,
                    }
                } 

    node_to_node_style={
                'selector': '$node > node',
                'style': {
                    'padding-top': '20px',
                    'padding-left': '20px',
                    'padding-bottom': '20px',
                    'padding-right': '20px',
                    'text-valign': 'top',
                    'text-halign': 'center',
                    'background-color': 'white',

                        }
                }

    edge_style= {
                'selector': '.edge',
                'style': {
                        'source-arrow-color': 'red',
                        'source-arrow-shape': 'triangle',
                        'line-color': 'red',
                        'width': 1,
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        }
                }
    edge_black_style= {
                'selector': '.blackedge',
                'style': {
                        'target-arrow-color': 'black',
                        'source-arrow-color': 'black',
                        'width': 1,
                        'line-color': 'black',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        }
                }

    dep_edge_style= {
                'selector': '.depedge',
                'style': {
                        'width': 1,
                        'source-arrow-color': '#6495ED',
                        'source-arrow-shape': 'triangle',
                        'line-color': '#6495ED',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        }
                }


    wrap_line={
                "selector": ".multiline-auto",
                "style":{
                    'content': 'data(title)',
                    'labelValig': "middle",
                    'shape':'data(shape_type)',
                    'width': 'data(width)',
                    'height': 'data(height)',
                    "border-color": "gray",
                    "border-width": "1",
                    "text-valign" : "center",
                    "text-halign" : "center",
                    'font-size':'14px',
                    "background-color":'data(node_color)',
                    'padding': 1,
                    'text-wrap': 'wrap',
                        "text-max-width": 200
                        }
            }
    layout = html.Div([

        html.Div(children=[
            cyto.Cytoscape(
                id='cytoscape5',
                elements=elements,
                style={
                    'height': '95vh',
                    'width': '100%'
                },
                layout={
                    'name': 'preset'
                },
                stylesheet=BASE_STYLELIST
            )
        ])
    ])
    return layout



def task_by_level(nodes, df=''):
    """
    возвращает кортеж задач и связей задач, задачи расширены на координаты позиции,
    родитель задач установлен в уроветь подразделений
    цель - рисовать задачи как кружки поверх прямоугольеиков подразделений

    """
    #получаем координаты для прямоугольников подразделений
    lst_tasks=[]
    t_all=[]
    #t_lst список для задач
    #t1_lst список для связей между задачами
    #сделать получение списков напрямую из DataFrame
    GRID_COLS=6 # число колонок
    RECT_WIDTH=55 # ширина прямоугольника
    RECT_HEIGHT=20# высота прямоугольника
    RECT_X_SPACE=10 # расстояние по горизонтали между прямоугольниками
    RECT_Y_SPACE=RECT_HEIGHT+15 # расстояние по вертикали между прямоугольниками
    RECT_LAYER_SPACE=20 # расстояние по вертикали между уровнями
    if not df.empty:

        t_lst,t1_lst=localDF(df)
        for n in nodes:
           
            pos=n['position']#координаты подразделения
            #level=n['data']['parent']
            node_id=n['data']['id']
            #dict_nodes[node_id]={'level':level,'position':pos,'t_count':t_count}
            #получение списка задач из DataFrame
            t_parent=[t for t in t_lst if t['data']['par']==node_id]
            t_count=len(t_parent) # число задач у подразделения
            x0=pos['x']-RECT_WIDTH/2
            y0=pos['y']+RECT_HEIGHT/2
            for i in range(t_count):
                t=t_parent[i]
                
                x=x0+i*RECT_WIDTH/t_count
                
                y=y0+6
                t['position']={'x':int(x),'y':int(y)}
                t['data']['label']=''
                t['data']['shape_type']='circle'
                t['data']['width']='5px'
                t['data']['height']='5px'
                t['data']['node-color']='red'
                t['classes']='task'
            t_all+=t_parent  
        return (t_all,t1_lst)
    else:
        return ([],[])
"""
def get_levels_with_edgs():
    in_data=get_department()
    lst_label=in_data[0]
    lst_level=in_data[1]
    lev_s=list(set(lst_level))
    lev_s.sort()
    levels=[]
    for i in range(len(lev_s)):
        levels.append({'data': {'id': 'lev'+str(i), 'label': 'уровень '+str(i)}})
    for i in range(len(lst_label)):
        lev='lev'+str(lst_level[i])
        nodes.append({'data': {'id': lst_label[i], 'label': lst_label[i], 'parent':lev}})
        #'breadthfirst'
    lev_egd=[{'data': {'source': 'lev1', 'target': 'lev2'},
              'classes': 'levels'},
             {'data': {'source': 'lev2', 'target': 'lev3'},
              'classes': 'levels'},
            ]


    return (levels, lev_edg)
"""

def social_up():
    node_color={'мастер 1_5':'red',
                'мастер 1_6':'Yellow',
                'мастер 1_7':'DodgerBlue', 
                'мастер 1_8': 'green',
                'мастер 19_5':'Navy', 
                'мастер 19_6':'Fuchsia',
                'мастер 19_7': 'Cyan',
                'мастер 19_8':'Lime',
                }
    out=[]
    kadr_df=pd.read_excel('taskdata\лифт.xlsx')
    #lst_label=kadr_df['Подразделение'].tolist()
    #lst_level=kadr_df['уровень'].tolist()
    g = kadr_df.groupby('должность')
    lst_df=[]
    for (i, sub_df) in g:
        source=sub_df['source'].tolist()
        target=sub_df['target'].tolist()
        labels=sub_df['должность'].tolist()
        delta=sub_df['продолжительность'].tolist()
        num=[]
        for i in range(len(delta)):
            if i==0:
                s=delta[i]
            else:
                s=delta[i]+sum(delta[:i])
            num.append(s)
        sub_df.loc[:,'num']=num
        num1 = sub_df['продолжительность'].tolist()
        
        lst_df.append(sub_df)
        """
        for j in range(len(source)):
            d = {'data': {'source': str(target[j]), 'target': str(source[j]), 'node_color': node_color[labels[j]], 'label': labels[j], 'delta': num[i]}, 'classes': 'socio'}
            out.append(d)
        
        """
      
    df = pd.concat(objs=lst_df)
    delta = df['num'].tolist()
    lst = ['01.01.'+str(1980+num) for num in delta ]

    df.loc[:, 'дата'] = lst
    df['дата'] = pd.to_datetime(df['дата'])
    #pd.to_datetime(01.01.'+str(1980+df.loc[:,'num']))
    df.sort_values(by=["дата"], inplace=True)
    
        
    df.set_index(["дата"])
    

    #df.shift(periods=df['num'], freq='Y',axis=1)
    #df.sort_values(by=["дата"], inplace=True)
    


    #df.sort_values(by="num",ascending=True)
    #df.set_index("num")
    source = df['source'].tolist()
    target=df['target'].tolist()
    labels=df['должность'].tolist()
    delta=df['num'].tolist()
    
    for j in range(len(source)):
        d={'data': {'source': str(target[j]), 'target': str(source[j]),'node_color':node_color[labels[j]], 'label':labels[j],'delta':delta[i]}, 'classes': 'socio'}
        out.append(d)
    
    return out    

def update_elements(filename, taskfilename,mode='rect'):
    nodes=get_elements(filename,mode)[1]
    dep_edges_lst1=dep_egds(filename)
    if taskfilename:
        df1=pd.read_excel( taskfilename)
    else:
        return '' 
    tgraph1=TaskGraph(nodes,df1)
     
    #lst_n, lst_ed = tgraph1.localDF(df1)
    #out=tgraph1.task_by_level(lst_n)
    out=tgraph1.out_graph
    d_tasks1=tgraph1.dict_tasks
    #res=(out,lst_ed)
    res=tgraph1.res
    return (nodes,res, out, d_tasks1)

class Task():
	"""
	Создает обьект задачи на основе строки таблицы  Excel или источника с такой-же структурой 
	"""
	def __init__(self,data_in):
		self.root_task=data_in['связанные задания']# root_task#+':'+data['инициатор задания']+':'+data['получатель']
		self.name=data_in['name']#+':'+data['инициатор задания']+':'+data['получатель']
		self.source_dep=data_in['инициатор задания']
		self.target_dep=data_in['получатель']
		if data_in['дата']:
			self.start_data=data_in['дата']
		else:
			dt.strptime('01.01.2020', '%d.%m.%Y')
		if data_in['период решения']:
			self.data_delta=data_in['период решения']#data['период решения']
		else:
			self.data_delta=1
		if data_in['тип']:
			self.msg_type=data_in['тип']
		else:
			self.data_delta='запрос'	
class TaskGraph:
    
    def __init__(self, nodes,df='', mode='rect'):
        "task_lst получаем из generate_all()"
        self.nodes=nodes
        self.tasknodes=[]
        self.dict_tasks={}
        self.dict_deps={}
        self.width = 0
        self.height=0
        self.df=df
        if isinstance(self.df, pd.DataFrame) and not self.df.empty:
            self.lst = self.localDF(self.df)  # lst_n, lst_ed
            self.out_graph=self.task_by_level(self.lst[0],mode)
        else:
            self.lst=([],[])
            self.out_graph=[]

        self.res = (self.out_graph, self.lst[1])
        
        


    def task_from_df(self,df):
        out=df.to_dict('records')
        for row in out:
            task=Task(row)
            self.tasknodes.append(task)
    
    def set_dict_task(self):
        self.dict_tasks=dict([(t.name,t) for t in self.tasknodes])
        return self.dict_tasks
    
    def localDF(self,df=''):
        
        
        if not df.empty:
            df=self.df
        else:
            self.df=df
        self.df.sort_values(by=["дата", "время"],ascending=True)
        self.df.set_index(["дата", "время"])
        self.cy_nodes=[]
        self.cy_edges=[]
        for i, row in self.df.iterrows():
            name=row['name']
            name1=row['связанные задания']
            if  not name in self.dict_tasks.keys():
                task=Task(row)
                self.dict_tasks[name]=task
                t_source={"data": {'par':str(task.source_dep),"id":str(task.name), "label": '', "timerange":task.data_delta, 'start_data':task.start_data, 'node_color':get_color(task.data_delta), },'classes':'task'}
                self.cy_nodes.append(t_source)
            if not name1 in self.dict_tasks.keys():
                task=Task(row)
                self.dict_tasks[name]=task
                t_source={"data": {'par':str(task.source_dep),"id":str(name1), "label": '', "timerange":task.data_delta,'start_data':task.start_data, 'node_color':get_color(task.data_delta), },'classes':'task'}
                self.cy_nodes.append(t_source)
        cn=0        
        for i, row in self.df.iterrows():
            name=row['name']
            name1=row['связанные задания']
            source, target, timerange, msg_type, size = name, name1, row['период решения'], row['тип'], row['решение']
            data={'data': {'id_seq':row['id_seq'], 'source': str(source),'target': str(target),'msg_type':msg_type,'size':size}}
        
            if msg_type=="запрос" :
                style='blackedge'
            elif msg_type=='ответ':
                style='edge'
            data['classes']=style
            self.cy_edges.append(data)
        
        return (self.cy_nodes, self.cy_edges)
    
    def task_by_level(self, task_nodes, mode='rect'):

        #получаем координаты для прямоугольников подразделений
        lst_tasks = []
        t_all = []
        if task_nodes:
            for n in self.nodes:
                pos = n['position']  # координаты подразделения
                RECT_WIDTH = int(n['data']['width'][:-2])
                RECT_HEIGHT = int(n['data']['height'][:-2])
                node_id = n['data']['id']
                #dict_nodes[node_id]={'level':level,'position':pos,'t_count':t_count}
		#получение списка задач из DataFrame
                t_parent = [
                    t for t in task_nodes if t['data']['par'] == node_id]
                t_count = len(t_parent)  # число задач у подразделения
                x0 = pos['x']-RECT_WIDTH/2+10
                y0 = pos['y']+RECT_HEIGHT/2
                for i in range(t_count):
                    t = t_parent[i]
                    if t:
                        x = x0+i*RECT_WIDTH/t_count
                        y = y0+8
                        #t['position']=pos
                        t['position'] = {'x': int(x), 'y': int(y)}
                        t['data']['label'] = ''
                        t['data']['shape_type'] = 'circle'
                        t['data']['width'] = '10px'
                        t['data']['height'] = '10px'
                        t['data']['node-color'] = 'red'
                        t['classes'] = 'task'
                        id = t['data']['id']
                        self.dict_tasks[id] = t
                        t_all.append(t)
            return t_all
        else:
            return []

def rename_task(filename, pref, id_seq, master, thex,step,freg):
    """
    замена в таблице задачм имен задач - добавление префикса
    @master (старое значение, новое значение) - кортеж замены для мастера
    @thex (старое значение, новое значение)  - кортеж замены для цеха
    """
    df=pd.read_excel(filename)
    dict_df=df.to_dict('records')
    for i in dict_df:
        if id_seq:
            i['id_seq']=id_seq
        if master:
            if str(i['инициатор задания'])==str(master[0]):
                i['инициатор задания']=str(master[1])
        if thex:
            if '_' in str(i['инициатор задания']):
                v=str(i['инициатор задания']).split('_')
                if v[0]==thex[0]:
                    i['инициатор задания']=thex[1]+'_'+v[1]
            elif str(i['инициатор задания'])==thex[0]:
                i['инициатор задания']=thex[1]

        if pref:
            i['name']=pref+'_'+str(i['name'])
            i['связанные задания']=pref+'_'+str(i['связанные задания'])
    df_out=pd.DataFrame(dict_df)
    return df_out




def generate_total_df(params):
    """
    Создается DataFrame для набора задач из списка задач

    """
    lst_out = []
    lst_out1=[]
    lst=[]

    for par in params:
        df_tmp = rename_task(**par)
        lst_out.append((par['filename'],df_tmp, par['step'], par['freg']))
    for i in lst_out:
        d={}
        item=i[1]
        delta=i[2]
        freg=i[3]
        if freg=='D':
            item.loc[:, 'дата'] = pd.to_datetime(item['дата'].astype(str)+' '+item['время'].astype(str)) + timedelta(days = delta)
        elif freg=='M':
            item.loc[:, 'дата'] = pd.to_datetime(item['дата'].astype(str)+' '+item['время'].astype(str)) + timedelta(days=30*delta)
        else:
            item.loc[:, 'дата'] = pd.to_datetime(item['дата'].astype(str)+' '+item['время'].astype(str))
        item.sort_values(by=["дата"], inplace=True)
        item.set_index(["дата"])
        item.shift(periods=delta, freq=freg,axis=1)
        d['name']=i[0]
        d['min']=min(item['дата'].astype(str))
        d['max']=max(item['дата'].astype(str))
        lst.append(d)
        #print(i[0], '   ',min(item['дата'].astype(str)),'   ',max(item['дата'].astype(str)))
        lst_out1.append(item)
    tmp=pd.DataFrame(lst)
    tmp.sort_values(by=["min"], inplace=True)
    tmp.set_index(["min"])
    
    df = pd.concat(objs=lst_out1)
    df.loc[:, 'дата'] = pd.to_datetime(df['дата'].astype(str)+' '+df['время'].astype(str))
    df.sort_values(by=["дата"], inplace=True)
    df.set_index(["дата"])
    return df


def df_to_excel(d1):
    '''
    записывает список словарей d1 в excel книгу с именем filename
    '''
    df1=pd.DataFrame(d1, filename )
    # create excel writer object 
    writer = pd.ExcelWriter(filename) # write dataframe to excel
    df1.to_excel(writer) 
    # save the excel 
    writer.save()



