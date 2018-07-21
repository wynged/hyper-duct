import environment
import agent
import MakeSpaceTower as tower
from itertools import groupby


def containmentTest(spaces, xCoords, yCoords,sVal):
	obst = []
	for i in range(len(xCoords)):
		for space in spaces:
			points = space.points_ceiling
			xs = [p.x for p in points]
			ys = [p.y for p in points]

			if xCoords[i] >= min(xs) and xCoords[i] <= max(xs) and yCoords[i] >= min(ys) and yCoords[i] <= max(ys):
				obst.append((xCoords[i]/sVal,yCoords[i]/sVal))
	return obst



def GetDuctPathFromBldg(building):
    sVal = 4000
    allSpaces = building
    levels = []
    output = []

    for key, g  in groupby(allSpaces, key = lambda x: x.level):
        levels.append(list(g))
    #print(len(levels))


    for lvl in range(len(levels)-1):
        spaces = levels[lvl]
        floorX = 35000
        floorY = 75000
        u = int(floorX/sVal)
        v = int(floorY/sVal)
        

        shafts = [s for s in allSpaces if s.name == 'Shaft']
        print("Shafts found: ",len(shafts))
        shaft = shafts[0]

        obstacles = [s for s in spaces if s.name == 'Conference']

        xCoords = []
        yCoords = []

        for i in range(u):
            for j in range(v):
                xCoords.append(j*sVal)
                yCoords.append(i*sVal)

        obst = containmentTest(obstacles,xCoords,yCoords,sVal)
        print ('Obstacle Count',len(obst))

        for space in spaces:
            name = space.name

            start = shaft.centroid_ceiling
            center = space.centroid_ceiling
            Z = center.z

            # ------------------------------------environment-------------------------------------
            gridH, gridW = u,v
            start_pos = (int(int(round(start.x/sVal)*sVal)/sVal), 16)#int(int(round(start.y/sVal)*sVal)/sVal) )
            print(start_pos)
            targetY = int(int(round(center.y/sVal)*sVal)/sVal)
            if targetY > max(yCoords):
                targetY = max(yCoords)
            end_positions = [(int(int(round(center.x/sVal)*sVal)/sVal),targetY)] #[(endX[i],endY[i]) for i in range(len(endX))]
            print(end_positions)
            end_rewards = [100]
            blocked_positions =  obst #[(obstX[i],obstY[i]) for i in range(len(obstX))]
            default_reward = 0.0

            env = environment.Environment(gridH, gridW, end_positions, end_rewards, blocked_positions, start_pos, default_reward)

            # ---------------------------------------agent---------------------------------------------
            alpha = 0.2
            epsilon = 0.5
            discount = 0.99
            action_space = env.action_space
            state_space = env.state_space

            if end_positions[0] not in obst:
                a = agent.QLearningAgent(alpha, epsilon, discount, action_space, state_space)
                a.train(env,100000)

                qVals = a.qvalues
                path = a.get_path(env)

                if len(path)>1:
                    for i in range(1,len(path)-2):
                        start = [path[i][0],path[i][1],Z]
                        end = [path[i][0],path[i+1][1],Z]
                        ductspec = {'start':start, 'end':end, 'width': 254, 'height': 254, 'cfm':100, 'spaceName': name}
                        output.append(ductspec)
            
            #pyplot.plot(qVals)
            #pyplot.show()
            #print(output)
    print("WTF------------------------------------------------------------")
    print([len(i) for i in output])
    return output

if __name__ == "__main__":
    tower = tower.makeSpaceTower()
    GetDuctPathFromBldg(tower)
