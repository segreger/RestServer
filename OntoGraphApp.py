import dash
from dash import html
from dash import dcc
import dash_cytoscape as cyto
from Graph import *
from tabletools import *
from OntoGraph import *

gr=OntoGraphTitle(target_mng,'Должность')


elements=gr.elements()
app = dash.Dash(__name__)
"""
style_rec={ 'width': '100%',
            'height': '400px',
            'content': 'data(title)',
            'labelValig': "middle",
            'shape':'rectangle',
            "border-color": "gray",
            "border-width": "1",
            "text-valign" : "center",
            "text-halign" : "center",
            'font-size':'14px',
            "background-color":'red',
            'padding': 1,
            'text-wrap': 'wrap',
            "text-max-width": 200,
            'color':'white',
            }
      
"""
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



app.layout=html.Div([
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
    ],

    )
#breadthfirst
if __name__ == '__main__':
    app.run_server(debug=True)
