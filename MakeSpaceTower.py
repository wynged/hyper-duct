from random import randint, uniform

from aecSpace.aecColor import aecColor
from aecSpace.aecFloor import aecFloor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

colors = \
[
    aecColor.aqua,     
    aecColor.blue,
    aecColor.cyan,
    aecColor.orange,
    aecColor.sand,
    aecColor.teal,
    aecColor.yellow,
]

def makeFloor(offset: float = 0.0,
              rotation: float = 0.0,
              roomsSouth: int = 1, 
              roomsEast: int = 2, 
              roomsNorth: int = 1, 
              roomsWest: int = 2,
              roomsNorthSize: float = 12000,
              roomsSouthSize: float = 15000):
    shell = aecFloor()
    floor = shell.floor
    corridor = shell.corridor
    if roomsSouth == 0:
        if randint(0, 1) == 0: roomsNorth = 0
        corridor.persons = 10
    else: corridor.persons = 5
    shaper = aecShaper()
    floorSizeX = 30000
    floorSizeY = 70000
    floor.boundary = shaper.makeBox(aecPoint(), floorSizeX, floorSizeY)
    shell.makeI(offset = offset,
                rotation = rotation,
                roomsWest = roomsWest, 
                roomsEast = roomsEast,
                roomsNorth = roomsNorth,
                roomsNorthSize = roomsNorthSize,
                roomsSouth = roomsSouth, 
                roomsSouthSize = roomsSouthSize)   
    rooms = shell.rooms.spaces
    roomsIndex =len(rooms) - 2
    if roomsIndex > 8:
        join = randint(0, roomsIndex)
        nxtRoom = join + 1
        if rooms[join].add(rooms[nxtRoom].points_floor): del rooms[nxtRoom]
    color = 0
    lastColor = 0
    for room in rooms:
        while color == lastColor: color = randint(1, 6)
        lastColor = color
        room.color = colors[color]
        room.color.alpha = 125
    corridor.space.color = aecColor.green
    floor.height = 7000
    floor.color = aecColor.aqua
    floor.color.alpha = 125
    corridor.space.height = 3500
    shell.rooms.setHeight(3500)    
    if roomsSouth == 0:
        floor.height = 10000
        corridor.space.height = 10000
        shell.rooms.setHeight(10000)
    return shell

def makeSpaceTower():
    x = 0
    y = 0
    z = 0
    rows = 1
    columns = 1
    stories = 20
    mostRooms = 8
    spaces = []
    vector = [0, 0, 0]
    xOffset = 100000
    yOffset = 90000
    zOffset = 3500
    
    while y < rows:
        while x < columns:
            rotate = 0
            while z < stories:
                spcGroup = aecSpaceGroup()
                offset = 0            
                if z == 0: 
                    southRooms = 0
                    zOffset = 10000
                else:
                    zOffset = 3500
                    southRooms = randint(1, 2)
                shell = makeFloor(offset = offset,
                                  rotation = rotate,
                                  roomsSouth = southRooms, 
                                  roomsEast = randint(1, mostRooms), 
                                  roomsNorth = 1, 
                                  roomsWest= randint(1, mostRooms),
                                  roomsNorthSize = randint(8000, 15000),
                                  roomsSouthSize = randint(8000, 15000))
                spcGroup.add([shell.corridor.space])
                spcGroup.add(shell.rooms.spaces)                  
                spcGroup.moveBy(vector[0], vector[1], vector[2])
                vector[2] += zOffset
                spaces += spcGroup.spaces               
                z += 1        
            z = 0
            x += 1
            vector[2] = 0
            vector[0] += xOffset      
        x = 0
        vector[0] = 0
        vector[2] = 0
        vector[1] += yOffset
        y += 1
        xCoord = 10000
        yCoord = 70000
        point = aecPoint(xCoord, yCoord, 0)
        core = aecSpace()
        shaper = aecShaper()
        core.boundary = shaper.makeBox(point, 10000, 10000)
        core.height = ((stories - 1) * 3500) + 15000
        core.color = aecColor.gray
        core.name = 'Shaft'
        spaces += [core]
        return spaces

#spaces = makeSpaceTower()
#spaceDrawer = aecSpaceDrawOCC()
#spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.