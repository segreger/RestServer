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
#from formlib import *
#from form_class import *
from Graph import *
from DepGraph import *
from tabletools import *
from dash.exceptions import PreventUpdate
from callback import *


#модальное окно для данных о подразделении из отдела продаж
#появляется при наведении указателя на подразделение
#form=select_nswsub()
desc_input=dcc.Textarea(
                id='desc_input',
                value='Textarea content initialized\nwith multiple lines of text',
                style={'width': '100%', 'height': 300},
            ),

title_field = dbc.Row(
    [
        dbc.Label("Наименование подразделения", html_for="dep-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="dep-input", placeholder="Enter title"
            ),
            width=10,
        ),
    ],
    className="mb-3",
    )    
descript_field = dbc.Row(
    [
        dbc.Label("Описание подразделения", html_for="desc-input", width=2),
        dbc.Col(desc_input,width=10,),
    ],
    className="mb-3",
    ) 
level_field = dbc.Row(
    [
        dbc.Label("Уровень управления", html_for="level-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="level-input", placeholder="Enter title"
            ),
            width=10,
        ),
    ],
    className="mb-3",
    )
shotname_field = dbc.Row(
    [
        dbc.Label("краткое имя", html_for="shotname", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="shotname", placeholder="Enter title"
            ),
            width=10,
        ),
    ],
    className="mb-3",
    )





button_field = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Submit", id='submit-button', color="primary", className="ms-auto", n_clicks=0),
            width=10,
        ),
    ],
    className="mb-3",
    )  

mess_field = dbc.Row(
    [
        dbc.Col(
            html.Div(id='mess_field', children=[]),
            width=10,
        ),
    ],
    className="mb-3",
    )   
    
form_dep= dbc.Form([title_field,descript_field,level_field,shotname_field, button_field,mess_field])




dep_input = dbc.Row(
    [
        dbc.Label("Подразделение", html_for="dep_input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="sel_input", placeholder="Enter email"
            ),
            width=10,
        ),
    ],
    className="mb-3",
    )


radios_input = dbc.Row(
    [
        dbc.Label("Создать", html_for="select_mode", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="select_mode",
                options=[
                    {"label": "Подразделение", "value": "Подразделение"},
                    {"label": "Должность", "value": "Должность"},
                ],
            ),
            width=10,
        ),
    ],
    className="mb-3",
    )

form_div = dbc.Row(
    [
        dbc.Col(
            html.Div(id='form_div',children=[]),
            width=10,
        ),
    ],
    className="mb-3",
    )
form_sub = dbc.Row(
    [
        dbc.Col(
            html.Div(id='sub_value',children=[]),
            width=10,
        ),
    ],
    className="mb-3",
    )
form_select = dbc.Form([form_sub, radios_input, form_div])


form_div_select=html.Div(id='form_div_select', children=[form])
form_div1=html.Div(id='form_div1', children=[form_dep])
form_div2=html.Div(id='form_div2', children=[form_dep])
form_div=html.Div(id='form_div0', children=[form_div_select,form_div1,form_div2])
modal3_1=dbc.Modal(
            [
                dbc.ModalHeader(),
                dbc.ModalBody(id='ModalBody3_1',children=[form]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close3_1", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal3_1",
            is_open=False,
            size="lg",
        )

filename='RestApi/data/Доработанные таблицы.xlsx'
collist=['Подразделение', 'Наименование подразделения','Подчиненность']
sheet_name='Структура предприятия'
df=pd.read_excel(filename,sheet_name)
for col in collist:
    df[col] = df[col].astype('string')
    df[col] = df[col].str.strip()
df['Родитель'] = [x.split('.')[0] if len(x.split('.'))==2 and x.split('.')[-1]=='0' else x for x in df['Подчиненность']]
df=table_encode(df,collist)
df['Тип'] = ['служба' if 'Служба' in x else 'подразделение' for x in df['Наименование подразделения']]

g=DepGraph(df,'Подразделение', 'Наименование подразделения','Родитель','Тип')

elements=g.elements()

style_rec=[{ 
            'selector':'node',
            'style':{
                'content': 'data(label)',
                'color':'white',
            },
            }
          ]

wrap_line=[{
            "selector": ".multiline-auto",
            "style":{
                   'content': 'data(label)',
                   'labelValig': "middle",
                   'shape':'rectangle',
                   "width": "mapData(size, 0, 200, 20, 60)",
                   "height": "mapData(size, 0, 100, 20, 60)",
                   "border-color": "gray",
                   "border-width": "1",
                   "text-valign" : "center",
                   "text-halign" : "center",
                   'font-size':'20px',
                   "background-color":'white',
                   'padding': 1,
                   'text-wrap': 'wrap',
                    "text-max-width": 400
                    }
          }]          

wrap_line1=[{
            "selector": ".multiline-auto",
            "style":{
                   'content': 'data(label)',
                   'labelValig': "middle",
                   'shape':'rectangle',
                   'width': 450,
                   'height': 200,
                   "border-color": "black",
                   "border-width": 4,
                   "text-valign" : "center",
                   "text-halign" : "center",
                   'font-size':'30px',
                   "background-color":'white',
                   'padding': '1px',
                   'text-wrap': 'wrap',
                    "text-max-width": 350,
                    'color':'black',
                    }
          }]




default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "width": "mapData(size, 0, 200, 20, 60)",
            "height": "mapData(size, 0, 100, 20, 60)",
            "content": "data(label)",
            "font-size": "14px",
            "text-valign": "center",
            "text-halign": "center",
            'shape':'rectangle',
        }
    }
]


struct_layout=html.Div([
        cyto.Cytoscape(
            id='graph',
            elements=elements,
            boxSelectionEnabled=False,
            autounselectify=True,
            layout={
                    'name': 'breadthfirst',
                    'roots': '[id = "1"]'
                   },
            stylesheet=wrap_line1,
            
            style={
                   'width': '100%',
                   'height': '1000px',
                   'background-color': 'white',
                   'padding': 0,
                  },
        ),
        modal3_1,
        form_div,
        form_div_select,
        form_div1,
        form_div2,
        dep_input,

    ],
    )


