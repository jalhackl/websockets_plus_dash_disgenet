from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
import requests
import json
from engineio.payload import Payload

import string
import random

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from dash import Dash
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import flask

import plotly.express as px
import pandas as pd



Payload.max_decode_packets = 50

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def sendUE4(adress, data):
    # The POST request to our node server
    res = requests.post('http://127.0.0.1:3000/in', json=data)
    #return
    # Convert response data to json
    #returned_data = res.json() 
    #print(returned_data)

idata = {'mes': 'dfhdfhfh', 'usr': 'NaS7QA89nxLg9nKQAAAn', 'tag': 'flask'}

scb1Data = [
  {"msg": "TMP", "id": '#button1'},
  {"msg": "MMU", "id": '#button2'},
  {"msg": "PAM", "id": '#button3'},
  {"msg": "CHR", "id": '#button3'},
  {"msg": "OMG", "id": '#button3'},
  {"msg": "WTF", "id": '#button3'},
  {"msg": "HH2H", "id": '#button3'},
  {"msg": "ASS1", "id": '#button3'}
]
pairs = [("a", "1"), ("b", "2"), ("c", "3")]
sliders = [("ddfd", "1"), ("bfsd", "2"), ("cdfsdf", "3")]

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

#create dash_app
dash_app = Dash(__name__, server = app, url_base_pathname='/dashboard/' )



import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


#route for dash
@app.route('/dashboard')
def render_dashboard():
    return flask.redirect('/dash1')


#socketio = SocketIO(app, manage_session=False)



#creating wsgi_app containing flask and dash
from werkzeug.exceptions import NotFound
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
   # '/' : app,
   "/prefix": app,
    '/dash1': dash_app.server,
   # '/dash2': dash_app2.server
})


Session(app)
socketio = SocketIO(app, manage_session=False)


###RECEIVE INCOMING WEBSOCKET MSG FROM NODE.JS 
@app.route('/flask', methods=['GET', 'POST'])
def wsreceiver():
    if request.method == 'POST':
        data =request.get_json()
    else:
        data = request.args

    global idata

    idata = data
    print(bcolors.WARNING + data['usr']  + "says: " + data['mes'] + bcolors.ENDC)

    outstr = data['usr'] +' : ' + data['mes']
### Multicast to connected web clients (not UE4!)
    socketio.emit('message', {'msg': outstr}, namespace = '/chat' , room='1')

### Send it back to node wich multicasts it to ue4 clients
    sendUE4('http://127.0.0.1:3000/in', data)

    return



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):

        
        username = request.form['username'] 
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            session['username'] = 'reee'
            session['room'] = '2'
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))


@app.route('/Test')
def test():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"


@app.route('/Test1')
def test1():
    
    return render_template('gene-element.html')


@app.route('/Test2')
def test2():
    
    return render_template('scroll.html', data = scb1Data)

@app.route('/Test3')
def test3():
    
    return render_template('test.html')

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    #print(bcolors.WARNING + session.get('username') + ' has entered the room.' + bcolors.ENDC)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    print(bcolors.WARNING + session.get('username') + "says: " + message['msg'] + bcolors.ENDC)
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)
    sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})

@socketio.on('ex', namespace='/chat')
def ex(message):
    room = session.get('room')
    #print(bcolors.WARNING + session.get('username') + "ex: " + json.dumps(message) + bcolors.ENDC)
    if message['fn'] == 'mkB':

        global scb1Data
        scb1Data.append({'id': message['id'], 'msg': message['msg'] })
        print('add to server' + message['msg'] + ' ' + message['id'] )
    
    emit('ex', message, room=room)
    #sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})

@socketio.on('test', namespace='/chat')
def test(message):
    #room = session.get('room')
    print(bcolors.WARNING + session.get('username') + "says: " + message['msg'] + bcolors.ENDC)
    #emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)
    #sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})

@socketio.on('sl1', namespace='/chat')
def test(message):
    room = session.get('room')
    #print(bcolors.WARNING + session.get('username') + "says: " + message['msg'] + bcolors.ENDC)
    emit('sl1', message , room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


@socketio.on('ds', namespace='/chat')
def ds(message):
    print("enter dashboard")
 



#Dash application code starts here

import json

import base64
import datetime
import io

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import dash_table as dt

import plotly.express as px


import pandas as pd

from additionalfunctions import *

 
#app = dash.Dash(__name__)
 
#app.config.suppress_callback_exceptions = True

scorethreshold = 0.6

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}

