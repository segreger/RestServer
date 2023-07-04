# -*- coding: utf-8 -*-
from RestApi.get_data import *

import requests 
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from dash.exceptions import PreventUpdate
from form_class import *
#form_sub=form_class()
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
form = dbc.Form([form_sub, radios_input, form_div])

def select_nswsub():

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
    form = dbc.Form([form_sub, radios_input, form_div])
    return form
