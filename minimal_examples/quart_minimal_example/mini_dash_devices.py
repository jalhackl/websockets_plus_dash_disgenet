import dash_devices 
from dash_devices.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from threading import Timer

import dash_cytoscape as cyto
import json


app = dash_devices.Dash(__name__)

default_stylesheet = [
    {
        "selector": "node",
        "style": {
           
           "height": "data(size)",
           "width": "data(size)",
           'background-color': "data(color)",
           "border-color": "data(color)",
            "content": "data(label)",
            "font-size": "12px",
            "text-valign": "center",
            "text-halign": "center",
        }
    }
]

class Example:
    def __init__(self, app):
        self.app = app
        
        global default_stylesheet
       
        
        self.count = 0

        self.elements=[
            {'data': {'id': 'one', 'label': 'Node 1', 'color': 'green'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2','color': 'red'}, 'position': {'x': 200, 'y': 200}},
             {'data': {'id': 'three', 'label': 'Node 3','color': 'red'}, 'position': {'x': 100, 'y': 150}},
               {'data': {'id': 'four', 'label': 'Node 4','color': 'green'}, 'position': {'x': 133, 'y': 74}},
                 {'data': {'id': 'five', 'label': 'Node 4','color': 'yellow'}, 'position': {'x': 74, 'y': 100}},
            {'data': {'source': 'one', 'target': 'two'}},
            {'data': {'source': 'one', 'target': 'three'}},
             {'data': {'source': 'one', 'target': 'four'}},
             {'data': {'source': 'three', 'target': 'four'}},
             {'data': {'source': 'two', 'target': 'five'}},
        ]

        self.app.layout = html.Div([

	 cyto.Cytoscape(
        id='cytoscapenetw',
        style={'width': '60%', 'height': '600px'},
        elements=self.elements,
        layout={
            'name': 'preset'
        }
         ,stylesheet=default_stylesheet
    ),
        ])


        @self.app.callback(None, [Input('cytoscapenetw', 'tapNode')],[State('cytoscapenetw', 'elements')])
        def funcgraph(tapdata, elementsn):
      

            for el in elementsn:
                print(el['data']['id'])
                if "color" in el['data']:
                  
                    if el['data']['id'] == tapdata['data']['id']:
                        if el['data']['color'] == 'red':
                            el['data']['color'] = 'green'
                        elif el['data']['color'] == 'green':
                            el['data']['color'] = 'yellow'
                        elif el['data']['color'] == 'yellow':
                            el['data']['color'] = 'red'

           

            self.app.push_mods({
                'cytoscapenetw': {'elements': elementsn}
            })
            return None


       
        


if __name__ == '__main__':
    Example(app)
    #app.run_server(debug=True, host='0.0.0.0', port=5000)
    app.run_server()