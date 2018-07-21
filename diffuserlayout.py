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

spaces = MakeSpaceTower.makeSpaceTower()
space_ceilings = []
#print(spaces)
for space in spaces:
    space_ceilings.append(space.mesh_ceiling)
print(space_ceilings[0])
