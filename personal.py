
from RestApi.get_data import *

import requests
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask import Flask, request   
from RestApi.utility import*
from RestApi.get_data import*
from graph_component import *
from formlib import *
from form_class import *
from Graph import *
from tabletools import *
from dash.exceptions import PreventUpdate
from callback import *
from service_utility import*


colors = ['#ffcc00', 
          '#f5f2e8', 
          '#f8f3e3',
          '#ffffff', 
          ]
base_url='http://ontogovorun.ru'
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_host=HostInfo(base_url,target_login, target_passw)
agent=JsonData(target_host)
#agent=RestManager(url=base_url)

def query_example(id_user):
    #base_url='http://localhost:8080/Plone/'
    #agent=JsonData(base_url)
    #items_lst=subclases_list(agent,'Подразделение')
    #options_data=[i['title'] for i in items_lst] 
    gui=[]

    if id_user:
        dolgn=agent.get_children(id_user)
        
        dolgn_title=html.H3(dolgn['baseclass']['title'])
        oprops=dolgn['oproperty']
        print('oprops',oprops)
        
        for p in oprops:
            if p['title']=='сотрудник':
                sotr=p
                break
        #gui.append({'title':sotr['title'],'uid':sotr['uid']})
        """
        gui.append(title)
        df_props=pd.DataFrame(oprops)
        for i in df_props.iloc:
            gui.append(prop_present(i))
        """
      
        
    else:
        html.H3('Не найден')
        gui.append(title)
    
    owner_div=html.Div(id='owner_div', children=gui)
    info_option=html.Div([dolgn_title,html.Br(),range_title_present({'title':sotr['title'],'uid':sotr['uid']})])
    #html.Div(id='person_div',children=prop_present({'title':sotr['title'],'uid':sotr['uid']}))

    d1=[{'field_name':'category_task','range_class':u'Раздел', 'label' :u'Раздел'},
        {'field_name':'type_task','range_class':'Тип задания', 'label' :'Тип задания'},
        {'field_name':'priority','range_class':'Приоритет срочности', 'label' :'Приоритет срочности'},
        {'field_name':'task_agent','range_class':'Должность', 'label' :'Исполнитель'},
        #{'field_name':'task_status','range_class':'Статус решения', 'label' :'Статус решения'},
        #{'field_name':'task_period','range_class':'Период решения', 'label' :'Период решения'},
        ]

    data={}
    lst_dropbox=[]
    for v in d1:
        options_data=[]
        values=get_source(agent,v['range_class'])
        options_data=[item['title'] for item in values['subclass']+values['submetaclass']]
        if options_data:
            value=options_data[0]
        else:
            value=''
        if v['field_name']=='task_agent':
            agbox=(dbc.Label(v['label'], html_for=v['field_name']),
            dcc.Dropdown(id=v['field_name']+'_dropdown',
                options=options_data,
                optionHeight=35,                    #height/space between dropdown options
                value=value,                    #dropdown value selected automatically when page loads
                disabled=False,                     #disable dropdown value selection
                multi=False,                        #allow multiple dropdown values to be selected
                searchable=True,                    #allow user-searching of dropdown values
                search_value='',                    #remembers the value searched in dropdown
                placeholder='Please select...',     #gray, default text shown when no option is selected
                clearable=True,                     #allow user to removes the selected value
                style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
                # className='select_box',           #activate separate CSS document in assets folder
                # persistence=True,                 #remembers dropdown value. Used with persistence_type
                # persistence_type='memory'         #remembers dropdown value selected until...
                ),                                  #'memory': browser tab is refreshed
                                                    #'session': browser tab is closed
                                                    #'local': browser cookies are deleted
            )
        else:


            dpbox=(dbc.Label(v['label'], html_for=v['field_name']),
                dcc.Dropdown(id=v['field_name']+'_dropdown',
                    options=options_data,
                    optionHeight=35,                    #height/space between dropdown options
                    value=value,                    #dropdown value selected automatically when page loads
                    disabled=False,                     #disable dropdown value selection
                    multi=False,                        #allow multiple dropdown values to be selected
                    searchable=True,                    #allow user-searching of dropdown values
                    search_value='',                    #remembers the value searched in dropdown
                    placeholder='Please select...',     #gray, default text shown when no option is selected
                    clearable=True,                     #allow user to removes the selected value
                    style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
                    # className='select_box',           #activate separate CSS document in assets folder
                    # persistence=True,                 #remembers dropdown value. Used with persistence_type
                    # persistence_type='memory'         #remembers dropdown value selected until...
                    ),                                  #'memory': browser tab is refreshed
                                                        #'session': browser tab is closed
                                                        #'local': browser cookies are deleted
            )
            lst_dropbox.append(dpbox)   
        
    


    

    #label_task=dbc.Row([dbc.Col(dbc.Label("Вопрос", html_for="dep-input", width=2))])
    label_task=dbc.Label("Вопрос", html_for="task_name")
    """
    field_task = dbc.Row(
                        [dbc.Col(
                            dbc.Input(
                                type="text", id="task_name", placeholder="Ввод вопросв"),
                                width=10,
                                ),
                        ]) 
    """
    field_task = dbc.Input(type="text", id="task_name", placeholder="Ввод вопросв"),
                       
    task_option=dbc.Row([dbc.Col(id='task_div',children=lst_dropbox,width=8)])
    #agent_option=html.Div(id='agent_div', children=[agbox])
    """
    layout=dbc.Container(id='view_div', children=[
        dbc.Row([dbc.Col(info_option, width=12)]),
        ])
    
    layout=dbc.Container(id='view_div', children=[
        dbc.Row([dbc.Col(info_option, width=12)]),

        dbc.Row(
            [dbc.Col([label_task,field_task,task_option], width=8),
            dbc.Col(agent_option, width=4)])
        ])
    """


    active_task=dcc.Dropdown(id='parent_task_fiwld',
                    options=[],
                    optionHeight=35,                    #height/space between dropdown options
                    value=value,                    #dropdown value selected automatically when page loads
                    disabled=False,                     #disable dropdown value selection
                    multi=False,                        #allow multiple dropdown values to be selected
                    searchable=True,                    #allow user-searching of dropdown values
                    search_value='',                    #remembers the value searched in dropdown
                    placeholder='Please select...',     #gray, default text shown when no option is selected
                    clearable=True,                     #allow user to removes the selected value
                    style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
                    )
    #########################################################       
    # форма выбора текущей задачи
    #########################################################
    tabs_styles = {"height": "30px", "width": "80%", "display": "inline-block"}
    tab_style={"height": "25px"}
    selecttab_style={"height": "25px"}
    parent_task_blk=dbc.Container(
         
        [
            dbc.Row([dbc.Col(html.H4('Текущая задача'))]),
            dbc.Row([dbc.Col(
                dcc.Tabs(id='tabs', value='Tab1', children=[
                    dcc.Tab(label='Входящие', id='tab1', value='Tab1', children =[],style=tab_style, selected_style=selecttab_style),
                    dcc.Tab(label='В работе', id='tab2', value='Tab2', children=[],style=tab_style, selected_style=selecttab_style),
                    dcc.Tab(label='Выполненные', id='tab3', value='Tab3', children=[],style=tab_style, selected_style=selecttab_style),
                ], parent_style=tabs_styles)
               )]),
            
            dbc.Row([dbc.Col(active_task)]),
        ]
        )
    new_task_header=dbc.Container(
        [
            dbc.Row([dbc.Col(html.H4('Новая задача'))]),
            
        ]
        )

    task_block = [dbc.Col(label_task, width=6),dbc.Col(field_task,width=6)]
   
    select_block=[dbc.Row([dbc.Col(wgt[0],width=6 ),dbc.Col(wgt[1],width=6 )], className='form-group' ) for wgt in  lst_dropbox]
    ag_block=[dbc.Row([dbc.Col(agbox[0],width=4),dbc.Col(agbox[1],width=8)])]  
    button_field = [dbc.Row([
            dbc.Col(
                dbc.Button("Submit", id='submit-button', color="primary", className="ms-auto", n_clicks=0),
                width=10,
            )   ,
            ],
        className="mb-3",
        )] 
    mess_field = dbc.Row([
        dbc.Col(
                html.Div(id='mess_field', children=[]),
                width=10,
               ),
        ],
        className="mb-3",
        ) 
    
    task_form =  dbc.Form([parent_task_blk, new_task_header, dbc.Container(id='view_div', children=[dbc.Row(task_block, className="form-group form-outline")]+select_block+ag_block+button_field)])

    logo = html.Img(src=app.get_asset_url('logo.png'),
                            style={'width': "128px", 'height': "128px",
                            }, className='inline-image')
    header = info_option
    #html.H3("Статистика российских пивоварен в Untappd", style={'text-transform': "uppercase"})
    """
    top=dbc.Container(
        dbc.Row([
            dbc.Col(logo),
            dbc.Col(header)],
                style={'max-height': '128px',
                'color': 'white',
                'wight':'100%'
                      }
        ),
        className='d-flex justify-content-center',
        style={'max-width': '100%',
               'background-color': colors[0]},
        )
    """
    top=dbc.Container(id='top_div', children=[
        dbc.Row([dbc.Col(header, width=12)])],
            style={'max-height': '128px',
                'color': 'red',
                'align':'center',
                'wight':'100%'
                  })  
    
    
    
    playout = html.Div(
                        [top,
                        dbc.Container(       
                                html.Div(
                                    [
                            
                                      task_form
                            
                                    ],
                                ),
                                fluid=False, style={'max-width': '1300px'},
                            ),
                        ],
                        style={'background-color': colors[1], 'font-family': 'Proxima Nova Bold'},
                    )
    return playout



 

def subclases_list(agent,nameclass):
    #base_url='http://localhost:8080/Plone/'
    #agent=JsonData(base_url) 
    data=get_source(agent,nameclass)
    print('data',data)
    
    out= data['submetaclass']
    
    return out
######################################################################################################
# Функции, создающие компоненты презентации                                                          #
##################################################################################################### 
def prop_present(prop):
    """_summary_

    Args:
        prop (DattaFrameRow): строка DataFrame_
    """
    i=prop
    title=i['title']
    uid=i['uid']
    
    range=agent.get_range_by_uid(i['uid'])
    #print('range',range)
    range_title=range.title
    #print('prop',range.props)
    out=html.Div(id=uid+'_div', children=[html.P(title+': '+range_title, style={'color': 'blue', 'fontSize': 14})])
    return out

def range_title_present(prop):
    """_summary_

    Args:
        prop (DattaFrameRow): строка DataFrame_
    """
    i=prop
    title=i['title']
    uid=i['uid']
    
    range=agent.get_range_by_uid(i['uid'])
    #print('range',range)
    range_title=range.title
    #print('prop',range.props)
    out=html.H3(range_title)
    return out