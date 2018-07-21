
import networkx as nx

import ductSizing
import math

#this adds the load for each point along all edges in the path
def AddCFMToRoute(lvl, span):
    loadVar = 'cfm'
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
        edge["width"] =  w * 25.4
        edge["height"] =  h * 25.4

    return span