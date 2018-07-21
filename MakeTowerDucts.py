from random import randint, uniform

import MakeDuct
import MakeSpaceTower
import ductSizing
import minSpanningPath
import space_cfm_calc
from hypar import glTF
from aecSpace.aecColor import aecColor
from aecSpace.aecFloor import aecFloor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

def makeTowerDucts():
    spaces = MakeSpaceTower.makeSpaceTower()
    # print(spaces)
    loads = space_cfm_calc.Space_CFM_Calc(spaces)
    print(loads[0])
    ductSpecs = minSpanningPath.GetDuctPathFromBldg(loads[0])
    ducts = []
    print(ductSpecs)
    for ductSpec in ductSpecs:
        print(ductSpec)
        start = aecPoint(ductSpec['start'][0], ductSpec['start'][1], ductSpec['start'][2])
        end = aecPoint(ductSpec['end'][0], ductSpec['end'][1], ductSpec['end'][2])
        ducts += [MakeDuct.makeDuct(start, end, ductSpec['width'], ductSpec['height'])]
    if len(ducts) == 1: ducts = [ducts]

    model = glTF()
    colorAqua = model.add_material(0.302, 0.722, 0.392, 0.1, 0.2, "Aqua)
    colorBlue = model.add_material(0.0, 0.631, 0.945, 0.1, 0.2, "Blue")
    colorCyan = model.add_material(0.275, 0.941, 0.941, 0.1, 0.2, "Cyan")
    colorGray = model.add_material(0.5, 0.5, 0.5, 0.1, 0.2, "Gray")
    colorGreen = model.add_material(0.486, 0.733, 0.0, 0.1, 0.2, "Green")
    colorOrange = model.add_material(0.964, 0.325, 0.078, 0.1, 0.2, "Orange")
    colorSand = model.add_material(0.75, 0.07, 1.0, 0.1, 0.2, "Sand")    
    colorYellow = model.add_material(1.0, 0.733, 0.0, 0.1, 0.2, "Yellow")
    for space in spaces:
        spaceMesh = space.mesh_graphic
        colorIndex = randint(0, 3)
        if colorIndex == 0: color = colorBlue
        if colorIndex == 1: color = colorOrange
        if colorIndex == 2: color = colorPurple
        if colorIndex == 3: color = colorYellow      
        model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, color)   
#    return {"model": model.save_base64(), 'computed':{'floors':levels, 'area':area}}   
    model.save_glb('C:\\Users\\aahau\\Dropbox\\Business\\Hypar\\Development\\GitHub\\hyper-duct\\model.glb')

makeTowerDucts()
#spaces = makeTowerDucts()
#spaceDrawer = aecSpaceDrawOCC()
#spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.

