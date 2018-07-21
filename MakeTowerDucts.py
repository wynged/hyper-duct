import sys
sys.path.insert(0, '.\pathing')

import MakeDuct
import MakeSpaceTower
import pathing.minSpanningPath
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

def makeTowerDucts(stories: int = 5, mostRooms: int = 4, routing = 0, useColor=0):
    model = glTF()
    spaces = MakeSpaceTower.makeSpaceTower(stories, mostRooms)
    number_of_spaces = len(spaces)

    alpha = 0.2
    reflect = 0.1
    colorAqua = model.add_material(0.302, 0.722, 0.392, alpha, reflect, "Aqua")
    colorBlue = model.add_material(0.0, 0.631, 0.945, alpha, reflect, "Blue")
    colorCyan = model.add_material(0.275, 0.941, 0.941, alpha, reflect, "Cyan")
    colorGranite = model.add_material(0.235, 0.235, 0.235, alpha, reflect, "Gray")
    colorGray = model.add_material(0.5, 0.5, 0.5, 1.0, 0.2, "Gray")
    colorGreen = model.add_material(0.486, 0.733, 0.0, alpha, reflect, "Green")
    colorOrange = model.add_material(0.964, 0.325, 0.078, alpha, reflect, "Orange")
    colorSand = model.add_material(1.0, 0.843, 0.376, alpha, reflect, "Sand") 
    colorTeal = model.add_material(0.0, 0.502, 0.502, alpha, reflect, "Teal")  
    colorYellow = model.add_material(1.0, 0.733, 0.0, alpha, reflect, "Yellow")

    loads = space_cfm_calc.Space_CFM_Calc(spaces)
    ductSpecs = pathing.minSpanningPath.GetDuctPathFromBldg(loads)
    mini = min([x["cfm"] for x in ductSpecs])
    maxi = max([x["cfm"] for x in ductSpecs])
    numcolors = 12
    hmColors = []

    xCoord = 13000
    yCoord = 74000
    point = aecPoint(xCoord, yCoord, 0)
    shaper = aecShaper()
    stack = aecSpace()
    stack.boundary = shaper.makeBox(point, 4000, 3000)
    stack.color = aecColor.gray
    stack.level = 8500
    stack.height = ((stories - 2) * 3500) + 8000
    spaces += [stack]
    
    xCoord = 10000
    yCoord = 65000
    point = aecPoint(xCoord, yCoord, 0)
    mech = aecSpace()
    mech.boundary = shaper.makeBox(point, 10000, 15000)
    mech.color = aecColor.gray
    mech.level = ((stories - 1) * 3500) + 11000
    mech.height = 4000
    spaces += [mech]   
    
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

    for i in range(numcolors):
        dI = i * (maxi-mini)/numcolors
        r,g,b = heatmap.convert_to_rgb(mini, maxi, dI)
        hmColors.append(model.add_material(r/255,g/255,b/255,1.0,1.0,"HM"+str(i)))
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

    return {"model": model.save_base64(), 'computed':{'Number of Spaces':number_of_spaces}}   
   # model.save_glb('model.glb')

# makeTowerDucts(stories = randint(5, 30), mostRooms = randint(2, 8), routing = randint(0, 1))

