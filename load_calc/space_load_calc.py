import random
# import hypar
# Import the classes we'll need.

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC
from itertools import groupby

#create an aecSpace object
space = aecSpace()
spacer = aecSpacer()
spaces = [space] + spacer.stack(space, 5, 1)

#CFM per space
for x in spaces:
    space_color = x.color.color
#    print (space_color)

space_points = []
for x in spaces:
    space_xyz = x.center_ceiling.xyz
    space_points.append(space_xyz)
#print (space_points)


space_points_grouped = []
space_points_grouped_list = []
for key, group in groupby(space_points, lambda x: x[2]):
    for thing in group:
        space_points_grouped = [thing[0], thing[1], key]
        space_points_grouped_list.append(space_points_grouped)

print(space_points_grouped_list)
    

'''
spacecolor = {
    (255,255,255) : "white",
    (0,0,0) : "black"
}
print(spacecolor.get((255,255,255)))

#Space location (x,y,z) grouped by floor
spacexy = space.center_ceiling.xy
print(spacexy)
spacez = space.center_ceiling.z
print(spacez)
spacexyz = space.center_ceiling.xyz
'''






'''

spacearea = space.area


#shaft location per floor

'''