import random
import MakeSpaceTower
# import hypar
# Import the classes we'll need.

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC
import itertools



def MechSummary(spaces, ductSpecs):
    totalSA = []
    DuctSA = []
    for x in spaces:
        DuctSA.append(spaces.get("cfm"))
    print(DuctSA)
    totalSA = sum(DuctSA)
    print(TotalSA)

MechSummary(spaces, ductSpecs)