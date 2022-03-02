import dash_devices
import dash_html_components as html
import dash_core_components as dcc

import dash_cytoscape as cyto

from dash_devices.dependencies import Input, Output, State


import json

elements=[
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]

app = dash_devices.Dash(__name__)
app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    dcc.Slider(id="scorethresholdslider", min=0, max=1, step = 0.05, value=0.6, 
               marks={0: '0', 1: '1'}),
    html.Div(id='thresh'),
    dcc.RadioItems(
    id='cytographlayout',
    options=[

        {'label': 'preset', 'value': 'preset'},
        {'label': 'circle', 'value': 'circle'},
        {'label': 'cose', 'value': 'cose'},
    ],
    value='preset'
    ),
    html.Button('Share Graph 1', id='sharecyto', n_clicks_timestamp=0),
    html.Button('Share Graph 2', id='sharecyto2', n_clicks_timestamp=0),
    cyto.Cytoscape(
        id='cytoscapenetw',
        style={'width': '60%', 'height': '600px'},
        elements=elements,
        layout={
            'name': 'circle'
        }
    ),
     html.P(id='placeholder1'),
     html.Div(id='placeholder2'),
    dcc.Store(id='cytostore', data = json.dumps(elements)),
    dcc.Textarea(
        id='cytostoretext',
        value="start",
        style={'width': '100%', 'height': 100},
    ),
])


@app.callback_shared([Output('placeholder2', 'children'),
            Output('cytostore', 'data')],
              [Input('sharecyto2', 'n_clicks_timestamp')],
              [State('cytoscapenetw', 'elements'),
              State('cytoscapenetw', 'tapNode')]
              )
def othergraph(sharebutton, elementsn, tapnode):
        print(json.dumps(elementsn))
        return html.Div([

    cyto.Cytoscape(
        id='cytoscapenetw2',
        style={'width': '50%', 'height': '600px'},
        elements=elementsn,
        layout={
            'name': 'preset'
        }
    ),
        html.Hr(), 
     
    ]), json.dumps(elementsn)





@app.callback_shared(
  

    Output('cytoscapenetw', 'elements'),
    
   [
    Input('sharecyto', 'n_clicks_timestamp')],
              [State('cytoscapenetw', 'elements'),
              State('cytoscapenetw', 'tapNode')]
              )

def set_elements2( sharebutton, elem, tapdata):

    global elements

    if tapdata != None:
        for i in elem:
         
            if "data" in i:
                if "id" in i['data']:
                    if i['data']['id'] == tapdata['data']['id']:
                        i['position']['x']=tapdata['position']['x']
                        i['position']['y']=tapdata['position']['y']
    
    elements = elem
   
    return elem



#callback for choosing score-threshold (for disgenenet-file)
@app.callback_shared(Output('thresh', 'children'),
              [Input('scorethresholdslider', 'value')])
def change_scorethreshold(val):
    global scorethreshold
    scorethreshold = val
    return scorethreshold


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)