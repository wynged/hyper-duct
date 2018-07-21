from shapely.geometry import Point
from itertools import combinations
import networkx as nx

lstOPoints = [ (0,3),(2,5),(4,8),(7,3), (8,8) ]

G = nx.Graph()

for i,j in combinations(lstOPoints, 2):
    dist = Point(i[0], i[1]).distance(Point(j[0], j[1]))
    print(dist)
    if(dist > 0):
        G.add_edge(i,j , weight=dist)

print(G)
span = nx.minimum_spanning_tree(G)

rootnode = 3
loadVar = 'cfm'

#this adds the load for each point along all edges in the path
for n in range(0,len(lstOPoints)):
    if(n==rootnode):
        continue
    pth = next(nx.shortest_simple_paths(span, source=lstOPoints[rootnode], target=lstOPoints[n]))
    
    for i in range(1,len(pth)):
        print("i: ", i)
        print("node: ", )
        if loadVar not in span[pth[i-1]][pth[i]]:
            span[pth[i-1]][pth[i]][loadVar] = 0
        span[pth[i-1]][pth[i]][loadVar] += 100
        print(span[pth[i-1]][pth[i]])

bldg = [
   [
    { "name": "Space-101",
    "location": [1.2, 3.0, 1.0],
    "cfm": 100,
    },
    { "name": "Space-101",
    "location": [1.2, 3.0, 1.0],
    "cfm": 100,
     },
   ]
]