header_list = ["number", "abbr", "name", "function", "attr"]
header_list_nodes = header_list
dfnodes = pd.read_csv('flask_websockets_Node\input\sample_nodes1.csv', names = header_list)

header_list = ["number", "xc", "yc", "zc", "xrgb", "yrgb", "zrgb", "100", "attr"]
dflayout = pd.read_csv('flask_websockets_Node\input\sample_layout1.csv', names = header_list)

header_list = ["source", "target"]
dfedges = pd.read_csv('flask_websockets_Node\input\sample_links1.csv', names = header_list)

df = dfnodes

edges = [{'data': {'source': x, 'target': y}} for x,y in zip(dfedges.source,dfedges.target)]


#nodes = [{'data': {'id': x, 'label': y, 'size': 1}} for x,y in zip(dfnodes.number,dfnodes.abbr)]

nodes = [{'data': {'id': x, 'label': y}} for x,y in zip(dfnodes.number,dfnodes.abbr)]


coord = [{'position': {'x': x, 'y':y }} for x,y in zip( dflayout.xc * 100, dflayout.yc * 100)]

dfnodesgenes = dfnodes
dfedgesgenes = dfedges


nodescoords = []
for i in range(len(edges)):
    nodes[i].update(coord[i])

elements = nodes + edges

uploadsort = "E"

dfnodestype1 = []
dfnodestype2 = []

pickednode = []
diseaseselected = False

diseasedegrees = []
disdisdegrees= []
genegenedegrees= []



tab1 = html.Div(children=[
    html.H1(children='Dash Graph app / upload'),
 
    html.Div(className="app-header",
    children='''
       Upload files here; bipartite network, statistics and diversity-ubiquity plot are only available if a gene-disease-network is uploaded.\n
       Compatible data files are found in the input-folder. \n
       Before running the individual node statistics, a node has to be picked in the gene or the disease network.

    '''),
    

    dcc.RadioItems(
    id='sortofupload',
    options=[
        {'label': 'edgelist', 'value': 'E'},
        {'label': 'diseasenetwork', 'value': 'D'},
        {'label': 'vrnetzer: edges', 'value': 'V'},
        {'label': 'vrnetzer: nodes', 'value': 'VN'},
        {'label': 'vrnetzer: layout', 'value': 'VL'}
    ],
    value='E'
    ),

    html.P(id='placeholder1'),

    html.P("Exclude gene-disease-edges with a score below:"),
    dcc.Slider(id="scorethresholdslider", min=0, max=1, step = 0.05, value=0.6, 
               marks={0: '0', 1: '1'}),

    html.Div(id='thresh'),


    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    
        multiple=True
    ),

    html.Div(id='output-data-upload'),



    dcc.RadioItems(
    id='graphelement',
    options=[
        {'label': 'Nodes', 'value': 'N'},
        {'label': 'Edges', 'value': 'E'},
        {'label': 'full data', 'value': 'D'},
        
    ],
    value='N'
    ),
 
    dash_table.DataTable(
    id='table1',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    
)
])


default_stylesheet = [
    {
        "selector": "node",
        "style": {
           # "width": "mapData(size, 0, 100, 20, 60)",
           # "height": "mapData(size, 0, 100, 20, 60)",
           #"size": "mapData(size, 0, 100, 20, 60)",
           "height": "data(size)",
           "width": "data(size)",
           #'background-color': '#B10DC9',
           'background-color': "data(color)",
           "border-color": "data(color)",
            "content": "data(label)",
            "font-size": "12px",
            "text-valign": "center",
            "text-halign": "center",
        }
    }
]

tab2 = html.Div([
    html.H3('Gene network'),


    dcc.RadioItems(
    id='cytographlayout',
    options=[
        {'label': 'circle', 'value': 'circle'},
        {'label': 'cose', 'value': 'cose'},
      
        
    ],
    value='cose'
    ),

     html.Button('Update Graph', id='updatecyto', n_clicks_timestamp=0),
     html.H3('Coloring according to DPI value (disease pleiotropy index, indicates the number of different disease classes a gene is associated with) '),
#cytoscape element
    cyto.Cytoscape(
        id='cytoscapenetw',

        style={'width': '90vh', 'height': '90vh'},

       # style={'width': '100%', 'height': '1200px'},
        elements=elements,
        layout={
            'name': 'circle'
        },
         stylesheet=default_stylesheet
    ),
    html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre']),

  
])

#callback for choosing score-threshold (for disgenenet-file)
@dash_app.callback(Output('thresh', 'children'),
              Input('scorethresholdslider', 'value'))
def change_scorethreshold(val):
    global scorethreshold
    scorethreshold = val
    return scorethreshold

