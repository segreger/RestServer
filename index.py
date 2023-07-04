
import dash

from dash import html
from dash import dcc
#import dash_table_experiments as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import callback_context, State, html
import dash_cytoscape as cyto
from flask import request 
from utility.utility import*
from app import app
from app import server
from struct_view import struct_layout
from personal import *


app.layout = html.Div([
    dcc.Location(id='url', refresh=True),

    html.Div(id='page-content')
])

page_container = html.Div(
    children=[
        # represents the URL bar, doesn't render anything
        dcc.Location(
            id='url',
            refresh=False,
        ),
        # content will be rendered in this element
        html.Div(id='page-content')
    ]
)### Index Page Layout ###
index_layout = html.Div(
    children=[
        dcc.Link(
            children='Go to Page 1',
            href='/struct_view',
        ),
        html.Br(),

    ]
)



"""
@app.callback(
     output=Output(component_id='var1', component_property='children'),
     inputs=[Input(component_id='url', component_property='pathname')])
def update_location_on_page(pathname):
     return pathname

@app.callback(
     output=Output(component_id='var2', component_property='children'),
     inputs=[Input(component_id='url', component_property='hash')])
def update_location_on_page(hash_val):
     if hash_val is None:
          return ''
     return hash_val
"""
@app.callback(
     output=Output(component_id='page-content', component_property='children'),
     inputs=[Input(component_id='url', component_property='pathname'),
             Input(component_id='url', component_property='search')])
def display_page(pathname, search):
     print(pathname)
     if pathname=='/personal' :
          if search:
               id_user=search.split('=')[-1]
               print(id_user)
               return query_example(id_user)
     elif pathname == '/struct_view':
          return struct_layout
     else:
          return struct_layout

"""
def update_location_on_page(partname, search):
     print(p,search)
     if search is None:
          return ''
     return search

@app.callback(Output('page-content', 'children'),
              [Input('url', 'search')])
def display_var(var):
     print(request.full_path, request.base_url, request.url)
     print(var)
     return var

@app.callback(Output('page-content', 'children'),
              [Input('url', 'partname')])
def display_page(partname, search):
     print(pathname)
     if pathname=='/personal' :
          return personal_layout
     elif pathname == '/apps/struct_view':
          return struct_layout
     else:
          return struct_layout
"""
if __name__ == '__main__':
    app.run_server(debug=True,host="127.0.0.1", port=8050, threaded=True)
