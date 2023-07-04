import dash
from dash import html
from dash import dcc
#import dash_table_experiments as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import callback_context, State, html
import dash_cytoscape as cyto
from utility.utility import*
from assets.styles import *
from utility.task_generate import *

import copy
import pandas as pd
import numpy as np
from datetime import datetime as dt




def graph_div(elements,id_graph,id_timer, interval=100):
    """Возващает Cytoscape с графом из elements и id = id_graph  и таймер с id = id_timer"""
    #styesheet=[markedge_style, edge_style, edge_black_style,deledge_style, task_style,task_mark_style, wrap_line,dep_edge_style, ]

    graph1 = html.Div([
        cyto.Cytoscape(
            id=id_graph,
            elements=elements,
            boxSelectionEnabled=False,
            autounselectify=True,
            layout={
                'name': 'preset',
                'padding': 1
            },
            stylesheet=BASE_STYLELIST,
            style={
                'width': '100%',
                'height': '75vh',
                'background-color': 'white', 
                'padding': 0,
            }
        ),
    ],

    )
    graph_div= html.Div([
        html.Div([
        graph1,
        dcc.Interval(id=id_timer, interval=interval, n_intervals=0, disabled=False),
        ], 
        ),
    ])
    return graph_div


def graph_div1(elements,id_graph,stylelist):
    """Возващает Cytoscape с графом из elements, id = id_graph и списком стилей stylelist"""
    graph1 = html.Div([
        cyto.Cytoscape(
            id=id_graph,
            elements=elements,
            boxSelectionEnabled=False,
            autounselectify=True,
            layout={
                'name': 'preset',
                'padding': 1
            },
            stylesheet=stylelist,
            style={
                'width': '100%',
                'height': '80vh',
                'background-color': 'white', 
                'padding': 0,
            }
        ),
    ],

    )



    graph_div= html.Div([
        html.Div([
        graph1,
        ], 
        ),
    ])
    return graph_div
