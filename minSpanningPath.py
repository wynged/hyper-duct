from shapely.geometry import Point
from itertools import combinations
import networkx as nx
import ductSizing

import math

import CFMAndSizes

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
#            if __name__ == "__main__":
#                print(sp1, sp2)
            G.add_edge(sp1['id'],sp2['id'] , weight=dist, start=list(i), end=list(j))
    # print(G)
    span = nx.minimum_spanning_tree(G)
    return span
    
def EdgesToDict(G):
    myducts = []
    for e in G.edges:
        myducts.append(G[e[0]][e[1]])

    return myducts

def GetDuctPathFromBldg(bldg):
    allDucts = []
    for lvl in bldg:
        spanningTree = GetRoutes(lvl)
        # print("SpanningTree:", spanningTree)
        spanWithLoads = CFMAndSizes.AddCFMToRoute(lvl, spanningTree)
        spanWithSize = CFMAndSizes.AddSizesToRoute(spanWithLoads, -5)
        allDucts.extend( EdgesToDict(spanWithSize) )

    return allDucts
    
# ducts = GetDuctPathFromBldg()