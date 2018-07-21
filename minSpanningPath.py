from shapely.geometry import Point
from itertools import combinations
import networkx as nx
import ductSizing

import math

tstbldg = [
   [
    { "name": "Space-101",
    "location": [10, 20, 10],
    "cfm": 100,
    },
    { "name": "Space-102",
    "location": [20, 30, 10],
    "cfm": 200,
     },
    { "name": "Space-103",
    "location": [30, 40, 10],
    "cfm": 250,
     },
    { "name": "Space-106",
    "location": [40, 50, 10],
    "cfm": 350,
     },
   ]
]

# lstOPoints = [ (0,3),(2,5),(4,8),(7,3), (8,8) ]

def GetRoutes(aLevel):
    G = nx.Graph()
    for sp1,sp2 in combinations(aLevel, 2):
        i,j = tuple(sp1['location']), tuple(sp2['location'])
        dist = Point(i[0], i[1]).distance(Point(j[0], j[1]))
        # print(dist)
        if(dist > 0):
            if __name__ == "__main__":
                print(sp1, sp2)
            G.add_edge(sp1['id'],sp2['id'] , weight=dist, start=list(i), end=list(j))
    # print(G)
    span = nx.minimum_spanning_tree(G)
    return span
    

#this adds the load for each point along all edges in the path
def AddCFMToRoute(lvl, span):
    # print("Level Info:", lvl)
    shafts = [s for s in lvl if s["name"] == "Shaft"]
    # print("Shafts: ", shafts)
    shaftNode = -1
    if len(shafts)>0:
        # print ("found shaft node")
        shaftNode = lvl.index(shafts[0])
    else:
        return span
    for n in range(0,len(lvl)):
        destSpace = lvl[n]
        # print("DestSpace: ", destSpace)
        if(n==shaftNode):
            continue 
        pth = next(nx.shortest_simple_paths(span, source=lvl[shaftNode]['id'], target=destSpace['id']))
        # print('found path')
        for i in range(1,len(pth)):
            # print("i: ", i)
            if loadVar not in span[pth[i-1]][pth[i]]:
                span[pth[i-1]][pth[i]][loadVar] = 0
            span[pth[i-1]][pth[i]][loadVar] += destSpace['cfm']
            # print(span[pth[i-1]][pth[i]])

    return span

def AddSizesToRoute(span):
    for e in span.edges:
        # print(e)
        edge = span[e[0]][e[1]]
        cfm = edge['cfm']
        if cfm > 0:
            ed = ductSizing.calcEDofPDandFlow(cfm, 0.08)
        else:
            ed = 1
        h = math.floor(ed)
        w = math.ceil(ductSizing.calcSecondDimension(ed, h))
        edge["width"] = w * 25.4
        edge["height"] = h * 25.4
        


    return span

# shaftnode = 0
loadVar = 'cfm'

def EdgesToDict(G):
    myducts = []
    for e in G.edges:
        myducts.append(G[e[0]][e[1]])

    return myducts

def GetDuctPathFromBldg(bldg):
    spanningTree = GetRoutes(bldg)
    # print("SpanningTree:", spanningTree)
    spanWithLoads = AddCFMToRoute(bldg, spanningTree)
    spanWithSize = AddSizesToRoute(spanWithLoads)
    return EdgesToDict(spanWithSize)
    
# ducts = GetDuctPathFromBldg()