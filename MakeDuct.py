from math import sqrt
from numpy import rad2deg, arctan2
from random import randint, uniform

from shapely import geometry as shapely

from aecSpace.aecColor import aecColor
from aecSpace.aecFloor import aecFloor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer

def makeDuct(start: aecPoint, end: aecPoint, width: float, height: float) -> aecSpace:
    shaper = aecShaper()
    duct = aecSpace()
    length = sqrt(((end.x - start.x) ** 2) + ((end.y - start.y) ** 2))
    duct.boundary = shaper.makeBox(aecPoint(0, 0, 0), xSize = length, ySize = width)
    midOrigin = aecPoint(0, (width * 0.5), 0)
    duct.moveTo(fromPnt = midOrigin, toPnt = start)
    angle = rad2deg(arctan2(end.y - start.y, end.x - start.x))
    duct.rotate(angle, start)
    duct.moveBy(z = (height * -0.5))
    duct.height = height
    return duct
    
   
# def makeDuctTest():
#    start = aecPoint(20, 50, 10)
#    end = aecPoint(60, 30, 10)
#    width = 5
#    height = 2
#    duct1 = makeDuct(start, end, width, height)
#    start = aecPoint(60, 30, 10)  
#    end = aecPoint(100, 50, 10)   
#    duct2 = makeDuct(start, end, width, height)
#    return [duct1, duct2]
#  
#spaces = makeDuctTest()
#spaceDrawer = aecSpaceDrawOCC()
#spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.        
    

