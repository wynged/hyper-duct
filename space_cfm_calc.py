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

#creating tower with multiple spaces per floors
#spaces = MakeSpaceTower.makeSpaceTower()
def Space_CFM_Calc(spaces):
    #CFM per square foot dictionary
    CFM_per_FloorArea = {
        "Shaft":0,
        "Office":1,
        "Conference": 1.5,
        "Bathroom":0.5,
        "Lobby":1.25,
        "Kitchen":3,
        "Incubator":2.5,
        "Elevator lobby":1.25,
        "":0,
        "Corridor":0.5
    }

    #get name, area, ceiling point location, calculate airflow
    levels= []
    space_prop_dict = []
    for x in spaces:
        cfmpersqft = CFM_per_FloorArea.get(x.name)  #get cfm for room type from dictionary
        area_converted = x.area*0.00001076391   #concert mm^2 to ft^2
        cfm = area_converted * cfmpersqft   #get cfm from cfm/sqft
        cfm = round(cfm, -1)    #round up cfm by 10
        # print("calced CFM: ", cfm)
        rounded_level = int(x.level)
        space_prop_dict.append({"id":x.ID,"name":x.name, "area":area_converted, "location":x.center_ceiling.xyz, "cfm":cfm, "level":rounded_level}) #get space properties
        levels.append(rounded_level)
    print(space_prop_dict)
    levels_set = set(levels)    #round levels


    shaft_space = space_prop_dict[-1]
    del space_prop_dict[-1]
    shaft_xy = shaft_space.get("location")
    for x in levels_set:
        space_prop_dict.append({"id":"Shaft"+str(x),"name":"Shaft", "area":0.5, "location":shaft_xy, "cfm":0.5, "level":x})


    #group spaces by level
    output = []
    from operator import itemgetter
    sorted_levels = sorted(space_prop_dict, key=itemgetter('level'))
    for key, group in itertools.groupby(sorted_levels, key=lambda x:x['level']):
    #   print (key,)
        #print (list(group))
        output.append(list(group))
    #print(output)
    return output