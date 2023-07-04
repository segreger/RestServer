from RestApi.get_data import *

import requests 
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
desc_input=dcc.Textarea(
                id='desc_input',
                value='Textarea content initialized\nwith multiple lines of text',
                style={'width': '100%', 'height': 300},
            ),
def form_class():
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
    
    form = dbc.Form([title_field,descript_field,level_field,shotname_field, button_field,mess_field])
    
    return form  