#callback for picking nodes
@dash_app.callback(Output('cytoscape-tapNodeData-json', 'children'),
              Input('cytoscapenetw', 'tapNodeData'))
def displayTapNodeData(data):
    global pickednode
    global diseaseselected
    pickednode = data
    diseaseselected = False
    print(str(pickednode))
    return json.dumps(data, indent=2)


#callback for creating gene network graph (cytoscape)
@dash_app.callback(
    Output('cytoscapenetw', 'elements'),

    Output('cytoscapenetw', 'layout'),
    
    Input('cytographlayout', 'value'),

    Input('updatecyto', 'n_clicks_timestamp'))
def set_elements( llayout, graphelement):

    if (uploadsort == 'D'):
        disses = [x[1] for x in genegenedegrees]

        #nodes = [{'data': {'id': x, 'label': y}} for x,y in zip(dfnodes.number,dfnodes.abbr)]
        
        
        #nodes = [{'data': {'id': x, 'label': y, 'size': z*5+5}} for x,y,z in zip(dfnodes.number,dfnodes.abbr, disses)]
        colors = []
        for colorelem in dfnodes.dpi:
            if (float(colorelem) < float(400)):
                col = "yellow"
                colors.append(col)
            elif (float(colorelem) < float(600)):
                col = "green"
                colors.append(col)
            elif (float(colorelem) < float(800)):
                col = "red"
                colors.append(col)
            else:
                col = "blue"
                colors.append(col)

        #coloring according to dpi
        nodes = [{'data': {'id': x, 'label': y, 'size': z*5+5, 'color': a}} for x,y,z,a in zip(dfnodes.number,dfnodes.abbr, disses, colors)]    

        edges = [{'data': {'source': x, 'target': y}} for x,y in zip(dfedges.source,dfedges.target)]

        layout={ 'name': llayout}

        elements = nodes + edges
    else:

        nodes = [{'data': {'id': x, 'label': y}} for x,y in zip(dfnodes.number,dfnodes.abbr)]
        edges = [{'data': {'source': x, 'target': y}} for x,y in zip(dfedges.source,dfedges.target)]

        layout={ 'name': llayout}

        elements = nodes + edges

    return elements, layout





tab3 = html.Div([
    html.H3('Bipartite gene-disease network / networkx'),

    html.Button('Update NXGraph', id='updatenx', n_clicks_timestamp=0),

    dcc.Graph(id="nxgr")

])

#callback for creating networkx bipartite graph
@dash_app.callback(
    Output('nxgr', 'figure'),
    Input('updatenx',  'n_clicks_timestamp')

)
def update_output2(ns):

    graph1 = createnxgraph(nxgraph1, dfnodestype1)
    return graph1



tab4 = html.Div([
    html.H3('disease network'),
    dcc.RadioItems(
    id='cytographlayout2',
    options=[
        {'label': 'circle', 'value': 'circle'},
        {'label': 'cose', 'value': 'cose'},
      
        
    ],
    value='cose'
    ),

     html.Button('Update Graph', id='updatecyto2', n_clicks_timestamp=0),
#cytoscape element
    cyto.Cytoscape(
        id='cytoscapenetw2',
        style={'width': '100%', 'height': '1200px'},
        elements=elements,
        layout={
            'name': 'circle'
        }
    ),
    html.Pre(id='cytoscape-tapNodeData-jsonb', style=styles['pre']),

])



#callback for picking nodes
@dash_app.callback(Output('cytoscape-tapNodeData-jsonb', 'children'),
              Input('cytoscapenetw2', 'tapNodeData'))
def displayTapNodeData(data):
    global pickednode
    global diseaseselected
    pickednode = data
    diseaseselected = True
    print(str(pickednode))
    return json.dumps(data, indent=2)
    

#callback for disease network graph
@dash_app.callback(
    Output('cytoscapenetw2', 'elements'),

    Output('cytoscapenetw2', 'layout'),
    
    Input('cytographlayout2', 'value'),

    Input('updatecyto2', 'n_clicks_timestamp'))
def set_elements( llayout, graphelement):
   
    genenodes = [{'data': {'id': x, 'label': y}} for x,y in zip(dfnodesgenes.number,dfnodesgenes.abbr)]
    geneedges = [{'data': {'source': x, 'target': y}} for x,y in zip(dfedgesgenes.source,dfedgesgenes.target)]

    layoutgene={ 'name': llayout}

    elementsgene = genenodes + geneedges

    return elementsgene, layoutgene





