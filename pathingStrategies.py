

#import sys
#sys.path.insert(0, '.\pathing')
from hypar import glTF

import space_cfm_calc
import minSpanningPath
import heatmap
import MakeDuct

import math
from aecSpace.aecPoint import aecPoint


import qLayout


# def specIntoDuct(ductSpec):
    

def SimpleShortestPath(model, spaces, useColor):
    loads = space_cfm_calc.Space_CFM_Calc(spaces)
    ductSpecs = minSpanningPath.GetDuctPathFromBldg(loads)
    mini = min([x["cfm"] for x in ductSpecs])
    maxi = max([x["cfm"] for x in ductSpecs])
    numcolors = 12
    hmColors = []
    colorGray = model.add_material(0.5, 0.5, 0.5, 1.0, 0.2, "Gray")

    for i in range(numcolors):
        dI = i * (maxi-mini)/numcolors
        r,g,b = heatmap.convert_to_rgb(mini, maxi, dI)
        hmColors.append(model.add_material(r/255,g/255,b/255,1.0,1.0,"HM"+str(i)))
    for ductSpec in ductSpecs:
        print(ductSpec)
        start = aecPoint(ductSpec['start'][0], ductSpec['start'][1], ductSpec['start'][2])
        end = aecPoint(ductSpec['end'][0], ductSpec['end'][1], ductSpec['end'][2])
        chosenColor = math.floor(12-ductSpec['cfm'] / (maxi-mini) * 12 )
        duct = MakeDuct.makeDuct(start, end, ductSpec['height'], ductSpec['width'])
        ductMesh = duct.mesh_graphic
        if useColor == 1:
            model.add_triangle_mesh(ductMesh.vertices, ductMesh.normals, ductMesh.indices, hmColors[ chosenColor-1])   
        else:
            model.add_triangle_mesh(ductMesh.vertices, ductMesh.normals, ductMesh.indices, colorGray)   
    return model

def QLearnedPathing(model, spaces):
    
    ductSpecs = qLayout.GetDuctPathFromBldg(spaces)

    for ductSpec in ductSpecs:
        print(ductSpec)
        start = aecPoint(ductSpec['start'][0], ductSpec['start'][1], ductSpec['start'][2])
        end = aecPoint(ductSpec['end'][0], ductSpec['end'][1], ductSpec['end'][2])
        duct = MakeDuct.makeDuct(start, end, ductSpec['height'], ductSpec['width'])
        ductMesh = duct.mesh_graphic
    
    return model
    