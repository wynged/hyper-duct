import MakeDuct
import MakeSpaceTower
import minSpanningPath
import space_cfm_calc
import math
import heatmap
from random import randint
from hypar import glTF
from aecSpace.aecColor import aecColor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
import pathingStrategies
import MechSummary

print("finished imports")

def makeTowerDucts(stories: int = 5, mostRooms: int = 4, routing = 0, useColor=1):
    model = glTF()
    spaces = MakeSpaceTower.makeSpaceTower(stories, mostRooms)
    number_of_spaces = len(spaces)

    if routing == 0:
        model = pathingStrategies.SimpleShortestPath(model, spaces, useColor)
    if routing == 1:
        print("Qlearning!!!")
        model = pathingStrategies.QLearnedPathing(model, spaces)

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
    ductSpecs = minSpanningPath.GetDuctPathFromBldg(loads)
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

    flat_loads = [item for sublist in loads for item in sublist]
    airinfo  = MechSummary.air(flat_loads, ductSpecs)
    airinfo["Number of Spaces"] = number_of_spaces
    print(airinfo)

    print("About to export")
    model.save_glb('model.glb')
    return {"model": model.save_base64(), 'computed':airinfo}   

makeTowerDucts(stories = randint(5, 30), mostRooms = randint(2, 8), routing = 0 )