tab5 = html.Div([
    html.H3('Individual node statistics / degree histograms'),
#cytoscape element
    dcc.Textarea(
        id='textarea-example',
        value=str(pickednode),
        style={'width': '100%', 'height': 100},
    ),
    #show picked node
    html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line'}),

    html.Button('Show Node Statistics', id='showstat', n_clicks_timestamp=0),

     dt.DataTable(
        id='tbl', 
        data = [],
    
    ),

    html.H4("Histograms for the degree distribution of the networks:"),
    dcc.Graph(id="histo1"),

    html.P("Number of bins:"),
    dcc.Slider(id="binnumber", min=1, max=100, value=1, 
               marks={1: '1', 100: '100'}),

    dcc.RadioItems(
    id='histoselectgraph',
    options=[
        {'label': 'DiseaseGraph Degree Distribution', 'value': 'D'},
        {'label': 'GeneGraph Degree Distribution', 'value': 'G'},
        
        
    ],
    value='N'
    ),
   


])

#callback for creating the data table for statistics of selected node
@dash_app.callback(
  [  Output('tbl', 'data'), 
    Output('tbl', 'columns')],
    Input('showstat', 'n_clicks_timestamp'))
def update_stat_table(click):
    if diseaseselected == True:
        statgraph = nxgraphgenes
    else:
        statgraph = nxgraphdisease
  
    data1, columns1 = allcentralities(statgraph, pickednode)


    data2, columns2 = allcentralities(nxgraph1, pickednode)

    data = [data1, data2]
    data = pd.concat(data)
    
    data.index = ['Projection', 'Bipartite Graph']
    data['Graph Type'] = data.index
    data = data.reset_index()
  

    columns = [{"name": i, "id": i} for i in data.columns]
    data = data.to_dict('records')
  
    return data, columns


#callback for creating a degree distribution histogram
@dash_app.callback(
    Output("histo1", "figure"), 
    [Input("binnumber", "value"), 
     Input("histoselectgraph", "value")])
def display_color(binnumber, histoselectgraph):
    global disdisdegrees
    global genegenedegrees
  
    if histoselectgraph == 'D':
        disdisdegreedata = []
        for elem in disdisdegrees:
            disdisdegreedata.append(elem[1])
  
        fig = px.histogram(disdisdegreedata, nbins = binnumber)
    else: 
        genegenedegreedata = []
        for elem in genegenedegrees:
            genegenedegreedata.append(elem[1])
   
        fig = px.histogram(genegenedegreedata, nbins = binnumber)

        
  
    return fig

#show picked node
@dash_app.callback(
    Output('textarea-example-output', 'children'),
    Input('textarea-example', 'value')
)
def update_output(value):
    global pickednode
    print(str(pickednode))
    return 'You have selected: \n{}'.format(pickednode)


tab6 = html.Div([
    html.H3('Diversity-ubiquity plot for genes'),
    html.Button('Compute diversity-ubiquity plot for disease network', id='showubiqu', n_clicks_timestamp=0),
     dcc.Graph(id="ubiqugraph", style={'width': '90vh', 'height': '90vh'})

])

#create diversity-ubiquity plot
@dash_app.callback(
    Output('ubiqugraph', 'figure'), 
    Input('showubiqu', 'n_clicks_timestamp'))
def update_stat_table(click):
    
    bipartdegrees = nx.degree(nxgraph1)

    #for diselem in nxgraphgenes.nodes:
     #   del bipartdegrees[diselem]

    #number of diseases each gene causes
    bipartdegreesgene = { genekey: bipartdegrees[genekey] for genekey in nxgraphdisease.nodes }

    bipartdegreesgdis = { diskey: bipartdegrees[diskey] for diskey in nxgraphdisease.nodes }


 
    plotxy = []

    #calculate ubiquity for genes (i.e. average number of genes that also cause the disease)
    for elem in nxgraphdisease.nodes:
        disnumbers = []
        for dis in nxgraph1[elem]:
            disnumber = len(nxgraph1[dis])

            disnumbers.append(disnumber)
        avrgdis = np.mean(disnumbers)

        plotxy.append([elem, bipartdegreesgene[elem], avrgdis])
    
    plotxydf = pd.DataFrame(plotxy, columns=['elem', 'diversity', 'ubiquity'])

    #for elem in nxgraphdisease.nodes:
    #    print(len(nxgraphdisease[elem]))
    #    plotxy.append([elem, bipartdegreesgene[elem], len(nxgraphdisease[elem])])
    #number of genes for each disease

    fig = px.scatter(plotxydf, x="diversity", y="ubiquity", hover_data=['elem'], title="diversity-ubiquity plot", labels = {"diversity": "diversity: number of diseases the gene causes", "ubiquity": "ubiquity: average number of genes which also cause the disease"})

    return fig




