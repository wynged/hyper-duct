from random import randint, uniform

import MakeDuct
import MakeSpaceTower
import ductSizing
import minSpanningPath
import space_cfm_calc
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
    return ducts
    
ducts = makeTowerDucts()
# spaceDrawer = aecSpaceDrawOCC()
# spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.

