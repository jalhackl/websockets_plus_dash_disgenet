from inspect import Attribute
from networkx.algorithms.bipartite.basic import color
from networkx.classes.function import edges
from networkx.readwrite import edgelist
import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
import itertools
import plotly.graph_objects as go


def convertnx(dataframe):
  G=nx.from_pandas_edgelist(dataframe, source='geneId', target='diseaseId')
  return G

def convertnx_part(dataframe, source='source', target='target'):
  G=nx.from_pandas_edgelist(dataframe, source=source, target=target)
  return G

def convertnxbipartite(edges):
  bottom_nodes, top_nodes = bipartite.sets(edges)
  return bottom_nodes, top_nodes

#create bipartite graph with networkx
def createnxgraph(G, nodes1):

  pos = nx.spring_layout(G)
  bpartdict = dict()
  for node in G.nodes:
    for nodetype in nodes1:
      if node == nodetype:
        bpartdict[str(node)] = 'blue'
      else:
        bpartdict[str(node)] = 'red'

  # edges 
  edge_x = []
  edge_y = []
  for edge in G.edges():
      x0, y0 = pos[edge[0]]
      x1, y1 = pos[edge[1]]
      edge_x.append(x0)
      edge_x.append(x1)
      edge_x.append(None)
      edge_y.append(y0)
      edge_y.append(y1)
      edge_y.append(None)

  edge_trace = go.Scatter(
      x=edge_x, y=edge_y,
      line=dict(color='black', width=5),
      hoverinfo='none',
      showlegend=False,
      mode='lines')

  # nodes 
  node_x = []
  node_y = []
  text = []
  for node in G.nodes():
      x, y = pos[node]
      node_x.append(x)
      node_y.append(y)
      text.append(node)

  #2 sorts of nodes:
  node_x1 = []
  node_y1 = []
  text1 = []

  node_x2 = []
  node_y2 = []
  text2 = []

  #one loop for preparing all nodes
  for node in G.nodes:
    for nodetype in nodes1:
      if node == nodetype:
        x, y = pos[node]
        node_x1.append(x)
        node_y1.append(y)
        text1.append(node)   

  node_trace = go.Scatter(
      x=node_x, y=node_y, text=text,
      mode='markers+text',
      showlegend=False,
      hoverinfo='none',
      marker=dict(
          color='green',
          size=15,
          line=dict(color='black', width=1)))

  node_trace1 = go.Scatter(
    x=node_x1, y=node_y1, text=text1,
    mode='markers+text',
    showlegend=False,
    hoverinfo='none',
    marker=dict(
        color='blue',
        size=10,
        line=dict(color='black', width=1)))

  # layout
  layout = dict(plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=10, b=10, l=10, r=10, pad=0),
                xaxis=dict(linecolor='black',
                            showgrid=False,
                            showticklabels=False,
                            mirror=True),
                yaxis=dict(linecolor='black',
                            showgrid=False,
                            showticklabels=False,
                            mirror=True))

  fig = go.Figure(data=[edge_trace,  node_trace, node_trace1], layout=layout)
  return fig



#create nodes from simple edge list
def createnodes(edges, header_list_nodes):
    edgess = list(edges.source)
    edgest = list(edges.target)
    edgeslist = edgess + edgest
    edgesset = set(edgeslist)
    edgesunique = list(edgesset)

    nodesunique = {'source': edgesunique, 'target': edgesunique}
    #nodesunique = {'number': edgesunique, 'abbr': edgesunique}
   # newnodes = [{'data': {'id': x, 'label': y}} for x,y in zip(edgesunique,edgesunique)]

    newnodes = [{'number': x, 'abbr': y} for x,y in zip(edgesunique,edgesunique)]
    newnodes = pd.DataFrame(newnodes, columns=["number","abbr"])

    return newnodes




