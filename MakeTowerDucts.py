from random import randint, uniform

import MakeDuct
import MakeSpaceTower
import ductSizing
import minSpanningPath
import space_cfm_calc
import math
import heatmap
from hypar import glTF
from aecSpace.aecColor import aecColor
from aecSpace.aecFloor import aecFloor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

def makeTowerDucts(stories: int = 5, mostRooms: int = 4, routing = 0, useColor=0):
    model = glTF()
    spaces = MakeSpaceTower.makeSpaceTower(stories, mostRooms)


    colorAqua = model.add_material(0.302, 0.722, 0.392, 0.3, 0.2, "Aqua")
    colorBlue = model.add_material(0.0, 0.631, 0.945, 0.3, 0.2, "Blue")
    colorCyan = model.add_material(0.275, 0.941, 0.941, 0.3, 0.2, "Cyan")
    colorGranite = model.add_material(0.235, 0.235, 0.235, 0.3, 0.2, "Gray")
    colorGray = model.add_material(0.5, 0.5, 0.5, 1.0, 0.2, "Gray")
    colorGreen = model.add_material(0.486, 0.733, 0.0, 0.3, 0.2, "Green")
    colorOrange = model.add_material(0.964, 0.325, 0.078, 0.3, 0.2, "Orange")
    colorSand = model.add_material(1.0, 0.843, 0.376, 0.3, 0.2, "Sand") 
    colorTeal = model.add_material(0.0, 0.502, 0.502, 0.3, 0.2, "Teal")  
    colorYellow = model.add_material(1.0, 0.733, 0.0, 0.3, 0.2, "Yellow")
    for space in spaces:
        spaceMesh = space.mesh_graphic

        if space.color.color == aecColor.aqua: color = colorAqua
        if space.color.color == aecColor.blue: color = colorBlue
        if space.color.color == aecColor.cyan: color = colorCyan
        if space.color.color == aecColor.gray: color = colorGray 
        if space.color.color == aecColor.granite: color = colorGranite
        if space.color.color == aecColor.green: color = colorGreen
        if space.color.color == aecColor.orange: color = colorOrange
        if space.color.color == aecColor.sand: color = colorSand
        if space.color.color == aecColor.teal: color = colorTeal
        if space.color.color == aecColor.yellow: color = colorYellow
        model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, color)   
    
    loads = space_cfm_calc.Space_CFM_Calc(spaces)
    ductSpecs = minSpanningPath.GetDuctPathFromBldg(loads)
    # ducts = []
    mini = min([x["cfm"] for x in ductSpecs])
    maxi = max([x["cfm"] for x in ductSpecs])
    numcolors = 12
    hmColors = []

    # if len(ducts) == 1: ducts = [ducts]

    for i in range(numcolors):
        dI = i * (maxi-mini)/numcolors
        r,g,b = heatmap.convert_to_rgb(mini, maxi, dI)
        hmColors.append(model.add_material(r/255,g/255,b/255,1.0,0.2,"HM"+str(i)))
    for ductSpec in ductSpecs:
        start = aecPoint(ductSpec['start'][0], ductSpec['start'][1], ductSpec['start'][2])
        end = aecPoint(ductSpec['end'][0], ductSpec['end'][1], ductSpec['end'][2])
        chosenColor = math.floor(12-ductSpec['cfm'] / (maxi-mini) * 12 )
        duct = MakeDuct.makeDuct(start, end, ductSpec['width'], ductSpec['height'])
        ductMesh = duct.mesh_graphic
        if useColor == 1:
            model.add_triangle_mesh(ductMesh.vertices, ductMesh.normals, ductMesh.indices, hmColors[ chosenColor-1])   
        else:
            model.add_triangle_mesh(ductMesh.vertices, ductMesh.normals, ductMesh.indices, colorGray)   

#   return {"model": model.save_base64(), 'computed':{'floors':levels, 'area':area}}   
    model.save_glb('model.glb')

makeTowerDucts(stories = randint(5, 30), mostRooms = randint(2, 8), routing = randint(0, 1))
#spaces = makeTowerDucts()
#spaceDrawer = aecSpaceDrawOCC()
#spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.

