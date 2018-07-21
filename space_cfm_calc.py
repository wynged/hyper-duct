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
    #print(space_prop_dict)
    levels_set = set(levels)    #round levels
    

    shaft_space = next(item for item in space_prop_dict if item["name"] == "Shaft")
    shaft_index = next((index for (index, d) in enumerate(space_prop_dict) if d["name"] == "Shaft"), None)
    del space_prop_dict[shaft_index]
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

# Generate a new dictionary for the RA CFM using the output of above and applying rules. 
def Space_CFMRA_Calc(output):
    outputRA = []
    RA_X_offset = 5000
    RA_Y_offset = 5000
    for y in output:
        #print (y)
        outputRA.append(
           {"id":y.get("id")+"RA",
          "name":y.get("name"),
          "area":y.get("area"),
          "location":(y.get("location")[0] + RA_X_offset,y.get("location")[1] + RA_Y_offset,y.get("location")[2] + 0),
          "cfm":y.get("cfm") * 0.85, 
          "level":y.get("level")}
        )
    #print(output[2])
    #print(outputRA[2])
    #print(outputRA)
    return outputRA


if __name__ == "__main__":
    spaces = MakeSpaceTower.makeSpaceTower()
    supply = Space_CFM_Calc(spaces)
    for z in supply:
        Space_CFMRA_Calc(z)