# create the Disease Network and the Disease Gene Network
# additionally. compute the degree of the nodes in each case
def alldiseasegenegraphs(data):

  genenodes = data.geneId
  diseasenodes = data.diseaseId


  diseasenodesfull = data [["diseaseId", "diseaseName"]]
  diseasenodesfull.columns = ['number', 'abbr']
 # dpi added
  genenodesfull = data[["geneId", "geneSymbol", "DPI"]]
  genenodesfull.columns = ['number', 'abbr', 'dpi']

  bothedges = data[["geneId", "diseaseId"]]

  genenodesset = pd.unique(genenodes)
  diseasenodesset = pd.unique(diseasenodes)
  diseasenet = []
  totalgenlist = []

  geneedges = []

  genedegrees = []
  for disease in diseasenodesset:
    totalgenlist = []
    genlist = []

    xx = bothedges.loc[bothedges['diseaseId'] == disease, ['geneId']]
   
    genlist.append( bothedges.loc[bothedges['diseaseId'] == disease, ['geneId']])

    totalgenlist.append( bothedges.loc[bothedges['diseaseId'] == disease, ['geneId']])
    diseasenet.append([disease, genlist])

    degreecount = 0
    for i in itertools.combinations(xx['geneId'],2):
      geneedges.append(i)
      degreecount = degreecount + 1
    genedegrees.append([disease, degreecount])

  diseaselist = []
  totaldiseaselist = []
  genenet = []

  diseaseedges = []

  diseasedegrees = []
  for gene in genenodesset:
 
    totaldiseaselist = []
    diseaselist = []
    xx = bothedges.loc[bothedges['geneId'] == gene, ['diseaseId']]
  
    diseaselist.append( bothedges.loc[bothedges['geneId'] == gene, ['diseaseId']])

    totaldiseaselist.append( bothedges.loc[bothedges['geneId'] == gene, ['diseaseId']])

    genenet.append([gene, diseaselist])
    diseasecount = 0
    for i in itertools.combinations(xx['diseaseId'],2):
      diseaseedges.append(i)
      diseasecount = diseasecount + 1
    diseasedegrees.append([gene, diseasecount])

  #data frame for gene graph
  geneedgespd = pd.DataFrame(geneedges, columns=["source","target"])

  #data frame for disease graph
  diseaseedgespd = pd.DataFrame(diseaseedges, columns=["source","target"])

  geneedgespd = geneedgespd.drop_duplicates()
  diseaseedgespd = diseaseedgespd.drop_duplicates()

  #calculate degrees for disease network
  disdisdegrees = []

  for disease in diseasenodesset:
    disdegree = 0
    xxd = diseaseedgespd.loc[diseaseedgespd['source'] == disease, ['target']]

    disdegree = disdegree + len(xxd)
    xxd = diseaseedgespd.loc[diseaseedgespd['target'] == disease, ['source']]

    disdegree = disdegree + len(xxd)
    disdisdegrees.append([disease, disdegree])
  
  genegenedegrees = []

  #calculate degrees for gene network
  for gene in genenodesset:
    genedegree = 0
    xxg = geneedgespd.loc[geneedgespd['source'] == gene, ['target']]

    genedegree = genedegree + len(xxg)
    xxg = geneedgespd.loc[geneedgespd['target'] == gene, ['source']]

    genedegree = genedegree + len(xxg)
    genegenedegrees.append([gene, genedegree])
  
  #no node duplicates
  genenodesfull=pd.DataFrame(genenodesfull).drop_duplicates()
  diseasenodesfull=pd.DataFrame(diseasenodesfull).drop_duplicates()

  return genenodesfull, geneedgespd, diseasenodesfull, diseaseedgespd, diseasedegrees, disdisdegrees, genegenedegrees


  #computation of popular centrality measures using networkx
def allcentralities(G, pickednode):
    degreenode = nx.degree(G, nbunch = pickednode['id'])
   
    degreecentr = nx.degree_centrality(G)
    degreecentrnode = degreecentr.get(pickednode['id'])

    betweencentr = nx.betweenness_centrality(G)
    betweencentrnode = betweencentr.get(pickednode['id'])

    eigencentr = nx.eigenvector_centrality(G)
    eigencentrnode = eigencentr.get(pickednode['id'])

    closenode = nx.closeness_centrality(G, u = pickednode["id"])
   
    datacloseness = pd.Series(closenode, index=['closeness'])

    datadeg = pd.Series(degreenode, index=['degree'])

    datadegcentr = pd.Series(degreecentrnode, index=['degree centrality'])

    databetweencentr = pd.Series(betweencentrnode, index=['betweenness centrality'])

    dataeigencentr = pd.Series(eigencentrnode, index=['eigenvector centrality'])
  
    seriesdata = pd.concat([datadeg, datacloseness, datadegcentr, databetweencentr, dataeigencentr])

    data = pd.DataFrame([seriesdata])
    columns=[{"name": i, "id": i} for i in data.columns]

    return data, columns