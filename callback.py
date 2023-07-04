import pdb
import dash
import requests 
from dash import html
from dash import dcc
#import dash_table_experiments as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import callback_context, State, html
import dash_cytoscape as cyto
from RestApi.utility import*
from RestApi.get_data import*
from graph_component import *
from formlib import *
from form_class import *
from Graph import *
from tabletools import *
@app.callback(
    Output("modal3_1", "is_open"),
    [Input('graph', 'tapNodeData')],
    [State("modal3_1", "is_open")],
    )
def toggle_modal3_1(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output(component_id='sub-value', component_property='children'),
    [Input('struct_cytoscape', 'tapNodeData')])
def set_sub(value):
    if isinstance(value,dict):
        print('sub=',value)
        s0 = value['label']
        print('s0=',s0)
        return s0
    else:
        return 'None sub'



#Создает сообщение в всплывающем окне при выборе подразделения
"""
@app.callback(
    Output(component_id='Modal_setsub', component_property='children'),
    [Input('select-mode', 'value'),
     Input(component_id='sub-value', component_property='children'),],prevent_initial_call=True,
    )
"""
@app.callback(
    Output(component_id='form_div', component_property='children'),
    [Input('select-mode', 'value'),
     Input(component_id='sub-value', component_property='children'),],prevent_initial_call=True,
    )

def get_sub(mode, baseclass):
    print('mode',mode)
    print('baseclass',baseclass)
    if mode:
        return form_class()
    else:
        return ''

@callback(
    Output(component_id="mess_field", component_property="children"),
    [   Input("submit_button", "n_clicks"),
        Input(component_id="sub_value", component_property="children"),
        Input('select_mode', 'value'),
        Input("dep_input", "value"),
        Input("desc_input", "value"),
    ],prevent_initial_call=True, suppress_callback_exceptions=True)


def toggle_modal1(submit_clicks,sub_value,baseclass,title, desc):
    if not submit_clicks:
        raise PreventUpdate
    print('sub_value',sub_value)
    agent=JsonData('http://localhost:8080/Plone/')
    classname='Подразделение'
    data=get_source(agent,baseclass)
    context_uid=data['baseclass']['uid']
    
    #container_uid=data['ontology'][0]['uid']
    container=agent.get_ontoitem('DextOntology','Библиотека подразделений')
    container_uid=container['uid']
    
    indata={'selonto':container_uid,'context_uid':context_uid,'title':title,'desc':desc,'meta':'subclass','out_kind':'','reponto_uid':container_uid}
    agent.create_subclass(indata)
    #plone_subclass(agent,context_uid,container_uid,title,desc)
    
    change_class_property1(agent,'DextOntoClass', title , 'hasMetatype', classname)

    
    target_name=sub_value
    #установка подчиненности
    target_data=agent.get_class_by_name(target_name)
    target_url=target_data['url']
    base=[{'@id':target_url}]#получили инормацию для range связи
    
    source=get_source(agent,title)
    source_url=source['baseclass']['url']
    #target=dict_class[d['target_title']]
    #target=container_uid
    prop=get_class_prop(source_url,'подчиненность')
    print('prop_url',prop['@id'])
    print('target_url',target_url)
    base=[{'@id':target_url}]
    #print(source.title, target.title, prop['@id'])
    requests.patch(prop['@id'], headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'range':target_url }, auth=('admin', 'admin'))
    
    return 'Successfully submitted.'