dash_app.layout = html.Div([
    html.H1('Dash Graph multiple tabs', className="app-headerf" ),
    dcc.Tabs(className="app-header", id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(id="tab-1", label='Data upload', value='tab-1-example'),
        dcc.Tab(id="tab-2", label='Gene Network', value='tab-2-example'),
        dcc.Tab(id="tab-3", label='Bipartite network', value='tab-3-example'),
        dcc.Tab(id="tab-4", label='Disease network', value='tab-4-example'),
        dcc.Tab(id="tab-5", label='Statistics / pick node before', value='tab-5-example'),
        dcc.Tab(id="tab-6", label='Diversity-ubiquity plot', value='tab-6-example'),
    ]),
    html.Div( 
    id='tabs-content-example',
             children = tab1,className="app-headerf2")
             
],className="app-headerf",)

#callback for showing selected data
@dash_app.callback( 
    Output('table1', 'columns'),
    Output('table1', 'data'),
    Input('graphelement', 'value'))
def set_table(graphelement):
    global dfnodes
    global dfedges


    if (graphelement == 'N'):
        dataview = dfnodes

    elif (graphelement == 'E'):
        dataview = dfedges
  
    elif (graphelement == 'D'):
        dataview = df

    return [{"name": i, "id": i} for i in dataview.columns], dataview.to_dict('records')
    


#callback for switching tabs
@dash_app.callback(dash.dependencies.Output('tabs-content-example', 'children'),
             [dash.dependencies.Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1
    elif tab == 'tab-2-example':
 
        return tab2
    elif tab == 'tab-3-example':
 
        return tab3

    elif tab == 'tab-4-example':
  
        return tab4

    elif tab == 'tab-5-example':
   
        return tab5

    elif tab == 'tab-6-example':
        
        return tab6



#callback for choosing upload type
@dash_app.callback(dash.dependencies.Output('placeholder1', 'children'),
             [dash.dependencies.Input('sortofupload', 'value')])
def choose_upload(opt):
    global uploadsort
    uploadsort = opt 

    return opt

#callback for uploading files
def parse_contents_only(contents, filename, date):
    global dfnodes
    global dfedges
    global df

    global dflayout

    global dfnodesgenes
    global dfedgesgenes


    content_type, content_string = contents.split(',')

    global nxgraph1

    global nxgraphdisease
    global nxgraphgenes

    global dfnodestype1
    global dfnodestype2

    global diseasedegrees
    global disdisdegrees
    global genegenedegrees

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:


            if (uploadsort == 'D'):

                
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))

                print(df.columns)

                #disease filter
                df = df.query('source == "CTD_human" & diseaseType == "disease"' )
                df = df.query('score > ' + str(scorethreshold))

                #all to string
                df=df. applymap(str)


                dfnodes, dfedges, dfnodesgenes, dfedgesgenes, diseasedegrees, disdisdegrees, genegenedegrees = alldiseasegenegraphs(df)

                #nodessets
                dfnodestype1 = df['geneId']
                dfnodestype2 = df['diseaseId']


                # create bipartite graph in networkx 
                nxgraph1 = convertnx(df)


                #create gene network / networkx
                nxgraphdisease = convertnx_part(dfedges)

                #create disease network / networkx
                nxgraphgenes = convertnx_part(dfedgesgenes)
                

            elif (uploadsort == 'VN'):
                #header_list = ["id", "label", 'name', 'fct', 'sample']
                header_list = ["number", "abbr", 'name', 'fct', 'sample']
                dfnodes = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')),  names = header_list)
            elif (uploadsort == 'VL'):
                

                header_list = ["number", "xc", "yc", "zc", "xrgb", "yrgb", "zrgb", "100", "attr"]
                dflayout = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')),  names = header_list)
                
            else:
                #edge list - only source and target
                
                header_list = ["source", "target"]
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')),  names = header_list)
                
                nxgraph1 = convertnx_part(df)
                
                dfedges = df

                dfnodes = createnodes(dfedges, header_list_nodes)


        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'ERROR, file upload not successful!'
        ])

    return html.Div([

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(), 
     
    ])

#upload data
@dash_app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(lc, ln, ld):
    if lc is not None:
        children = [
            parse_contents_only(c, n, d) for c, n, d in
            zip(lc, ln, ld)]
        return children




if __name__ == '__main__':
   # socketio.run(app, host="127.0.0.1", port=5000)
    socketio.run(app)

