from random import randint, uniform

from shapely import geometry as shapely

from aecSpace.aecColor import aecColor
from aecSpace.aecFloor import aecFloor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer

def makeDuct(start: aecPoint, end: aecPoint, height: float, width: float) -> aecSpace:
    duct = aecSpace()
    
    

