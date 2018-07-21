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
import hypar

spaces = MakeSpaceTower.makeSpaceTower()
space_ceilings = []
#print(spaces)
for space in spaces:
    space_ceilings.append(space.getMesh2D)
print(space_ceilings[0])


'''
r = 3
c = 4

x = [i % c for i in range(r*c)]
y = [i / c for i in range(r*c)]

print x
print y
'''
